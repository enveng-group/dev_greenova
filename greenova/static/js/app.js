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

