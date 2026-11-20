document.addEventListener("DOMContentLoaded", function () {
    const districtElement = document.getElementById("kecamatan");
    const yearElement = document.getElementById("tahun");

    if (!districtElement || !yearElement) return;

    const panels = {
        mengulang: "ai-prediction-mengulang",
        putus_sekolah: "ai-prediction-putus",
        lulusan: "ai-prediction-lulusan"
    };

    function showLoading(panel) {
        panel.querySelector(".prediction-ai-loading").hidden = false;
        panel.querySelector(".prediction-ai-error").hidden = true;
        panel.querySelector(".prediction-ai-result").hidden = true;
        panel.querySelector(".prediction-ai-meta").textContent = "";
    }

    function showResult(panel, text, metadata) {
        panel.querySelector(".prediction-ai-loading").hidden = true;

        const resultElement = panel.querySelector(".prediction-ai-result");
        resultElement.textContent = text;
        resultElement.hidden = false;

        panel.querySelector(".prediction-ai-error").hidden = true;

        panel.querySelector(".prediction-ai-meta").textContent = metadata;
    }

    function showError(panel, message) {
        panel.querySelector(".prediction-ai-loading").hidden = true;

        const errorElement = panel.querySelector(".prediction-ai-error");
        errorElement.textContent = message;
        errorElement.hidden = false;

        panel.querySelector(".prediction-ai-result").hidden = true;
        panel.querySelector(".prediction-ai-meta").textContent = "";
    }

    async function loadPredictionAI() {
        const district = districtElement.value;
        const year = yearElement.value;

        Object.values(panels).forEach(panelId => {
            const panel = document.getElementById(panelId);
            if (panel) showLoading(panel);
        });

        const params = new URLSearchParams({
            kecamatan: district,
            tahun: year
        });

        try {
            const response = await fetch(
                `/prediction-ai/?${params.toString()}`
            );

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.error || "Analisis AI gagal dimuat."
                );
            }

            const metadata =
                `Kecamatan ${data.district} • Tahun ${data.prediction_year}` +
                ` • Model ${data.model}` +
                ` • ${Number(data.elapsed).toFixed(2)} detik` +
                (data.cached ? " • Cache" : "");

            Object.entries(panels).forEach(([key, panelId]) => {
                const panel = document.getElementById(panelId);
                if (!panel) return;

                const explanation = data.explanations[key];

                if (explanation) {
                    showResult(panel, explanation, metadata);
                } else {
                    showError(panel, "Penjelasan AI untuk indikator ini tidak tersedia.");
                }
            });

        } catch (error) {
            Object.values(panels).forEach(panelId => {
                const panel = document.getElementById(panelId);
                if (panel) {
                    showError(
                        panel,
                        error.message || "Gagal memuat analisis AI."
                    );
                }
            });

            console.error("Prediction AI Error:", error);
        }
    }

    loadPredictionAI();
});
