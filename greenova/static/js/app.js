import { ChartManager } from './modules/chart-manager.js';
import { ChatWidget } from './modules/chat-widget.js';

// Initialize managers
const chartManager = new ChartManager();
const chatWidget = new ChatWidget();

// HTMX Events
htmx.on('htmx:afterRequest', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        const canvas = evt.detail.elt;
        const data = JSON.parse(evt.detail.xhr.response);
        chartManager.init(canvas, data);
    }
    if (evt.detail.failed) {
        console.error('HTMX request failed:', evt.detail.xhr.responseText);
    }
});

htmx.on('htmx:beforeCleanupElement', (evt) => {
    if (evt.detail.elt.tagName === 'CANVAS') {
        chartManager.cleanup(evt.detail.elt.id);
    }
});