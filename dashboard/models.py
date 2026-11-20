from django.db import models


class PredictionHistory(models.Model):
    district = models.CharField(max_length=100, verbose_name="Kecamatan")
    prediction_year = models.PositiveIntegerField(verbose_name="Tahun Prediksi")
    data_year = models.PositiveIntegerField(verbose_name="Tahun Data")
    predictions = models.JSONField(verbose_name="Hasil Prediksi")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Waktu Prediksi"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Riwayat Prediksi"
        verbose_name_plural = "Riwayat Prediksi"

    def __str__(self):
        return f"{self.district} - {self.prediction_year}"
