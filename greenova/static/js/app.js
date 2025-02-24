// HTMX Events
htmx.on('htmx:afterRequest', (evt) => {
    if (evt.detail.successful) {
        document.querySelectorAll('canvas[data-chart-data]').forEach(canvas => {
            chartManager.init(canvas, canvas.dataset.chartData);
        });
    }
});

htmx.on('htmx:beforeCleanupElement', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        chartManager.cleanup(evt.detail.elt.id);
    }
});
