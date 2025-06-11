/**
 * Greenova Main Application JavaScript
 *
 * This file follows a progressive enhancement approach:
 * 1. Core functionality works without JavaScript
 * 2. Uses hyperscript for simple interactions
 * 3. Uses htmx for AJAX interactions
 * 4. Uses vanilla JS only when necessary
 */

(function () {
  'use strict';

  // Application modules
  const MODULES = {
    /**
     * Core initialization and utilities
     */
    core: {
      init() {
        // Initialize only if browser supports essential features
        if (!document.querySelector || !window.addEventListener) {
          console.warn('Browser unsupported, skipping JS initialization');
          return;
        }

        // Verify htmx is loaded
        if (typeof htmx === 'undefined') {
          console.warn('HTMX not loaded');
        } else {
          console.log('HTMX loaded successfully');
        }

        // Initialize app modules
        Object.keys(MODULES).forEach((module) => {
          if (
            module !== 'core' &&
            typeof MODULES[module].init === 'function'
          ) {
            try {
              MODULES[module].init();
            } catch (err) {
              console.error(`Error initializing module ${module}:`, err);
            }
          }
        });

        // Set up global event listeners
        this.setupGlobalEventListeners();
      },

      setupGlobalEventListeners() {
        // Handle flash messages with auto-dismiss
        const flashMessages = document.querySelectorAll(
          '.message[data-auto-dismiss]'
        );
        flashMessages.forEach((message) => {
          setTimeout(() => {
            if (message.getAttribute) {
              message.setAttribute(
                'classes',
                'add fade-out:0s, remove message:1s'
              );
            }
          }, 5000); // 5 second delay before starting fade-out
        });
      },

      /**
       * Load a CSS stylesheet dynamically
       * @param {string} href - Stylesheet URL
       * @param {string} id - Optional ID for the stylesheet
       */
      loadStylesheet(href, id) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        if (id) {
          link.id = id;
        }
        document.head.appendChild(link);
      },
    },

    /**
     * Project selection and filtering
     */
    projects: {
      init() {
        // Handle project selection changes
        document.addEventListener('change', (e) => {
          if (e.target.matches('#project-select')) {
            this.handleProjectChange(e.target.value);
          }
        });

        // Restore project selection when returning from another page
        this.restoreProjectSelection();

        // Update Add Obligation button to include the current project_id
        this.updateAddObligationButton();
      },

      handleProjectChange(projectId) {
        // Store the selection in session storage
        if (projectId) {
          sessionStorage.setItem('lastProjectId', projectId);
        }

        // Trigger updates for data containers
        if (htmx) {
          htmx.trigger('#chart-container', 'refreshCharts');
          htmx.trigger('#obligations-container', 'refreshObligations');
        }

        // Update the Add Obligation button URL
        this.updateAddObligationButton();
      },

      restoreProjectSelection() {
        const projectSelect = document.getElementById('project-select');
        const lastProjectId = sessionStorage.getItem('lastProjectId');

        if (projectSelect && lastProjectId) {
          projectSelect.value = lastProjectId;
          // Trigger change event to update dependent components
          projectSelect.dispatchEvent(new Event('change'));
        }
      },

      updateAddObligationButton() {
        const projectSelect = document.getElementById('project-select');
        const addObligationBtn = document.querySelector('.add-obligation-btn');

        if (projectSelect && addObligationBtn) {
          const projectId = projectSelect.value;
          if (projectId) {
            const currentHref = addObligationBtn.getAttribute('href');
            const baseUrl = currentHref.split('?')[0];
            addObligationBtn.setAttribute(
              'href',
              `${baseUrl}?project_id=${projectId}`
            );
          }
        }
      },
    },

    /**
     * Chart and visualization management
     */
    charts: {
      init() {
        // Set up chart scrolling functionality
        document.addEventListener('htmx:afterSettle', () => {
          const chartScroll = document.getElementById('chartScroll');
          if (chartScroll) {
            this.setupChartNavigation(chartScroll);
          }
        });
      },

      setupChartNavigation(container) {
        // Add keyboard navigation
        container.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowLeft') {
            e.preventDefault();
            this.scrollCharts(container, 'left');
          } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            this.scrollCharts(container, 'right');
          }
        });
      },

      scrollCharts(container, direction) {
        if (!container) return;

        const scrollAmount = 320;
        container.scrollBy({
          left: direction === 'left' ? -scrollAmount : scrollAmount,
          behavior: 'smooth',
        });
      },
    },

    /**
     * Table and data display features
     */
    tables: {
      init() {
        // Initial setup of table scrolling
        this.setupTableScrolling();

        // Listen for new content that may contain tables
        document.addEventListener(
          'htmx:afterSettle',
          this.setupTableScrolling.bind(this)
        );
      },

      setupTableScrolling() {
        const tableContainers = document.querySelectorAll('.table-container');
        tableContainers.forEach((container) => {
          const scrollArea = container.querySelector('.horizontal-scroll');
          const scrollIndicator = container.querySelector('.scroll-indicator');

          // Create scroll indicator if it doesn't exist
          if (scrollArea && !scrollIndicator) {
            const indicator = document.createElement('div');
            indicator.className = 'scroll-indicator';

            const thumb = document.createElement('div');
            thumb.className = 'scroll-thumb';
            indicator.appendChild(thumb);

            container.appendChild(indicator);

            // Update scroll indicator on scroll
            scrollArea.addEventListener('scroll', () =>
              this.updateScrollIndicator(scrollArea, thumb)
            );

            // Initial update
            this.updateScrollIndicator(scrollArea, thumb);
          }
        });
      },

      updateScrollIndicator(scrollArea, thumb) {
        if (!scrollArea || !thumb) return;

        // Calculate thumb width and position
        const scrollWidth = scrollArea.scrollWidth;
        const viewportWidth = scrollArea.clientWidth;
        const scrollLeft = scrollArea.scrollLeft;

        const thumbWidth = (viewportWidth / scrollWidth) * 100;
        const thumbPosition =
          (scrollLeft / (scrollWidth - viewportWidth)) * (100 - thumbWidth);

        // Update thumb style
        thumb.style.width = `${thumbWidth}%`;
        thumb.style.marginLeft = `${thumbPosition}%`;
      },

      /**
       * Handle exporting table data to CSV
       * @param {Element} table - Table element to export
       * @param {string} filename - Desired filename for the CSV
       */
      exportToCSV(table, filename) {
        if (!table) return;

        // Extract headers
        const rows = Array.from(table.querySelectorAll('tr'));
        const headers = Array.from(rows[0].querySelectorAll('th')).map(
          (cell) => `"${cell.textContent.trim().replace(/"/g, '""')}"`
        );

        // Extract data rows
        const data = rows.slice(1).map((row) => {
          return Array.from(row.querySelectorAll('td')).map(
            (cell) => `"${cell.textContent.trim().replace(/"/g, '""')}"`
          );
        });

        // Combine headers and data
        const csvContent = [
          headers.join(','),
          ...data.map((row) => row.join(',')),
        ].join('\n');

        // Create download link
        const blob = new Blob([csvContent], {
          type: 'text/csv;charset=utf-8;',
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');

        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.display = 'none';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      },
    },

    /**
     * HTMX extensions and event handling
     */
    htmxHandlers: {
      init() {
        // Set up HTMX event handlers if HTMX is available
        if (typeof htmx === 'undefined') return;

        // Setup loading states
        document.body.addEventListener('htmx:beforeRequest', (e) => {
          const target = e.detail.target;
          if (target.matches('#obligations-container, #chart-container')) {
            target.innerHTML =
              '<div class="notice" role="status" aria-busy="true">Loading...</div>';
          }
        });

        // Handle HTMX response errors
        document.body.addEventListener('htmx:responseError', (e) => {
          const target = e.detail.target;
          target.innerHTML = `
            <div class="notice error" role="alert">
              <p>Error loading data. Please try again.</p>
            </div>
          `;
        });

        // Handle obligation status changes
        document.addEventListener('htmx:afterSettle', (e) => {
          if (
            e.detail.triggerSpec &&
            e.detail.triggerSpec.includes('obligation:statusChanged')
          ) {
            htmx.trigger('#chart-container', 'refreshCharts');
          }
        });

        // Add entrance animations to newly swapped content
        document.body.addEventListener('htmx:afterSwap', (e) => {
          if (e.detail.target.hasAttribute('data-animate-entrance')) {
            e.detail.target.setAttribute('classes', 'add fade-in');
          }
        });

        // Integration with PathDeps extension
        if (typeof window.PathDeps !== 'undefined') {
          document.body.addEventListener('htmx:afterRequest', (e) => {
            // Only handle successful POST/PUT/DELETE requests (mutations)
            if (!e.detail.successful || e.detail.xhr.method === 'GET') return;

            const path = e.detail.requestConfig.path;
            if (path && path.includes('/obligations/')) {
              // Manually refresh related components
              window.PathDeps.refresh('/obligations/');
              window.PathDeps.refresh('/mechanisms/charts/');
              window.PathDeps.refresh('/dashboard/overdue-count/');
            }
          });
        }
      },
    },

    /**
     * Form handling and validation
     */
    forms: {
      init() {
        // Handle filter form submission
        document.addEventListener('submit', (e) => {
          if (e.target.matches('#obligations-filter-form')) {
            e.preventDefault();
            this.handleFilterFormSubmit(e.target);
          }
        });

        // Set up filter removal handlers
        document.addEventListener('click', (e) => {
          if (e.target.matches('.remove-filter')) {
            e.preventDefault();
            const type = e.target.getAttribute('data-filter-type');
            const value = e.target.getAttribute('data-filter-value');
            if (type && value) {
              this.removeFilter(type, value);
            }
          }
        });
      },

      handleFilterFormSubmit(form) {
        // Update UI elements related to filtering
        const filterCount = document.getElementById('filter-count');
        if (filterCount) {
          const activeFilters = Array.from(
            form.querySelectorAll('select, input[type="text"]')
          ).filter((el) => el.value && el.value !== '').length;

          filterCount.textContent = activeFilters;
          filterCount.hidden = activeFilters === 0;
        }
      },

      /**
       * Remove a filter value and trigger update
       * @param {string} type - Filter field name
       * @param {string} value - Value to remove
       */
      removeFilter(type, value) {
        const select = document.querySelector(`select[name="${type}"]`);
        if (select) {
          Array.from(select.options).forEach((option) => {
            if (option.value === value) {
              option.selected = false;
            }
          });
          select.dispatchEvent(new Event('change'));
        }
      },
    },

    /**
     * Document actions like print, export, etc.
     */
    documentActions: {
      init() {
        // Handle print button clicks
        document.addEventListener('click', (e) => {
          if (e.target.matches('#print-obligations')) {
            e.preventDefault();
            window.print();
          }
        });

        // Handle export button clicks
        document.addEventListener('click', (e) => {
          if (e.target.matches('#export-obligations')) {
            e.preventDefault();
            const table = document.querySelector('table');
            if (table) {
              MODULES.tables.exportToCSV(table, 'obligations_export.csv');
            }
          }
        });

        // Handle obligation link clicks
        document.addEventListener('click', (e) => {
          if (
            e.target.matches('.obligation-link') ||
            e.target.closest('.obligation-link')
          ) {
            // Show loading indicator
            document.body.classList.add('loading');

            // Store the current project ID in session storage
            const projectId = document.querySelector(
              'input[name="project_id"]'
            )?.value;
            if (projectId) {
              sessionStorage.setItem('lastProjectId', projectId);
            }
          }
        });
      },
    },
   
  };

  // Initialize application when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    MODULES.core.init();
  });
})();
