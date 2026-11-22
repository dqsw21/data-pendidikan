from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render

from .data_processor import load_dataset, get_chart_data


def home(request):
    from dashboard.dataset_processor import load_new_dataset

    df = load_new_dataset()

    statistics = {
        "total_data": len(df),
        "total_kecamatan": df["provinsi"].replace({"Bangka Belitung": "Kep. Bangka Belitung"}).nunique() if not df.empty else 0,
        "tahun_awal": "2023/2024",
        "tahun_akhir": "2025/2026",
        "total_jenjang": df["jenjang"].nunique() if not df.empty else 0,
    }

    context = {
        "statistics": statistics,
        "active_page": "home",
    }

    return render(request, "dashboard/home.html", context)


def dataset_explorer(request):
    from django.core.paginator import Paginator
    from dashboard.dataset_processor import load_new_dataset

    df = load_new_dataset()

    search_query = request.GET.get("q", "").strip()
    selected_year = request.GET.get("tahun", "").strip()

    if search_query:
        df = df[
            df["provinsi"].str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )
        ]

    if selected_year:
        df = df[df["tahun_ajar"] == selected_year]

    table_data = df.to_dict("records")
    years = ["2023/2024", "2024/2025", "2025/2026"]

    paginator = Paginator(table_data, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

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
    from dashboard.dataset_processor import load_new_dataset
    from dashboard.province_predictor import get_province_history

    df = load_new_dataset()

    provinces = sorted(
        df["provinsi"].dropna().unique().tolist()
    )

    actual_years = sorted(
        df["tahun_ajar"].dropna().unique().tolist(),
        key=lambda year: int(year[:4])
    )

    forecast_years = [
        "2026/2027",
        "2027/2028",
        "2028/2029",
        "2029/2030",
    ]

    available_years = actual_years + forecast_years

    selected_province = request.POST.get(
        "provinsi",
        request.GET.get("provinsi", provinces[0] if provinces else "")
    )

    selected_school_year = request.POST.get(
        "tahun_ajar",
        request.GET.get(
            "tahun_ajar",
            "2029/2030" if available_years else ""
        )
    )

    chart_data = {"labels": [], "series": {}}
    error = None

    try:
        if selected_province not in provinces:
            raise ValueError("Provinsi yang dipilih tidak valid.")

        if selected_school_year not in available_years:
            raise ValueError("Tahun ajar yang dipilih tidak tersedia.")

        chart_data = get_province_history(
            province=selected_province,
            selected_school_year=selected_school_year,
        )

    except (ValueError, TypeError, KeyError, IndexError) as exc:
        error = str(exc)

    context = {
        "active_page": "prediction",
        "provinces": provinces,
        "available_years": available_years,
        "selected_province": selected_province,
        "selected_school_year": selected_school_year,
        "chart_data": chart_data,
        "error": error,
    }

    return render(request, "dashboard/prediction.html", context)

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
