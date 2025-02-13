export class ChartManager {
    #instances = new Map();

    async init(canvas, data) {
        try {
            this.cleanup(canvas.id);

            // Lazy load Chart.js
            const Chart = (await import('/static/js/chart.umd.js')).default;

            const chart = new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: [
                            'var(--error)',
                            'var(--primary)',
                            'var(--success)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { 
                                boxWidth: 12,
                                padding: 8,
                                color: 'var(--contrast)'
                            }
                        }
                    }
                }
            });

            this.#instances.set(canvas.id, chart);
            return chart;
        } catch (error) {
            console.error('Chart initialization error:', error);
            return null;
        }
    }

    cleanup(chartId) {
        if (this.#instances.has(chartId)) {
            this.#instances.get(chartId).destroy();
            this.#instances.delete(chartId);
        }
    }
}