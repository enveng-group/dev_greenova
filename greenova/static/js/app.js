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

/*!
 * Minimal theme switcher
 *
 * Pico.css - https://picocss.com
 * Copyright 2019-2024 - Licensed under MIT
 */

const themeSwitcher = {
  // Config
  _scheme: "auto",
  menuTarget: "details.dropdown",
  buttonsTarget: "a[data-theme-switcher]",
  buttonAttribute: "data-theme-switcher",
  rootAttribute: "data-theme",
  localStorageKey: "picoPreferredColorScheme",

  // Init
  init() {
    this.scheme = this.schemeFromLocalStorage;
    this.initSwitchers();
  },

  // Get color scheme from local storage
  get schemeFromLocalStorage() {
    return window.localStorage?.getItem(this.localStorageKey) ?? this._scheme;
  },

  // Preferred color scheme
  get preferredColorScheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  },

  // Init switchers
  initSwitchers() {
    const buttons = document.querySelectorAll(this.buttonsTarget);
    buttons.forEach((button) => {
      button.addEventListener(
        "click",
        (event) => {
          event.preventDefault();
          // Set scheme
          this.scheme = button.getAttribute(this.buttonAttribute);
          // Close dropdown
          document.querySelector(this.menuTarget)?.removeAttribute("open");
        },
        false
      );
    });
  },

  // Set scheme
  set scheme(scheme) {
    if (scheme == "auto") {
      this._scheme = this.preferredColorScheme;
    } else if (scheme == "dark" || scheme == "light") {
      this._scheme = scheme;
    }
    this.applyScheme();
    this.schemeToLocalStorage();
  },

  // Get scheme
  get scheme() {
    return this._scheme;
  },

  // Apply scheme
  applyScheme() {
    document.querySelector("html")?.setAttribute(this.rootAttribute, this.scheme);
  },

  // Store scheme to local storage
  schemeToLocalStorage() {
    window.localStorage?.setItem(this.localStorageKey, this.scheme);
  },
};

// Init
themeSwitcher.init();

// Project selection handler
document.addEventListener('change', function(e) {
  if (e.target.matches('#project-select')) {
    // Trigger updates for both containers
    htmx.trigger('#chart-container', 'refreshCharts');
    htmx.trigger('#obligations-container', 'refreshObligations');
  }
});

// Loading states
document.addEventListener('htmx:beforeRequest', function(evt) {
  const target = evt.detail.target;
  if (target.matches('#obligations-container, #chart-container')) {
    target.innerHTML = '<div class="notice" role="status" aria-busy="true">Loading...</div>';
  }
});

// Error handling
document.addEventListener('htmx:responseError', function(evt) {
  const target = evt.detail.target;
  target.innerHTML = `
    <div class="notice error" role="alert">
      <p>Error loading data. Please try again.</p>
    </div>
  `;
});

// Handle table scrolling
document.addEventListener('htmx:afterSettle', function() {
  const tableContainer = document.querySelector('.horizontal-scroll');
  const scrollThumb = document.querySelector('.scroll-thumb');

  if (tableContainer && scrollThumb) {
    // Update scroll indicator
    const updateScrollIndicator = () => {
      const scrollWidth = tableContainer.scrollWidth;
      const viewportWidth = tableContainer.clientWidth;
      const scrollLeft = tableContainer.scrollLeft;

      // Calculate thumb width and position
      const thumbWidth = (viewportWidth / scrollWidth) * 100;
      const thumbPosition = (scrollLeft / (scrollWidth - viewportWidth)) * (100 - thumbWidth);

      // Update thumb style
      scrollThumb.style.width = `${thumbWidth}%`;
      scrollThumb.style.marginLeft = `${thumbPosition}%`;
    };

    // Initial update
    updateScrollIndicator();

    // Update on scroll
    tableContainer.addEventListener('scroll', updateScrollIndicator);

    // Make top scroll indicator interactive
    const scrollIndicator = document.getElementById('scroll-indicator');
    scrollIndicator.addEventListener('click', (e) => {
      const rect = scrollIndicator.getBoundingClientRect();
      const ratio = (e.clientX - rect.left) / rect.width;
      const maxScroll = tableContainer.scrollWidth - tableContainer.clientWidth;
      tableContainer.scrollLeft = maxScroll * ratio;
    });
  }
});

