// HTMX Events
htmx.on('htmx:afterRequest', (evt) => {
    if (evt.detail.successful) {
        // Initialize charts after content loaded
        document.querySelectorAll('canvas[data-chart]').forEach(canvas => {
            const chartData = canvas.dataset.chart;
            if (chartData) {
                chartManager.init(canvas, chartData);
            }
        });

    }
});

htmx.on('htmx:beforeCleanupElement', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        chartManager.cleanup(evt.detail.elt.id);
    }
});
