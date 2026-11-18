const chartData = JSON.parse(
    document.getElementById("chart-data").textContent
);

function createChart(elementId, data, title) {
    const element = document.getElementById(elementId);

    new Chart(element, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: data.datasets.map((dataset) => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: {
                    SMA: "#2563eb",
                    MA: "#0d9488",
                    SMK: "#f59e0b"
                }[dataset.label],
                borderRadius: 5,
                maxBarThickness: 45
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom"
                },
                title: {
                    display: false,
                    text: title
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ": " +
                                context.parsed.y.toFixed(2) + "%";
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Persentase (%)"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Tahun"
                    }
                }
            }
        }
    });
}

createChart("chartMengulang", chartData.mengulang, "Angka Mengulang");
createChart("chartPutusSekolah", chartData.putus_sekolah, "Angka Putus Sekolah");
createChart("chartLulusan", chartData.lulusan, "Angka Lulusan");