// Filter form submission handler
document.addEventListener('submit', function(e) {
  if (e.target.matches('#obligations-filter-form')) {
    // The form will be handled by HTMX, this is just for additional functionality
    e.preventDefault();

    // Update any UI elements related to filtering
    const filterCount = document.getElementById('filter-count');
    if (filterCount) {
      const activeFilters = Array.from(e.target.querySelectorAll('select, input[type="text"]'))
        .filter(el => el.value && el.value !== '')
        .length;
      filterCount.textContent = activeFilters;
      filterCount.hidden = activeFilters === 0;
    }
  }
});

// Print handler
document.addEventListener('click', function(e) {
  if (e.target.matches('#print-obligations')) {
    e.preventDefault();
    window.print();
  }
});

// Export handler
document.addEventListener('click', function(e) {
  if (e.target.matches('#export-obligations')) {
    const table = document.querySelector('table');
    if (!table) return;

    // Function to download CSV
    const exportToCSV = (filename) => {
      // Extract headers
      const rows = Array.from(table.querySelectorAll('tr'));
      const headers = Array.from(rows[0].querySelectorAll('th'))
        .map(cell => `"${cell.textContent.trim().replace(/"/g, '""')}"`);

      // Extract data rows
      const data = rows.slice(1).map(row => {
        return Array.from(row.querySelectorAll('td'))
          .map(cell => `"${cell.textContent.trim().replace(/"/g, '""')}"`);
      });

      // Combine headers and data
      const csvContent = [
        headers.join(','),
        ...data.map(row => row.join(','))
      ].join('\n');

      // Create download link
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');

      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      link.style.display = 'none';

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    exportToCSV('obligations_export.csv');
  }
});

// Function to remove filter
function removeFilter(type, value) {
  const select = document.querySelector(`select[name="${type}"]`);
  if (select) {
    Array.from(select.options).forEach(option => {
      if (option.value === value) {
        option.selected = false;
      }
    });
    select.dispatchEvent(new Event('change'));
  }
}

// Update the Add Obligation button to include the current project_id
document.addEventListener('DOMContentLoaded', function() {
  function updateAddObligationButton() {
    const projectSelect = document.getElementById('project-select');
    const addObligationBtn = document.querySelector('.add-obligation-btn');

    if (projectSelect && addObligationBtn) {
      const projectId = projectSelect.value;
      if (projectId) {
        const currentHref = addObligationBtn.getAttribute('href');
        const baseUrl = currentHref.split('?')[0];
        addObligationBtn.setAttribute('href', `${baseUrl}?project_id=${projectId}`);
      }
    }
  }

  // Initial update
  updateAddObligationButton();

  // Update when project selection changes
  document.addEventListener('change', function(e) {
    if (e.target.matches('#project-select')) {
      updateAddObligationButton();
    }
  });
});

// Handle obligation link clicks to show loading state
document.addEventListener('click', function(e) {
  if (e.target.matches('.obligation-link') || e.target.closest('.obligation-link')) {
    // Show loading indicator
    document.body.classList.add('loading');

    // Store the current project ID in session storage so we can return to it
    const projectId = document.querySelector('input[name="project_id"]')?.value;
    if (projectId) {
      sessionStorage.setItem('lastProjectId', projectId);
    }
  }
});

// Restore project selection when returning from obligation edit
document.addEventListener('DOMContentLoaded', function() {
  const projectSelect = document.getElementById('project-select');
  const lastProjectId = sessionStorage.getItem('lastProjectId');

  if (projectSelect && lastProjectId) {
    projectSelect.value = lastProjectId;
    // Trigger change event if needed by your implementation
    projectSelect.dispatchEvent(new Event('change'));
  }
});

document.addEventListener('htmx:afterSettle', function(evt) {
  if (evt.detail.triggerSpec && evt.detail.triggerSpec.includes('obligation:statusChanged')) {
    htmx.trigger('#chart-container', 'refreshCharts');
    // Refresh mechanism charts or other affected components
  }
});

/**
 * Main application JavaScript functionality
 */

document.addEventListener('DOMContentLoaded', function() {
  /**
   * Theme switching functionality
   * Uses the head-support extension to dynamically update theme
   */
  const themeSwitchers = document.querySelectorAll('[data-theme-switcher]');
  const currentTheme = localStorage.getItem('theme') || 'auto';

  // Apply the saved theme on page load
  setTheme(currentTheme);

  themeSwitchers.forEach(switcher => {
    const theme = switcher.getAttribute('data-theme-switcher');

    // Highlight active theme
    if (theme === currentTheme) {
      switcher.setAttribute('aria-current', 'true');
    }

    switcher.addEventListener('click', function(event) {
      event.preventDefault();

      // Update localStorage
      localStorage.setItem('theme', theme);

      // Apply the theme
      setTheme(theme);

      // Update active state on links
      themeSwitchers.forEach(s => {
        s.removeAttribute('aria-current');
      });
      switcher.setAttribute('aria-current', 'true');

      // Trigger a custom event for other components to react
      document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    });
  });

  /**
   * Sets the theme attribute on the document
   * @param {string} theme - The theme to apply ('light', 'dark', or 'auto')
   */
  function setTheme(theme) {
    if (theme === 'auto') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', theme);
    }
  }

  /**
   * Handle table scrolling indicators
   */
  const tableContainers = document.querySelectorAll('.table-container');

  tableContainers.forEach(container => {
    const scrollIndicator = document.createElement('div');
    scrollIndicator.className = 'scroll-indicator';

    const scrollThumb = document.createElement('div');
    scrollThumb.className = 'scroll-thumb';
    scrollIndicator.appendChild(scrollThumb);

    container.appendChild(scrollIndicator);

    container.addEventListener('scroll', function() {
      const scrollPercentage = container.scrollLeft / (container.scrollWidth - container.clientWidth);
      const thumbPosition = scrollPercentage * (scrollIndicator.clientWidth - scrollThumb.clientWidth);
      scrollThumb.style.transform = `translateX(${thumbPosition}px)`;
    });
  });
});

