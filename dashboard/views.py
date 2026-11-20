from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render

from .data_processor import load_dataset, get_chart_data


def home(request):
    df = load_dataset()

    statistics = {
        "total_data": len(df),
        "total_kecamatan": df["bps_nama_kecamatan"].nunique(),
        "tahun_awal": int(df["tahun"].min()),
        "tahun_akhir": int(df["tahun"].max()),
        "total_jenjang": 3,
    }

    context = {
        "statistics": statistics,
        "chart_data": get_chart_data(),
        "active_page": "home",
    }

    return render(request, "dashboard/home.html", context)


def dataset_explorer(request):
    from django.core.paginator import Paginator

    df = load_dataset()

    search_query = request.GET.get("q", "").strip()
    selected_year = request.GET.get("tahun", "").strip()

    if search_query:
        df = df[
            df["bps_nama_kecamatan"].str.contains(
                search_query,
                case=False,
                na=False
            )
        ]

    if selected_year:
        df = df[df["tahun"] == int(selected_year)]

    columns = [
        "bps_nama_kecamatan",
        "tahun",
        "angka_mengulang_sma",
        "angka_putus_sekolah_sma",
        "angka_lulusan_sma",
        "angka_mengulang_ma",
        "angka_putus_sekolah_ma",
        "angka_lulusan_ma",
        "angka_mengulang_smk",
        "angka_putus_sekolah_smk",
        "angka_lulusan_smk",
    ]

    table_data = df[columns].fillna(0).to_dict("records")
    years = sorted(load_dataset()["tahun"].dropna().unique().astype(int).tolist())

    paginator = Paginator(table_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "selected_year": selected_year,
        "years": years,
        "total_filtered": len(table_data),
        "active_page": "dataset",
    }

    return render(request, "dashboard/dataset.html", context)


def prediction_page(request):
    from dashboard.predictor import (
        get_prediction_options,
        predict_education,
        INDICATORS,
    )

    options = get_prediction_options()

    district = request.POST.get(
        "kecamatan",
        request.GET.get(
            "kecamatan",
            options["districts"][0] if options["districts"] else ""
        )
    )

    year_input = request.POST.get(
        "tahun",
        request.GET.get(
            "tahun",
            str(options["default_prediction_year"])
        )
    )

    result = None
    error = None
    chart_data = {}

    try:
        prediction_year = int(year_input)

        result = predict_education(
            district=district,
            prediction_year=prediction_year
        )

        df = load_dataset()

        district_data = df[
            df["bps_nama_kecamatan"] == district
        ].sort_values("tahun")

        actual_years = sorted(
            district_data["tahun"].dropna().astype(int).unique().tolist()
        )

        forecast_years = [2026, 2027, 2028]
        chart_years = actual_years + forecast_years

        chart_data = {
            "labels": chart_years,
            "mengulang": [],
            "putus_sekolah": [],
            "lulusan": [],
        }

        category_keys = {
            "Mengulang": "mengulang",
            "Putus Sekolah": "putus_sekolah",
            "Lulusan": "lulusan",
        }

        colors = {
            "SMA": "#2563eb",
            "MA": "#0d9488",
            "SMK": "#f59e0b",
        }

        for column, config in INDICATORS.items():
            category = category_keys[config["category"]]

            actual_values = []

            for year in actual_years:
                year_rows = district_data[
                    district_data["tahun"] == year
                ]

                value = (
                    float(year_rows.iloc[-1][column])
                    if not year_rows.empty
                    else None
                )

                actual_values.append(value)

            forecast_values = []

            for year in forecast_years:
                forecast_result = predict_education(
                    district=district,
                    prediction_year=year
                )

                prediction_item = next(
                    item for item in forecast_result["predictions"]
                    if item["column"] == column
                )

                forecast_values.append(
                    prediction_item["predicted_value"]
                )

            chart_data[category].append({
                "label": config["level"],
                "color": colors[config["level"]],
                "actual": actual_values + [None] * len(forecast_years),
                "forecast": (
                    [None] * len(actual_years)
                    + forecast_values
                ),
            })

    except (ValueError, TypeError, KeyError, IndexError) as exc:
        error = str(exc)

    context = {
        "active_page": "prediction",
        "districts": options["districts"],
        "selected_district": district,
        "latest_year": options["latest_year"],
        "prediction_year": year_input,
        "result": result,
        "chart_data": chart_data,
        "error": error,
    }

    return render(request, "dashboard/prediction.html", context)

