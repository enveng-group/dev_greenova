export class ChartManager {
    #instances = new Map();
    #defaultConfig = {
        type: 'doughnut',
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    };

    async init(canvas, data) {
        try {
            if (!canvas || !data) {
                console.warn('Missing required parameters for chart initialization');
                return null;
            }

            // Clean up existing chart if present
            this.cleanup(canvas.id);

            // Parse data if it's a string
            const chartData = typeof data === 'string' ? JSON.parse(data) : data;

            // Validate chart data
            if (!this.#validateChartData(chartData)) {
                console.error('Invalid chart data structure');
                return null;
            }

            try {
                // Import Chart.js dynamically with proper module syntax
                const { default: Chart } = await import('/static/js/vendor/chart.umd.js');

                // Configure chart with validated data
                const config = {
                    ...this.#defaultConfig,
                    data: {
                        labels: chartData.labels || [],
                        datasets: [{
                            data: chartData.datasets?.[0]?.data || [],
                            backgroundColor: [
                                'var(--error)',
                                'var(--primary)',
                                'var(--success)'
                            ]
                        }]
                    }
                };

                // Create new chart instance
                const chart = new Chart(canvas.getContext('2d'), config);
                
                // Store chart instance
                this.#instances.set(canvas.id, chart);
                
                return chart;
            } catch (chartError) {
                console.error('Failed to load Chart.js:', chartError);
                this.#showFallbackContent(canvas, chartData);
                return null;
            }
        } catch (error) {
            console.error('Chart initialization error:', error);
            this.#showFallbackContent(canvas, data);
            return null;
        }
    }

    cleanup(chartId) {
        try {
            const existingChart = this.#instances.get(chartId);
            if (existingChart) {
                existingChart.destroy();
                this.#instances.delete(chartId);
            }
        } catch (error) {
            console.error('Chart cleanup error:', error);
        }
    }

    #validateChartData(data) {
        return data 
            && (Array.isArray(data.labels) || Array.isArray(data.datasets))
            && (!data.datasets || data.datasets.every(dataset => 
                Array.isArray(dataset.data)));
    }

    #showFallbackContent(canvas, data) {
        const container = canvas.parentElement;
        if (container) {
            // Hide the canvas
            canvas.style.display = 'none';
            
            // Create fallback content
            const fallback = document.createElement('div');
            fallback.setAttribute('role', 'alert');
            fallback.innerHTML = `
                <p>Unable to load chart visualization.</p>
                <details>
                    <summary>View Data</summary>
                    <table role="grid">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this.#createTableRows(data)}
                        </tbody>
                    </table>
                </details>
            `;
            container.appendChild(fallback);
        }
    }

    #createTableRows(data) {
        try {
            const labels = data.labels || [];
            const values = data.datasets?.[0]?.data || [];
            return labels.map((label, index) => `
                <tr>
                    <td>${label}</td>
                    <td>${values[index] || 0}</td>
                </tr>
            `).join('');
        } catch (error) {
            return '<tr><td colspan="2">Error displaying data</td></tr>';
        }
    }

    getChartInstance(chartId) {
        return this.#instances.get(chartId) || null;
    }
}