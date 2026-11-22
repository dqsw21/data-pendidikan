document.addEventListener("DOMContentLoaded", function () {
    const dataElement = document.getElementById("prediction-chart-data");

    if (!dataElement || typeof Chart === "undefined") {
        console.error("Prediction chart data atau Chart.js tidak ditemukan.");
        return;
    }

    const data = JSON.parse(dataElement.textContent);
    const labels = data.labels || [];

    const configs = [
        { key: "SMA_lulusan", id: "chartSmaLulusan", color: "#2563eb" },
        { key: "SMA_mengulang", id: "chartSmaMengulang", color: "#0d9488" },
        { key: "SMA_putus", id: "chartSmaPutus", color: "#f59e0b" },
        { key: "SMK_lulusan", id: "chartSmkLulusan", color: "#2563eb" },
        { key: "SMK_mengulang", id: "chartSmkMengulang", color: "#0d9488" },
        { key: "SMK_putus", id: "chartSmkPutus", color: "#f59e0b" },
    ];

    const formatter = new Intl.NumberFormat("id-ID");

    configs.forEach(function (config) {
        const series = data.series[config.key];
        const canvas = document.getElementById(config.id);

        if (!series || !canvas) return;

        const actualCount = series.actual_count || [];
        const actualPercent = series.actual_percent || [];
        const forecastCount = series.forecast_count || [];
        const forecastPercent = series.forecast_percent || [];

        const lastActualIndex = actualCount.reduce(function (lastIndex, value, index) {
            return value !== null && value !== undefined ? index : lastIndex;
        }, -1);

        const forecastPlot = labels.map(function (_, index) {
            if (index === lastActualIndex) {
                return actualCount[index];
            }

            return forecastCount[index] ?? null;
        });

        new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: series.metric + " (Aktual)",
                        data: actualCount,
                        borderColor: config.color,
                        backgroundColor: config.color,
                        borderWidth: 2.5,
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        tension: 0.25,
                        fill: false,
                        spanGaps: false
                    },
                    {
                        label: series.metric + " (Prediksi)",
                        data: forecastPlot,
                        borderColor: config.color,
                        backgroundColor: config.color,
                        borderWidth: 2.5,
                        borderDash: [7, 5],
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        pointStyle: "circle",
                        tension: 0.25,
                        fill: false,
                        spanGaps: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: "nearest",
                    intersect: true
                },
                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                        labels: {
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            title: function (items) {
                                if (!items.length) return "";
                                return "Tahun Ajar: " + labels[items[0].dataIndex];
                            },
                            label: function (context) {
                                const index = context.dataIndex;
                                const isForecast = context.datasetIndex === 1;

                                const count = isForecast
                                    ? forecastCount[index]
                                    : actualCount[index];

                                const percentage = isForecast
                                    ? forecastPercent[index]
                                    : actualPercent[index];

                                const status = isForecast ? "Prediksi" : "Aktual";

                                if (count === null || count === undefined) {
                                    return status + ": Data tidak tersedia";
                                }

                                const combinedPercent = labels.map(function (_, i) {
                                    if (actualPercent[i] !== null && actualPercent[i] !== undefined) {
                                        return actualPercent[i];
                                    }
                                    return forecastPercent[i] ?? null;
                                });

                                const currentPercent = Number(percentage || 0);
                                const previousPercent = index > 0
                                    ? combinedPercent[index - 1]
                                    : null;

                                let changeLabel = "0%";

                                if (previousPercent !== null && previousPercent !== undefined) {
                                    const difference = currentPercent - Number(previousPercent);
                                    const formattedDifference = Math.abs(difference).toLocaleString("id-ID", {
                                        maximumFractionDigits: 2
                                    });

                                    if (difference > 0) {
                                        changeLabel = "▲ +" + formattedDifference + "%";
                                    } else if (difference < 0) {
                                        changeLabel = "▼ -" + formattedDifference + "%";
                                    }
                                }

                                return [
                                    status + ": " + formatter.format(count) + " siswa",
                                    "Persentase: " + currentPercent.toLocaleString("id-ID", {
                                        maximumFractionDigits: 2
                                    }) + "%",
                                    "Perubahan: " + changeLabel
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Tahun Ajar"
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return formatter.format(value);
                            }
                        },
                        title: {
                            display: true,
                            text: "Jumlah Siswa"
                        }
                    }
                }
            }
        });
    });
});