def analysis_page(request):
    from .analysis_engine import analyze_education

    analysis = analyze_education()

    selected_year = request.GET.get("tahun", analysis.get("latest_year"))
    try:
        selected_year = int(selected_year)
    except (ValueError, TypeError):
        selected_year = analysis.get("latest_year")

    analysis = analyze_education(selected_year)

    changes_by_indicator = []

    if not analysis.get("error"):
        for indicator in analysis["indicator_summary"]:
            changes = [
                item for item in analysis["change_summary"]
                if item["column"] == indicator["column"]
            ]

            changes.sort(
                key=lambda item: abs(item["change"]),
                reverse=True
            )

            changes_by_indicator.append({
                "indicator": indicator,
                "changes": changes[:5],
            })

    context = {
        "analysis": analysis,
        "changes_by_indicator": changes_by_indicator,
        "active_page": "analysis",
    }

    return render(request, "dashboard/analysis.html", context)


def model_info_page(request):
    from django.shortcuts import render

    context = {
        "active_page": "model_info",
    }

    return render(request, "dashboard/model_info.html", context)


def about_page(request):
    context = {"active_page": "about"}
    return render(request, "dashboard/about.html", context)


def landing_page(request):
    return render(request, "dashboard/landing.html")





def dashboard_ai_explanation(request):
    import hashlib
    import json

    from django.core.cache import cache
    from django.http import JsonResponse

    from dashboard.data_processor import load_dataset, get_chart_data
    from dashboard.ai_interpreter import ai_interpreter
    from dashboard.ai_service import AIServiceError

    df = load_dataset()

    statistics = {
        "total_data": len(df),
        "total_kecamatan": df["bps_nama_kecamatan"].nunique(),
        "tahun_awal": int(df["tahun"].min()),
        "tahun_akhir": int(df["tahun"].max()),
        "total_jenjang": 3,
    }

    chart_data = get_chart_data()

    cache_context = {
        "statistics": statistics,
        "charts": chart_data,
    }

    fingerprint = hashlib.sha256(
        json.dumps(
            cache_context,
            sort_keys=True,
            ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()

    cache_key = f"dashboard_ai_{fingerprint}"

    cached_result = cache.get(cache_key)

    if cached_result:
        return JsonResponse({
            **cached_result,
            "cached": True,
        })

    try:
        result = ai_interpreter.explain_dashboard(
            chart_data=chart_data,
            statistics=statistics,
        )

        response_data = {
            "success": True,
            "explanations": result["explanations"],
            "model": result["model"],
            "elapsed": result["elapsed"],
            "cached": False,
        }

        cache.set(cache_key, response_data, timeout=86400)

        return JsonResponse(response_data)

    except AIServiceError:
        return JsonResponse({
            "success": False,
            "error": "AI sedang tidak dapat memberikan analisis. Silakan coba kembali.",
        }, status=503)

    except Exception:
        return JsonResponse({
            "success": False,
            "error": "Terjadi kesalahan saat memproses analisis AI.",
        }, status=500)


def prediction_ai_explanation(request):
    import hashlib
    import json

    from django.core.cache import cache
    from django.http import JsonResponse

    from dashboard.predictor import predict_education
    from dashboard.ai_interpreter import ai_interpreter
    from dashboard.ai_service import AIServiceError

    district = request.GET.get("kecamatan", "").strip()
    year_input = request.GET.get("tahun", "").strip()

    if not district or not year_input:
        return JsonResponse({
            "success": False,
            "error": "Kecamatan dan tahun prediksi harus diisi.",
        }, status=400)

    try:
        prediction_year = int(year_input)
        prediction_data = predict_education(
            district=district,
            prediction_year=prediction_year,
        )

        cache_context = {
            "district": district,
            "year": prediction_year,
            "prediction": prediction_data,
        }

        fingerprint = hashlib.sha256(
            json.dumps(
                cache_context,
                sort_keys=True,
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()

        cache_key = f"prediction_ai_{fingerprint}"

        cached_result = cache.get(cache_key)

        if cached_result:
            return JsonResponse({
                **cached_result,
                "cached": True,
            })

        result = ai_interpreter.explain_prediction(
            district=district,
            prediction_year=prediction_year,
            chart_data=prediction_data,
        )

        response_data = {
            "success": True,
            "district": district,
            "prediction_year": prediction_year,
            "explanations": result["explanations"],
            "model": result["model"],
            "elapsed": result["elapsed"],
            "cached": False,
        }

        cache.set(cache_key, response_data, timeout=86400)

        return JsonResponse(response_data)

    except AIServiceError:
        return JsonResponse({
            "success": False,
        "error": "AI sedang tidak dapat memberikan analisis. Silakan coba kembali.",
        }, status=503)

    except (ValueError, TypeError):
        return JsonResponse({
            "success": False,
            "error": "Kecamatan atau tahun prediksi tidak valid.",
        }, status=400)

    except Exception:
        return JsonResponse({
            "success": False,
            "error": "Terjadi kesalahan saat memproses analisis AI prediksi.",
        }, status=500)
