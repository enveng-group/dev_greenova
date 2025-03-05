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
