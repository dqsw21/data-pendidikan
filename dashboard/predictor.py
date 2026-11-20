import pandas as pd
import numpy as np

from dashboard.data_processor import load_dataset


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


ALLOWED_YEARS = [2026, 2027, 2028]
FORECAST_YEARS = [2026, 2027, 2028]


def get_prediction_options():
    df = load_dataset()

    districts = sorted(
        df["bps_nama_kecamatan"].dropna().unique().tolist()
    )

    latest_year = int(df["tahun"].max())

    return {
        "districts": districts,
        "latest_year": latest_year,
        "default_prediction_year": 2026,
    }


def _calculate_stability(values):
    values = [float(v) for v in values if pd.notna(v)]

    if len(values) <= 1:
        return 50.0

    mean_value = np.mean(values)
    std_value = np.std(values)

    scale = abs(mean_value)

    if scale < 1e-6:
        scale = max([abs(v) for v in values] or [0])

    if scale < 1e-6:
        return 100.0

    score = 100 / (1 + (std_value / scale * 10))

    return round(max(0, min(100, score)), 2)


def _get_trend(values):
    if len(values) < 2:
        return {
            "direction": "Belum cukup data",
            "change": 0.0,
        }

    change = float(values[-1]) - float(values[-2])

    if change > 0:
        direction = "Naik"
    elif change < 0:
        direction = "Turun"
    else:
        direction = "Stabil"

    return {
        "direction": direction,
        "change": change,
    }


def _bounded_value(value, config):
    value = max(0.0, float(value))

    if config["category"] == "Lulusan":
        return value

    return min(100.0, value)


def _regional_statistics(df, column, year=None):
    if year is None:
        year = int(df["tahun"].max())

    values = df[df["tahun"] == year][column].dropna()

    if values.empty:
        return 0.0, 0.0, 0.0

    mean_value = float(values.mean())
    median_value = float(values.median())

    positive = values[values > 0]

    positive_mean = (
        float(positive.mean()) if not positive.empty else 0.0
    )

    return mean_value, median_value, positive_mean


# ============================================================
# PAE CORE
# Satu mesin tren aktual untuk semua kecamatan dan indikator.
# ============================================================

def calculate_indicator_forecast(
    district_data,
    full_dataset,
    column,
    config,
    target_year,
):
    historical = (
        district_data[["tahun", column]]
        .dropna()
        .sort_values("tahun")
    )

    years = historical["tahun"].astype(int).tolist()
    values = historical[column].astype(float).tolist()

    if not values:
        return 0.0, "Tidak ada data"

    current_year = years[-1]
    current_value = values[-1]

    if len(values) >= 2:
        year_gap = max(1, years[-1] - years[-2])
        annual_change = (values[-1] - values[-2]) / year_gap
    else:
        annual_change = 0.0

    related_indicators = {
        "angka_lulusan_sma": (
            "angka_mengulang_sma",
            "angka_putus_sekolah_sma",
        ),
        "angka_lulusan_ma": (
            "angka_mengulang_ma",
            "angka_putus_sekolah_ma",
        ),
        "angka_lulusan_smk": (
            "angka_mengulang_smk",
            "angka_putus_sekolah_smk",
        ),
    }

    is_graduate = config["category"] == "Lulusan"
    related_projection = {}

    if is_graduate and column in related_indicators:
        for related_column in related_indicators[column]:
            history = (
                district_data[["tahun", related_column]]
                .dropna()
                .sort_values("tahun")
            )

            related_values = history[related_column].astype(float).tolist()
            related_years = history["tahun"].astype(int).tolist()

            if not related_values:
                related_projection[related_column] = {
                    "value": 0.0,
                    "trend": 0.0,
                }
                continue

            related_trend = 0.0

            if len(related_values) >= 2:
                gap = max(1, related_years[-1] - related_years[-2])
                related_trend = (
                    related_values[-1] - related_values[-2]
                ) / gap

            related_projection[related_column] = {
                "value": related_values[-1],
                "trend": related_trend,
            }

    predicted = current_value

    # Asumsi pertumbuhan siswa moderat, bukan data aktual.
    student_growth_rate = 0.005

    for year in range(current_year + 1, int(target_year) + 1):
        yearly_change = annual_change

        if is_graduate:
            yearly_change += max(0.0, predicted) * student_growth_rate

            interaction_change = 0.0

            for projection in related_projection.values():
                previous_value = projection["value"]
                next_value = _bounded_value(
                    previous_value + projection["trend"],
                    {"category": "Rate"},
                )

                interaction_change -= 0.25 * (
                    next_value - previous_value
                )

                projection["value"] = next_value

            yearly_change = yearly_change + interaction_change

        predicted += yearly_change
        predicted = _bounded_value(predicted, config)

    method = "Local Trend + Student Growth Assumption + Dynamic Indicator Interaction"

    return predicted, method

