// Store chart instances
const chartInstances = new Map();

// Clean up charts when content changes
document.addEventListener('htmx:beforeSwap', function() {
    chartInstances.forEach(chart => chart.destroy());
    chartInstances.clear();
});

// Initialize charts after content loads
document.addEventListener('htmx:afterSettle', function() {
    const canvases = document.querySelectorAll('canvas[data-mechanism]');
    canvases.forEach(initializeChart);
});

function initializeChart(canvas) {
    const mechanism = canvas.dataset.mechanism;
    const projectId = canvas.dataset.project;
    
    if (!mechanism || !projectId) return;

    fetch(`/analytics/mechanism-status/?mechanism=${encodeURIComponent(mechanism)}&project=${projectId}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            // Destroy existing chart if it exists
            if (chartInstances.has(canvas.id)) {
                chartInstances.get(canvas.id).destroy();
            }

            const chart = new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.status_counts,
                        backgroundColor: [
                            '#ff6384',  // Not Started
                            '#36a2eb',  // In Progress
                            '#4bc0c0'   // Completed
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
                                padding: 8
                            }
                        }
                    },
                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            const status = data.labels[elements[0].index].toLowerCase();
                            updateObligationsTable(mechanism, status, projectId);
                        } else {
                            updateObligationsTable(mechanism, '', projectId);
                        }
                    }
                }
            });
            
            chartInstances.set(canvas.id, chart);
        })
        .catch(error => {
            console.error('Error loading chart data:', error);
            canvas.parentElement.innerHTML = `
                <div role="alert">
                    <p>Error loading chart data</p>
                </div>
            `;
        });
}

function updateObligationsTable(mechanism, status, projectId) {
    const filterState = document.getElementById('filter-state');
    if (filterState) {
        filterState.value = mechanism;
        filterState.dataset.status = status;
        htmx.trigger('#obligations-section', 'obligationsUpdate');
    }
}

// Debug logging for HTMX events
htmx.logger = function(elt, event, data) {
    if(console) {
        console.log(event, elt, data);
    }
}