/**
 * Handle HTMX events
 */
document.addEventListener('htmx:afterSwap', function(event) {
  // Reinitialize components that may have been added via HTMX
  const tableContainers = event.detail.target.querySelectorAll('.table-container');

  tableContainers.forEach(container => {
    if (!container.querySelector('.scroll-indicator')) {
      const scrollIndicator = document.createElement('div');
      scrollIndicator.className = 'scroll-indicator';

      const scrollThumb = document.createElement('div');
      scrollThumb.className = 'scroll-thumb';
      scrollIndicator.appendChild(scrollThumb);

      container.appendChild(scrollIndicator);

      container.addEventListener('scroll', function() {
        const scrollPercentage = container.scrollLeft / (container.scrollWidth - container.clientWidth);
        const thumbPosition = scrollPercentage * (scrollIndicator.clientWidth - scrollThumb.clientWidth);
        scrollThumb.style.transform = `translateX(${thumbPosition}px)`;
      });
    }
  });
});

/**
 * Example of using head-support extension to dynamically load stylesheets
 * This function can be used to load CSS files on-demand
 * @param {string} href - The URL of the stylesheet
 * @param {string} id - Unique identifier for the stylesheet
 */
function loadStylesheet(href, id) {
  // Create a new head element
  const headElement = document.createElement('head');
  headElement.setAttribute('hx-head', 'merge');

  // Create link element
  const linkElement = document.createElement('link');
  linkElement.setAttribute('rel', 'stylesheet');
  linkElement.setAttribute('href', href);
  if (id) {
    linkElement.setAttribute('id', id);
  }

  // Add to the head element
  headElement.appendChild(linkElement);

  // Create a div to hold the head
  const container = document.createElement('div');
  container.appendChild(headElement);

  // Process the head using htmx head-support
  htmx.process(container);
}

/**
 * Utility function to create head elements that can be used in htmx responses
 * @param {string} title - Page title
 * @param {Array} styles - Array of stylesheet URLs to include
 * @returns {string} HTML string with head tag
 */
function createHeadFragment(title, styles = []) {
  let head = '<head hx-head="merge">';

  if (title) {
    head += `<title>${title}</title>`;
  }

  styles.forEach(style => {
    head += `<link rel="stylesheet" href="${style}" hx-head="re-eval">`;
  });

  head += '</head>';
  return head;
}

/**
 * Main application JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize the application
  initializeApp();
});

/**
 * Initialize application components
 */
function initializeApp() {
  // Set up scroll listeners for tables
  setupTableScroll();

  // Listen for HTMX events
  setupHtmxListeners();
}

/**
 * Set up horizontal scroll handling for data tables
 */
function setupTableScroll() {
  document.querySelectorAll('.table-container').forEach(container => {
    const scrollArea = container.querySelector('.horizontal-scroll');
    const thumb = container.querySelector('.scroll-thumb');

    if (scrollArea && thumb) {
      scrollArea.addEventListener('scroll', () => {
        const scrollPercentage = (scrollArea.scrollLeft /
          (scrollArea.scrollWidth - scrollArea.clientWidth)) * 100;

        thumb.style.width = scrollArea.clientWidth / scrollArea.scrollWidth * 100 + '%';
        thumb.style.marginLeft = scrollPercentage + '%';
      });
    }
  });
}