def _build_explanation(
    config,
    current_value,
    predicted_value,
    trend,
    method_name,
    history_count,
    stability_score,
):
    change = predicted_value - current_value

    if change > 0:
        direction = "meningkat"
    elif change < 0:
        direction = "menurun"
    else:
        direction = "tetap"

    if config["category"] in ["Mengulang", "Putus Sekolah"]:
        if change > 0:
            interpretation = (
                "Nilai diproyeksikan meningkat dan perlu menjadi perhatian."
            )
        elif change < 0:
            interpretation = (
                "Nilai diproyeksikan menurun. Perubahan perlu dipantau."
            )
        else:
            interpretation = "Nilai diproyeksikan relatif tetap."
    else:
        if change > 0:
            interpretation = "Angka lulusan diproyeksikan meningkat."
        elif change < 0:
            interpretation = "Angka lulusan diproyeksikan menurun."
        else:
            interpretation = "Angka lulusan diproyeksikan tetap."

    explanation = (
        f"{config['label']} diperkirakan {direction}. "
        f"Nilai aktual terakhir {current_value:.4f}, "
        f"proyeksi {predicted_value:.4f}. "
        f"Metode: {method_name}."
    )

    method_explanation = (
        "Mesin membaca data aktual kecamatan, menghitung perubahan "
        "antar-tahun, lalu menggunakan perubahan tersebut sebagai "
        "dasar proyeksi tahun berikutnya. Prediksi dilakukan bertahap. "
        "Indikator lulusan tidak dibatasi maksimum 100."
    )

    return {
        "prediction_direction": direction,
        "interpretation": interpretation,
        "explanation": explanation,
        "method_explanation": method_explanation,
        "historical_trend": trend["direction"],
        "historical_change": trend["change"],
        "history_count": history_count,
        "stability_score": stability_score,
    }


def predict_education(district, prediction_year):
    df = load_dataset()
    prediction_year = int(prediction_year)

    if prediction_year not in ALLOWED_YEARS:
        raise ValueError(
            "Tahun prediksi hanya tersedia untuk 2026, 2027, dan 2028."
        )

    district_data = (
        df[df["bps_nama_kecamatan"] == district]
        .sort_values("tahun")
    )

    if district_data.empty:
        raise ValueError("Kecamatan tidak ditemukan dalam dataset.")

    latest_data = district_data.iloc[-1]
    actual_latest_year = int(latest_data["tahun"])

    predictions = []

    for column, config in INDICATORS.items():
        historical_data = (
            district_data[["tahun", column]]
            .dropna()
            .sort_values("tahun")
        )

        historical_values = (
            historical_data[column].astype(float).tolist()
        )

        historical_years = (
            historical_data["tahun"].astype(int).tolist()
        )

        current_value = float(historical_values[-1])

        trend = _get_trend(historical_values)
        stability_score = _calculate_stability(historical_values)

        predicted_value, method_name = calculate_indicator_forecast(
            district_data=district_data,
            full_dataset=df,
            column=column,
            config=config,
            target_year=prediction_year,
        )

        explanation_data = _build_explanation(
            config=config,
            current_value=current_value,
            predicted_value=predicted_value,
            trend=trend,
            method_name=method_name,
            history_count=len(historical_values),
            stability_score=stability_score,
        )

        predictions.append({
            "column": column,
            "label": config["label"],
            "category": config["category"],
            "level": config["level"],
            "current_value": current_value,
            "predicted_value": predicted_value,
            "change": predicted_value - current_value,
            "method": method_name,
            **explanation_data,
        })

    # Data aktual untuk grafik.
    actual_data = []

    for year in sorted(district_data["tahun"].unique()):
        year_row = district_data[district_data["tahun"] == year]

        if year_row.empty:
            continue

        row = year_row.iloc[-1]

        actual_data.append({
            "year": int(year),
            "type": "actual",
            "values": {
                column: (
                    float(row[column])
                    if pd.notna(row[column])
                    else 0.0
                )
                for column in INDICATORS
            },
        })

    # Prediksi 2026–2028.
    forecast_data = []

    for year in FORECAST_YEARS:
        year_predictions = {}

        for column, config in INDICATORS.items():
            predicted, _ = calculate_indicator_forecast(
                district_data=district_data,
                full_dataset=df,
                column=column,
                config=config,
                target_year=year,
            )

            year_predictions[column] = predicted

        forecast_data.append({
            "year": year,
            "type": "forecast",
            "values": year_predictions,
        })

    return {
        "district": district,
        "latest_year": actual_latest_year,
        "prediction_year": prediction_year,
        "actual_data": actual_data,
        "forecast_data": forecast_data,
        "predictions": predictions,
    }
