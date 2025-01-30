// Modern module imports
import { ChartConfig } from './chart-config.js';

// Feature detection utility
const supports = {
  touch: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
  keyboard: matchMedia('(pointer: fine)').matches,
  reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
  hover: matchMedia('(hover: hover)').matches,
  viewTransitions: 'startViewTransition' in document,
  containerQueries: CSS.supports('container-type: inline-size')
};

// Progressive enhancement for desktop interactions
class ProgressiveInteractions {
  constructor() {
    this.setupKeyboardNavigation();
    this.setupDesktopEnhancements();
    this.setupTouchEnhancements();
  }

  setupKeyboardNavigation() {
    if (supports.keyboard) {
      // Enhanced keyboard navigation
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          modalHandler.closeAll();
        }
        // Add more keyboard shortcuts for desktop
      });
    }
  }

  setupDesktopEnhancements() {
    if (supports.hover) {
      // Add tooltips and hover states
      document.querySelectorAll('[data-tooltip]').forEach(el => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = el.dataset.tooltip;
        el.appendChild(tooltip);
      });
    }
  }

  setupTouchEnhancements() {
    if (supports.touch) {
      // Already have touch handling in ObligationList
      // Add any additional touch-specific enhancements
    }
  }
}

// Progressive chart initialization
class ProgressiveCharts {
  constructor() {
    this.setupChartResponsiveness();
  }

  setupChartResponsiveness() {
    if ('ResizeObserver' in window) {
      const ro = new ResizeObserver(entries => {
        entries.forEach(entry => {
          const chart = entry.target.chart;
          if (chart) {
            // Adjust chart options based on container size
            const width = entry.contentRect.width;
            chart.options.responsive = true;
            chart.options.maintainAspectRatio = width > 600;
            chart.resize();
          }
        });
      });

      document.querySelectorAll('[data-chart]').forEach(el => {
        ro.observe(el);
      });
    }
  }
}

// Enhanced modal handling
class ProgressiveModal extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.setupModal();
  }

  setupModal() {
    // Base mobile setup
    this.setupMobileView();

    // Progressive desktop enhancements
    if (supports.keyboard) {
      this.setupKeyboardInteractions();
    }

    if (supports.viewTransitions) {
      this.setupViewTransitions();
    }
  }

  // ...existing modal methods...
}