/**
 * Set up listeners for HTMX events
 */
function setupHtmxListeners() {
  // Handle loading indicator state
  document.body.addEventListener('htmx:beforeRequest', function(evt) {
    const target = evt.detail.target;
    target.classList.add('htmx-request-in-flight');
  });

  document.body.addEventListener('htmx:afterRequest', function(evt) {
    const target = evt.detail.target;
    target.classList.remove('htmx-request-in-flight');
  });

  // Handle errors
  document.body.addEventListener('htmx:responseError', function(evt) {
    console.error('HTMX request failed:', evt.detail.error);
  });

  // Handle chart scrolling
  document.addEventListener('chartsLoaded', function() {
    setupChartNavigation();
  });
}

/**
 * Handle chart navigation with scroll buttons
 */
function scrollCharts(direction) {
  const container = document.getElementById('chartScroll');
  if (!container) return;

  const scrollAmount = container.clientWidth * 0.8;
  const targetPosition = direction === 'left'
    ? container.scrollLeft - scrollAmount
    : container.scrollLeft + scrollAmount;

  container.scrollTo({
    left: targetPosition,
    behavior: 'smooth'
  });
}

/**
 * Set up chart navigation buttons
 */
function setupChartNavigation() {
  const container = document.getElementById('chartScroll');
  if (!container) return;

  // Show/hide navigation buttons based on scroll position
  container.addEventListener('scroll', () => {
    const atStart = container.scrollLeft <= 10;
    const atEnd = container.scrollLeft >= (container.scrollWidth - container.clientWidth - 10);

    // Could update button visibility here if needed
  });
}

// Initialize HTMX extensions
document.addEventListener('DOMContentLoaded', function() {
  // Register HTMX extensions
  htmx.defineExtension('class-tools', window.htmxClassToolsExtension);

  // Setup scroll handling for chart scrolling
  window.scrollCharts = function(direction) {
    const container = document.getElementById('chartScroll');
    if (!container) return;

    const scrollAmount = container.clientWidth * 0.8;
    container.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });
  };

  // Setup flash messages with auto-dismiss
  const flashMessages = document.querySelectorAll('.message[data-auto-dismiss]');
  flashMessages.forEach(message => {
    setTimeout(() => {
      message.setAttribute('classes', 'add fade-out:0s, remove message:1s');
    }, 5000); // 5 second delay before starting fade-out
  });
});

// Setup global event listeners for htmx events
document.body.addEventListener('htmx:afterSwap', function(event) {
  // Add entrance animations to newly swapped content
  if (event.detail.target.hasAttribute('data-animate-entrance')) {
    event.detail.target.setAttribute('classes', 'add fade-in');
  }
});

// Overdue count handler
document.body.addEventListener('highOverdueCount', function(event) {
  const overdueElement = document.querySelector('.stat-card.overdue');
  if (overdueElement && event.detail.count > 5) {
    overdueElement.setAttribute('classes', 'add pulse-animation');
  }
});

/**
 * Path-Deps extension integration
 */
document.addEventListener('DOMContentLoaded', function() {
  // Listen for obligation changes to refresh related components
  document.body.addEventListener('htmx:afterRequest', function(evt) {
    // Only handle successful POST/PUT/DELETE requests (mutations)
    if (!evt.detail.successful || evt.detail.xhr.method === 'GET') return;

    const path = evt.detail.requestConfig.path;

    // Handle obligation path changes
    if (path && path.includes('/obligations/')) {
      // Manually refresh charts and lists that depend on obligations
      if (PathDeps) {
        PathDeps.refresh('/obligations/');
        PathDeps.refresh('/mechanisms/charts/');
        PathDeps.refresh('/dashboard/overdue-count/');
      }
    }
  });
});

// Helper function to refresh specific components
function refreshDependentComponents(path) {
  if (window.PathDeps) {
    PathDeps.refresh(path);
  }
}

// Make sure you're not redefining HTMX extensions - only use them

// Check if htmx is loaded before trying to use it
document.addEventListener('DOMContentLoaded', function() {
    if (typeof htmx !== 'undefined') {
        // Your htmx-dependent code here
    } else {
        console.error('HTMX not loaded');
    }
});
