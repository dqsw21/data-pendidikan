from pathlib import Path

import pandas as pd

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset_pendidikan.csv"

NUMERIC_COLUMNS = [
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


def load_dataset():
    df = pd.read_csv(DATASET_PATH, dtype=str)

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column].str.replace(",", ".", regex=False),
            errors="coerce"
        )

    df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")

    return df


def get_chart_data():
    df = load_dataset()

    indicators = {
        "mengulang": [
            "angka_mengulang_sma",
            "angka_mengulang_ma",
            "angka_mengulang_smk",
        ],
        "putus_sekolah": [
            "angka_putus_sekolah_sma",
            "angka_putus_sekolah_ma",
            "angka_putus_sekolah_smk",
        ],
        "lulusan": [
            "angka_lulusan_sma",
            "angka_lulusan_ma",
            "angka_lulusan_smk",
        ],
    }

    result = {}

    for category, columns in indicators.items():
        grouped = df.groupby("tahun")[columns].mean().round(2)

        result[category] = {
            "labels": [int(year) for year in grouped.index],
            "datasets": [
                {
                    "label": level,
                    "data": grouped[column].fillna(0).tolist(),
                }
                for level, column in zip(["SMA", "MA", "SMK"], columns)
            ],
        }

    return result