// Web Component for obligation cards
class ObligationCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          container-type: inline-size;
        }
        /* ...existing styles... */
      </style>
      <div class="card">
        <slot></slot>
      </div>
    `;
  }
}

customElements.define('obligation-card', ObligationCard);

// Modern lazy loading with native loading="lazy"
const lazyInit = () => {
  document.querySelectorAll('img:not([loading])').forEach(img => {
    img.loading = 'lazy';
    img.decoding = 'async';
  });
};

// Modern Intersection Observer with options
const createObserver = (options = {}) => {
  return new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = entry.target;
        if (target.dataset.src) {
          target.src = target.dataset.src;
          observer.unobserve(target);
        }
      }
    });
  }, {
    rootMargin: '50px',
    threshold: 0.1,
    ...options
  });
};

// Modern chart initialization with ResizeObserver
const initializeChart = (element, config) => {
  if (!element) return null;
  
  const chart = new Chart(element.getContext('2d', { alpha: false }), config);
  
  const resizeObserver = new ResizeObserver(entries => {
    for (const entry of entries) {
      chart.resize();
    }
  });
  
  resizeObserver.observe(element.parentElement);
  return chart;
};

// Modern HTMX event handling with optional chaining
document.body.addEventListener('htmx:configRequest', (event) => {
  const token = document?.querySelector('[name=csrfmiddlewaretoken]')?.value;
  if (token) {
    event.detail.headers['X-CSRFToken'] = token;
  }
});

// Modern modal handling with View Transitions API
const modalHandler = {
  async open(modalId) {
    if (!document.startViewTransition) {
      document.getElementById(modalId)?.showModal();
      return;
    }

    await document.startViewTransition(async () => {
      document.getElementById(modalId)?.showModal();
    }).finished;
  },

  async close(modalId) {
    if (!document.startViewTransition) {
      document.getElementById(modalId)?.close();
      return;
    }

    await document.startViewTransition(async () => {
      document.getElementById(modalId)?.close();
    }).finished;
  }
};

// Modern obligation details fetching
const showObligationDetails = async (obligationNumber) => {
  try {
    const response = await fetch(`/obligations/${obligationNumber}/`);
    if (!response.ok) throw new Error('Failed to fetch obligation details');
    
    const html = await response.text();
    const details = document.getElementById('obligationDetails');
    if (details) {
      details.innerHTML = html;
      await modalHandler.open('obligationModal');
    }
  } catch (error) {
    console.error('Error fetching obligation details:', error);
  }
};

// Modern timeline updates with structured clone
const updateTimeline = (period) => {
  const timelineChart = document.getElementById('timelineChart');
  if (!timelineChart?.dataset.chartData) return;

  const timelineData = structuredClone(
    JSON.parse(timelineChart.dataset.chartData)
  );
  
  // ...existing timeline update code...
};

// Modern touch-enabled obligation list
class ObligationList {
  #currentObligations = [];
  #touchStartX = 0;
  #touchEndX = 0;

  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.#addEventListeners();
  }

  #addEventListeners() {
    this.container?.addEventListener('touchstart', e => {
      this.#touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    this.container?.addEventListener('touchend', e => {
      this.#touchEndX = e.changedTouches[0].screenX;
      this.#handleSwipe();
    }, { passive: true });
  }

  #handleSwipe() {
    const SWIPE_THRESHOLD = 50;
    const delta = this.#touchEndX - this.#touchStartX;
    
    if (Math.abs(delta) > SWIPE_THRESHOLD) {
      delta > 0 ? this.previousPage() : this.nextPage();
    }
  }

  // ...existing obligations list methods...
}

// Modern form validation
const setupFormValidation = () => {
  const forms = document.querySelectorAll('form[data-validate]');
  
  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      
      try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
          method: form.method,
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });
        
        if (!response.ok) throw new Error('Form submission failed');
        
        // Handle success
      } catch (error) {
        console.error('Form submission error:', error);
      }
    });
  });
};

// Modern initialization with feature detection
const init = async () => {
  if (!window.requestAnimationFrame) return;

  // Initialize features progressively
  lazyInit();
  
  if ('IntersectionObserver' in window) {
    const observer = createObserver();
    document.querySelectorAll('[data-src]').forEach(el => observer.observe(el));
  }

  if ('ResizeObserver' in window) {
    // Initialize charts
    initializeLazyCharts();
  }

  if ('ValidityState' in window) {
    setupFormValidation();
  }
};

// Modern event listener with options
document.addEventListener('DOMContentLoaded', init, { 
  once: true,
  passive: true 
});

// Initialize with progressive enhancement
const initProgressive = async () => {
  // Base initialization
  if (!window.requestAnimationFrame) return;

  // Feature-dependent initialization
  new ProgressiveInteractions();
  new ProgressiveCharts();

  // Register components
  customElements.define('progressive-modal', ProgressiveModal);
  customElements.define('obligation-card', ObligationCard);

  // Initialize based on viewport
  const mediaQuery = window.matchMedia('(min-width: 48em)');
  const handleViewportChange = (e) => {
    if (e.matches) {
      // Desktop view optimizations
      initializeDesktopFeatures();
    } else {
      // Mobile view optimizations
      initializeMobileFeatures();
    }
  };

  mediaQuery.addListener(handleViewportChange);
  handleViewportChange(mediaQuery);
};

// Start initialization
document.addEventListener('DOMContentLoaded', initProgressive, { 
  once: true,
  passive: true 
});

// Export for module usage
export { 
  ObligationCard,
  modalHandler,
  showObligationDetails,
  ObligationList
};