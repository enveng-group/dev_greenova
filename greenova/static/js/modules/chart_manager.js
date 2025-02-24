class ChartManager {
    constructor() {
        this.charts = new Map();
        this.defaultConfig = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        };
    }

    init(canvas, data) {
        if (!canvas || !data) {
            console.error('Missing canvas or data for chart initialization');
            return null;
        }

        try {
            // Parse data if it's a string
            const config = typeof data === 'string' ? JSON.parse(data) : data;

            // Merge default config
            config.options = {
                ...this.defaultConfig,
                ...config.options
            };

            // Create new chart
            const chart = new Chart(canvas, config);
            this.charts.set(canvas.id, chart);

            return chart;
        } catch (error) {
            console.error('Chart initialization failed:', error);
            return null;
        }
    }

    cleanup(canvasId) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.destroy();
            this.charts.delete(canvasId);
        }
    }

    resizeChart(canvasId) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.resize();
        }
    }
}

// Export singleton instance
export const chartManager = new ChartManager();
