from dashboard.dataset_processor import load_new_dataset


METRICS = {
    "lulusan": {
        "count": "lulusan",
        "label": "Lulusan",
    },
    "mengulang": {
        "count": "mengulang_jumlah",
        "label": "Mengulang",
    },
    "putus": {
        "count": "putus_jumlah",
        "label": "Putus Sekolah",
    },
    "peserta_baru": {
        "count": "peserta_didik_baru",
        "label": "Peserta Didik Baru",
    },
    "jumlah_peserta": {
        "count": "jumlah_peserta_didik",
        "label": "Jumlah Peserta Didik",
    },
}


def linear_forecast(years, values, target_year):
    """Prediksi menggunakan tren linear seluruh data historis."""
    valid = [
        (int(year), float(value))
        for year, value in zip(years, values)
        if value is not None
    ]

    if not valid:
        return 0.0

    if len(valid) == 1:
        return max(0.0, valid[0][1])

    mean_x = sum(x for x, _ in valid) / len(valid)
    mean_y = sum(y for _, y in valid) / len(valid)

    numerator = sum(
        (x - mean_x) * (y - mean_y)
        for x, y in valid
    )

    denominator = sum(
        (x - mean_x) ** 2
        for x, _ in valid
    )

    slope = numerator / denominator if denominator else 0.0
    intercept = mean_y - slope * mean_x

    return max(0.0, intercept + slope * target_year)


def generate_province_prediction(province, target_year):
    df = load_new_dataset()

    province_data = df[df["provinsi"] == province].copy()

    if province_data.empty:
        raise ValueError("Data provinsi tidak ditemukan.")

    province_data["year_start"] = (
        province_data["tahun_ajar"]
        .str[:4]
        .astype(int)
    )

    actual_years = sorted(
        province_data["year_start"].unique().tolist()
    )

    last_year = max(actual_years)

    if target_year <= last_year:
        raise ValueError(
            f"Tahun prediksi harus lebih besar dari {last_year}."
        )

    years = list(range(actual_years[0], target_year + 1))
    labels = [f"{year}/{year + 1}" for year in years]

    result = {
        "labels": labels,
        "series": {},
    }

    for level in ["SMA", "SMK"]:
        level_data = (
            province_data[province_data["jenjang"] == level]
            .sort_values("year_start")
        )

        if level_data.empty:
            continue

        historical = level_data[
            level_data["year_start"].isin(actual_years)
        ]

        historical_years = historical["year_start"].astype(int).tolist()

        student_values = (
            historical["jumlah_peserta_didik"]
            .astype(float)
            .tolist()
        )

        predicted_students = {
            year: linear_forecast(
                historical_years,
                student_values,
                year,
            )
            for year in range(last_year + 1, target_year + 1)
        }

        for metric_key, metric in METRICS.items():
            count_column = metric["count"]

            historical_counts = (
                historical[count_column]
                .astype(float)
                .tolist()
            )

            predicted_counts = {
                year: linear_forecast(
                    historical_years,
                    historical_counts,
                    year,
                )
                for year in range(last_year + 1, target_year + 1)
            }

            actual_count = [None] * len(years)
            actual_percent = [None] * len(years)

            forecast_count = [None] * len(years)
            forecast_percent = [None] * len(years)

            for _, row in historical.iterrows():
                year = int(row["year_start"])
                index = year - years[0]

                count = float(row[count_column])
                students = float(row["jumlah_peserta_didik"])

                actual_count[index] = count

                actual_percent[index] = (
                    count / students * 100
                    if students > 0
                    else 0.0
                )

            for year in range(last_year + 1, target_year + 1):
                index = year - years[0]

                count = predicted_counts[year]
                students = predicted_students[year]

                forecast_count[index] = count

                forecast_percent[index] = (
                    count / students * 100
                    if students > 0
                    else 0.0
                )

            result["series"][f"{level}_{metric_key}"] = {
                "level": level,
                "metric": metric["label"],
                "actual_count": actual_count,
                "actual_percent": actual_percent,
                "forecast_count": forecast_count,
                "forecast_percent": forecast_percent,
            }

    return result


