from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

FILES = {
    "2023/2024": DATA_DIR / "Data_TahunAjar_2023-2024.csv",
    "2024/2025": DATA_DIR / "Data_TahunAjar_2024-2025.csv",
    "2025/2026": DATA_DIR / "Data_TahunAjar_2025-2026.csv",
}


def parse_number(value, decimal=False):
    if pd.isna(value):
        return 0

    value = str(value).strip()
    if not value:
        return 0

    if decimal:
        value = value.replace(",", ".")
        try:
            return float(value)
        except ValueError:
            return 0

    value = value.replace(".", "").replace(",", "")
    try:
        return int(float(value))
    except ValueError:
        return 0


def load_new_dataset():
    records = []

    for school_year, filepath in FILES.items():
        if not filepath.exists():
            continue

        raw = pd.read_csv(filepath, header=None, skiprows=2, dtype=str)

        for _, row in raw.iterrows():
            if len(row) < 10:
                continue

            province = str(row.iloc[2]).strip()
            level = str(row.iloc[1]).strip()

            if not province or province.lower() == "nan":
                continue

            records.append({
                "tahun_ajar": school_year,
                "jenjang": level,
                "provinsi": province,
                "peserta_didik_baru": parse_number(row.iloc[3]),
                "jumlah_peserta_didik": parse_number(row.iloc[4]),
                "lulusan": parse_number(row.iloc[5]),
                "mengulang_jumlah": parse_number(row.iloc[6]),
                "mengulang_persentase": parse_number(row.iloc[7], decimal=True),
                "putus_jumlah": parse_number(row.iloc[8]),
                "putus_persentase": parse_number(row.iloc[9], decimal=True),
            })

    return pd.DataFrame(records)
