import json

from dashboard.ai_service import gemini_service


class AIDataInterpreter:

    @staticmethod
    def explain_dashboard(chart_data, statistics):
        data_context = {
            "statistics": statistics,
            "charts": chart_data,
        }

        prompt = f"""
Kamu adalah AI analis data pendidikan pada website Data Pendidikan.

DATA:
{json.dumps(data_context, ensure_ascii=False)}

ATURAN:
- Gunakan bahasa Indonesia yang sederhana, jelas, dan mudah dipahami.
- Gunakan hanya data yang tersedia.
- Jangan mengarang angka, penyebab, atau fakta.
- Jelaskan perubahan berdasarkan tahun jika terlihat.
- Bandingkan SMA, MA, dan SMK jika datanya tersedia.
- Jangan menyimpulkan penyebab perubahan berdasarkan grafik saja.
- Jika data tidak cukup, sampaikan keterbatasannya.
- Buat analisis ringkas, informatif, dan mudah dibaca.
- Jangan gunakan Markdown.
- Setiap penjelasan berupa paragraf biasa.

Jelaskan secara terpisah:
1. mengulang: siswa mengulang, perubahan antar tahun, dan perbandingan SMA, MA, SMK.
2. putus_sekolah: siswa putus sekolah, perubahan antar tahun, dan perbandingan SMA, MA, SMK.
3. lulusan: jumlah lulusan, perubahan antar tahun, dan perbandingan SMA, MA, SMK.

BALAS HANYA DENGAN JSON VALID:

{{
    "mengulang": "Penjelasan grafik siswa mengulang",
    "putus_sekolah": "Penjelasan grafik putus sekolah",
    "lulusan": "Penjelasan grafik lulusan"
}}
"""

        result = gemini_service.generate(prompt)
        text = result["text"].strip()

        if text.startswith("```"):
            text = text.replace("```json", "", 1)
            text = text.replace("```", "").strip()

        try:
            explanations = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("AI menghasilkan format JSON yang tidak valid.") from exc

        required_keys = ["mengulang", "putus_sekolah", "lulusan"]

        for key in required_keys:
            if key not in explanations or not isinstance(explanations[key], str):
                raise ValueError(f"Format penjelasan AI tidak valid: {key}")

        return {
            "success": True,
            "explanations": explanations,
            "model": result["model"],
            "elapsed": result["elapsed"],
        }


    @staticmethod
    def explain_prediction(district, prediction_year, chart_data):
        data_context = {
            "kecamatan": district,
            "tahun_prediksi": prediction_year,
            "data_indikator": chart_data,
        }

        prompt = f"""
Kamu adalah AI analis prediksi pendidikan pada website Data Pendidikan.

DATA PREDIKSI:
{json.dumps(data_context, ensure_ascii=False)}

ATURAN:
- Gunakan bahasa Indonesia sederhana, jelas, dan mudah dipahami.
- Analisis hanya data yang diberikan.
- Jangan mengarang angka, penyebab, atau fakta.
- Data aktual dan prediksi harus dibedakan dengan jelas.
- Jelaskan perkembangan indikator dari data aktual menuju tahun prediksi.
- Jelaskan tren dan perubahan nilai.
- Bandingkan SMA, MA, dan SMK jika datanya tersedia.
- Jangan menganggap kenaikan atau penurunan sebagai penyebab kondisi tertentu.
- Sebutkan kecamatan dan tahun prediksi dalam analisis.
- Buat penjelasan informatif, tetapi tidak terlalu panjang.
- Jangan menggunakan Markdown.
- Setiap penjelasan berupa paragraf biasa.

Jelaskan secara terpisah:
1. mengulang: perkembangan siswa mengulang dan interpretasi hasil prediksi.
2. putus_sekolah: perkembangan siswa putus sekolah dan interpretasi hasil prediksi.
3. lulusan: perkembangan angka lulusan dan interpretasi hasil prediksi.

BALAS HANYA DENGAN JSON VALID:

{{
    "mengulang": "Analisis prediksi mengulang",
    "putus_sekolah": "Analisis prediksi putus sekolah",
    "lulusan": "Analisis prediksi lulusan"
}}
"""

        result = gemini_service.generate(prompt)
        text = result["text"].strip()

        if text.startswith("```"):
            text = text.replace("```json", "", 1)
            text = text.replace("```", "").strip()

        try:
            explanations = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("AI menghasilkan format JSON prediksi yang tidak valid.") from exc

        required_keys = ["mengulang", "putus_sekolah", "lulusan"]

        for key in required_keys:
            if key not in explanations or not isinstance(explanations[key], str):
                raise ValueError(f"Format penjelasan prediksi tidak valid: {key}")

        return {
            "success": True,
            "explanations": explanations,
            "model": result["model"],
            "elapsed": result["elapsed"],
        }



ai_interpreter = AIDataInterpreter()
