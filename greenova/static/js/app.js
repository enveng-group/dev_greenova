import { chartManager } from './modules/chart_manager.js';

document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    setupEventListeners();
});

function initializeCharts() {
    document.querySelectorAll('canvas[data-chart-data]').forEach(canvas => {
        const chartData = canvas.dataset.chartData;
        if (chartData) {
            canvas.previousElementSibling?.setAttribute('aria-busy', 'true');
            chartManager.init(canvas, chartData);
            canvas.previousElementSibling?.removeAttribute('aria-busy');
        }
    });
}

function setupEventListeners() {
    // Handle window resize
    window.addEventListener('resize', () => {
        document.querySelectorAll('canvas[data-chart-data]').forEach(canvas => {
            chartManager.resizeChart(canvas.id);
        });
    });

    // Clean up charts before removal
    window.addEventListener('beforeunload', () => {
        document.querySelectorAll('canvas[data-chart-data]').forEach(canvas => {
            chartManager.cleanup(canvas.id);
        });
    });
}

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
