// Chart scrolling functionality
function scrollCharts(direction) {
  const container = document.getElementById('chartScroll');
  if (!container) return;

  const scrollAmount = 320;
  container.scrollBy({
    left: direction === 'left' ? -scrollAmount : scrollAmount,
    behavior: 'smooth'
  });
}

// Initialize chart navigation
document.addEventListener('htmx:afterSettle', function() {
  const chartScroll = document.getElementById('chartScroll');
  if (chartScroll) {
    // Add keyboard navigation
    chartScroll.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        scrollCharts('left');
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        scrollCharts('right');
      }
    });
  }
});

// Add loading indicator
document.addEventListener('htmx:beforeRequest', function(evt) {
  if (evt.detail.target.id === 'chart-container') {
    evt.detail.target.innerHTML = '<div class="notice" role="status" aria-busy="true">Loading charts...</div>';
  }
});

// Add this to your existing app.js
document.addEventListener('htmx:afterRequest', (evt) => {
  if (evt.detail.elt.matches('form[hx-post*="logout"]') && evt.detail.successful) {
    window.location.href = '/';
  }
});
