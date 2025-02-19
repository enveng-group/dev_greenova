export class ProjectContent {
    constructor() {
      document.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'project-content') {
        // Initialize any charts or other components
        if (window.chartManager) {
            window.chartManager.initializeCharts();
        }
    }
    });
    }


}