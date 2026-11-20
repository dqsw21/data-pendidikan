document.addEventListener("DOMContentLoaded", function () {
    const panels = {
        mengulang: document.getElementById("ai-mengulang"),
        putus_sekolah: document.getElementById("ai-putus-sekolah"),
        lulusan: document.getElementById("ai-lulusan"),
    };

    function showLoading(panel) {
        if (!panel) return;

        const loading = panel.querySelector(".chart-ai-loading");
        const error = panel.querySelector(".chart-ai-error");
        const result = panel.querySelector(".chart-ai-result");
        const meta = panel.querySelector(".chart-ai-meta");

        if (loading) loading.hidden = false;
        if (error) error.hidden = true;
        if (result) result.hidden = true;
        if (meta) meta.textContent = "";
    }

    function showResult(panel, text, model, cached) {
        if (!panel) return;

        const loading = panel.querySelector(".chart-ai-loading");
        const error = panel.querySelector(".chart-ai-error");
        const result = panel.querySelector(".chart-ai-result");
        const meta = panel.querySelector(".chart-ai-meta");

        if (loading) loading.hidden = true;
        if (error) error.hidden = true;

        if (result) {
            result.textContent = text || "Tidak ada penjelasan tersedia.";
            result.hidden = false;
        }

        if (meta) {
            meta.textContent = `${model || "AI"} • ${cached ? "Cache" : "Analisis baru"}`;
        }
    }

    function showError(panel, message) {
        if (!panel) return;

        const loading = panel.querySelector(".chart-ai-loading");
        const error = panel.querySelector(".chart-ai-error");
        const result = panel.querySelector(".chart-ai-result");
        const meta = panel.querySelector(".chart-ai-meta");

        if (loading) loading.hidden = true;
        if (result) result.hidden = true;

        if (error) {
            error.textContent = message;
            error.hidden = false;
        }

        if (meta) meta.textContent = "";
    }

    Object.values(panels).forEach(showLoading);

    fetch("/dashboard-ai/", {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    })
    .then(function (response) {
        return response.json().then(function (data) {
            if (!response.ok || !data.success) {
                throw new Error(data.error || "Analisis AI gagal.");
            }

            return data;
        });
    })
    .then(function (data) {
        showResult(
            panels.mengulang,
            data.explanations.mengulang,
            data.model,
            data.cached
        );

        showResult(
            panels.putus_sekolah,
            data.explanations.putus_sekolah,
            data.model,
            data.cached
        );

        showResult(
            panels.lulusan,
            data.explanations.lulusan,
            data.model,
            data.cached
        );
    })
    .catch(function (error) {
        const message = error.message || "Gagal menghubungkan ke AI.";

        Object.values(panels).forEach(function (panel) {
            showError(panel, message);
        });
    });
});