def get_province_history(province, selected_school_year):
    """Prediksi menggunakan tren, momentum, dan percepatan yang diredam."""
    df = load_new_dataset()
    province_data = df[df["provinsi"] == province].copy()

    if province_data.empty:
        raise ValueError("Data provinsi tidak ditemukan.")

    province_data["year_start"] = (
        province_data["tahun_ajar"].str[:4].astype(int)
    )

    actual_years = sorted(province_data["year_start"].unique().tolist())
    last_actual_year = max(actual_years)
    selected_start_year = int(selected_school_year[:4])

    if selected_start_year < actual_years[0] or selected_start_year > 2029:
        raise ValueError("Tahun ajar yang dipilih tidak tersedia.")

    years = list(range(actual_years[0], selected_start_year + 1))
    labels = [f"{year}/{year + 1}" for year in years]

    result = {"labels": labels, "series": {}}

    def forecast_values(values, steps):
        values = [float(v) for v in values]

        if not values:
            return [0.0] * steps

        if len(values) == 1:
            return [max(0.0, values[-1])] * steps

        changes = [
            values[i] - values[i - 1]
            for i in range(1, len(values))
        ]

        recent_change = changes[-1]

        if len(changes) >= 2:
            trend = changes[-1] * 0.70 + changes[-2] * 0.30
            acceleration = changes[-1] - changes[-2]
        else:
            trend = recent_change
            acceleration = 0.0

        current = values[-1]
        forecasts = []

        # Fluktuasi naik-turun terkontrol.
        fluctuation = max(abs(current) * 0.025, abs(trend) * 0.50, 1.0)
        directions = [1, -1, -1, 1, -1, 1]

        for step in range(steps):
            damping = 0.90 ** step
            trend_change = trend * damping
            acceleration_change = acceleration * (0.35 ** (step + 1))
            random_direction = directions[step % len(directions)]

            variation = fluctuation * random_direction * (0.85 ** step)

            change = trend_change + acceleration_change + variation
            current = max(0.0, current + change)

            forecasts.append(current)

        return forecasts

    forecast_steps = max(0, selected_start_year - last_actual_year)

    for level in ["SMA", "SMK"]:
        level_data = province_data[
            province_data["jenjang"] == level
        ].sort_values("year_start")

        historical = level_data[
            level_data["year_start"].isin(actual_years)
        ]

        student_values = (
            historical["jumlah_peserta_didik"].astype(float).tolist()
        )

        student_predictions = forecast_values(
            student_values, forecast_steps
        )

        student_forecasts = {
            year: student_predictions[index]
            for index, year in enumerate(
                range(last_actual_year + 1, selected_start_year + 1)
            )
        }

        for metric_key, metric in METRICS.items():
            column = metric["count"]
            historical_counts = historical[column].astype(float).tolist()

            predictions = forecast_values(
                historical_counts, forecast_steps
            )

            metric_forecasts = {
                year: predictions[index]
                for index, year in enumerate(
                    range(last_actual_year + 1, selected_start_year + 1)
                )
            }

            actual_count = []
            actual_percent = []
            forecast_count = []
            forecast_percent = []

            for year in years:
                row = historical[historical["year_start"] == year]

                if not row.empty:
                    record = row.iloc[0]
                    count = float(record[column])
                    students = float(record["jumlah_peserta_didik"])

                    actual_count.append(count)
                    actual_percent.append(
                        count / students * 100 if students > 0 else 0.0
                    )
                    forecast_count.append(None)
                    forecast_percent.append(None)

                else:
                    count = metric_forecasts.get(year)
                    students = student_forecasts.get(year)

                    actual_count.append(None)
                    actual_percent.append(None)
                    forecast_count.append(count)
                    forecast_percent.append(
                        count / students * 100
                        if count is not None and students and students > 0
                        else 0.0
                    )

            result["series"][f"{level}_{metric_key}"] = {
                "level": level,
                "metric": metric["label"],
                "actual_count": actual_count,
                "actual_percent": actual_percent,
                "forecast_count": forecast_count,
                "forecast_percent": forecast_percent,
            }

    return result
