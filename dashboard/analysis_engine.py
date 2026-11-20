from .data_processor import load_dataset


INDICATORS = {
    "angka_mengulang_sma": {
        "label": "Angka Mengulang SMA",
        "category": "Mengulang",
        "level": "SMA",
    },
    "angka_putus_sekolah_sma": {
        "label": "Angka Putus Sekolah SMA",
        "category": "Putus Sekolah",
        "level": "SMA",
    },
    "angka_lulusan_sma": {
        "label": "Angka Lulusan SMA",
        "category": "Lulusan",
        "level": "SMA",
    },
    "angka_mengulang_ma": {
        "label": "Angka Mengulang MA",
        "category": "Mengulang",
        "level": "MA",
    },
    "angka_putus_sekolah_ma": {
        "label": "Angka Putus Sekolah MA",
        "category": "Putus Sekolah",
        "level": "MA",
    },
    "angka_lulusan_ma": {
        "label": "Angka Lulusan MA",
        "category": "Lulusan",
        "level": "MA",
    },
    "angka_mengulang_smk": {
        "label": "Angka Mengulang SMK",
        "category": "Mengulang",
        "level": "SMK",
    },
    "angka_putus_sekolah_smk": {
        "label": "Angka Putus Sekolah SMK",
        "category": "Putus Sekolah",
        "level": "SMK",
    },
    "angka_lulusan_smk": {
        "label": "Angka Lulusan SMK",
        "category": "Lulusan",
        "level": "SMK",
    },
}


def analyze_education(year=None):
    df = load_dataset()

    available_years = sorted(
        df["tahun"].dropna().astype(int).unique().tolist()
    )

    if not available_years:
        return {
            "error": "Dataset tidak memiliki data tahun.",
        }

    latest_year = max(available_years)

    if year is None:
        year = latest_year

    year = int(year)

    current = df[df["tahun"] == year].copy()

    if current.empty:
        return {
            "error": f"Data tahun {year} tidak tersedia.",
            "available_years": available_years,
        }

    previous_year = year - 1
    previous = df[df["tahun"] == previous_year].copy()

    indicator_summary = []
    level_summary = []
    district_summary = []
    change_summary = []

    for column, config in INDICATORS.items():
        values = current[column].dropna()

        if values.empty:
            continue

        highest_idx = current[column].idxmax()
        lowest_idx = current[column].idxmin()

        highest_row = current.loc[highest_idx]
        lowest_row = current.loc[lowest_idx]

        indicator_summary.append({
            "column": column,
            "label": config["label"],
            "category": config["category"],
            "level": config["level"],
            "mean": float(values.mean()),
            "median": float(values.median()),
            "min": float(values.min()),
            "max": float(values.max()),
            "highest_district": highest_row["bps_nama_kecamatan"],
            "highest_value": float(highest_row[column]),
            "lowest_district": lowest_row["bps_nama_kecamatan"],
            "lowest_value": float(lowest_row[column]),
            "data_count": int(values.count()),
        })

    for level in ["SMA", "MA", "SMK"]:
        level_indicators = [
            item for item in indicator_summary
            if item["level"] == level
        ]

        level_summary.append({
            "level": level,
            "indicator_count": len(level_indicators),
            "indicators": level_indicators,
        })

    for _, row in current.iterrows():
        district_summary.append({
            "district": row["bps_nama_kecamatan"],
            "year": int(row["tahun"]),
            "indicators": {
                column: float(row[column])
                for column in INDICATORS
                if column in row and row[column] is not None
            },
        })

    if not previous.empty:
        previous = previous.set_index("bps_nama_kecamatan")

        for column, config in INDICATORS.items():
            for _, row in current.iterrows():
                district = row["bps_nama_kecamatan"]

                if district not in previous.index:
                    continue

                old_value = float(previous.loc[district, column])
                new_value = float(row[column])
                difference = new_value - old_value

                change_summary.append({
                    "district": district,
                    "column": column,
                    "label": config["label"],
                    "category": config["category"],
                    "level": config["level"],
                    "previous_year": previous_year,
                    "current_year": year,
                    "previous_value": old_value,
                    "current_value": new_value,
                    "change": difference,
                    "direction": (
                        "naik" if difference > 0
                        else "turun" if difference < 0
                        else "tetap"
                    ),
                })

    increases = sorted(
        [item for item in change_summary if item["change"] > 0],
        key=lambda item: item["change"],
        reverse=True,
    )

    decreases = sorted(
        [item for item in change_summary if item["change"] < 0],
        key=lambda item: item["change"],
    )

    return {
        "year": year,
        "latest_year": latest_year,
        "available_years": available_years,
        "total_data": len(current),
        "total_districts": current["bps_nama_kecamatan"].nunique(),
        "indicator_summary": indicator_summary,
        "level_summary": level_summary,
        "district_summary": district_summary,
        "change_summary": change_summary,
        "top_increases": increases[:10],
        "top_decreases": decreases[:10],
    }


def get_education_analysis(year=None):
    return analyze_education(year)
