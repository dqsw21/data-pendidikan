import os
import logging
import time

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


MODEL_CHAIN = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
]


class AIServiceError(Exception):
    """Error ketika seluruh model AI gagal digunakan."""
    pass


class GeminiAIService:
    def __init__(self):
        self.timeout = 30

    def generate(self, prompt):
        errors = []

        available_keys = [
            (index + 1, key)
            for index, key in enumerate(API_KEYS)
            if key and key.strip()
        ]

        if not available_keys:
            raise AIServiceError("API Key Gemini belum dikonfigurasi.")

        for model_name in MODEL_CHAIN:
            for key_number, api_key in available_keys:
                start_time = time.time()

                try:
                    client = genai.Client(
                        api_key=api_key,
                        http_options=types.HttpOptions(
                            timeout=self.timeout * 1000
                        ),
                    )

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.3,
                            max_output_tokens=1000,
                        ),
                    )

                    text = getattr(response, "text", None)

                    if not text or not text.strip():
                        raise AIServiceError("Respons AI kosong.")

                    elapsed = round(time.time() - start_time, 2)

                    logger.info(
                        "Gemini berhasil | model=%s | key=%s | waktu=%ss",
                        model_name,
                        key_number,
                        elapsed,
                    )

                    return {
                        "success": True,
                        "text": text.strip(),
                        "model": model_name,
                        "key_slot": key_number,
                        "elapsed": elapsed,
                    }

                except Exception as error:
                    elapsed = round(time.time() - start_time, 2)

                    logger.warning(
                        "Gemini gagal | model=%s | key=%s | "
                        "error=%s | waktu=%ss",
                        model_name,
                        key_number,
                        type(error).__name__,
                        elapsed,
                    )

                    errors.append({
                        "model": model_name,
                        "key": key_number,
                        "error": type(error).__name__,
                    })

        raise AIServiceError(
            "Seluruh model Gemini gagal memberikan respons."
        )


gemini_service = GeminiAIService()
