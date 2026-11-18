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
