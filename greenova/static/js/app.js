// Import only what's needed
import { ChartManager } from './modules/chart-manager.js';

// Initialize chart manager
const chartManager = new ChartManager();

// HTMX Events
htmx.on('htmx:afterRequest', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        const canvas = evt.detail.elt;
        const data = JSON.parse(evt.detail.xhr.response);
        chartManager.init(canvas, data);
    }
});

htmx.on('htmx:beforeCleanupElement', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        chartManager.cleanup(evt.detail.elt.id);
    }
});