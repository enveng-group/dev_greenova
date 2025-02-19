import { ChartManager } from './modules/chart-manager.js';
import { ProjectSelect } from './modules/project-select.js';
import { ProjectContent } from './modules/project-content.js';

// Initialize managers
const chartManager = new ChartManager();
const projectSelect = new ProjectSelect();
const projectContent = new ProjectContent();

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
    } else {
        console.error('HTMX request failed:', evt.detail.xhr.responseText);
    }
});

htmx.on('htmx:beforeCleanupElement', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        chartManager.cleanup(evt.detail.elt.id);
    }
});