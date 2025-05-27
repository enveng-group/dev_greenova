/* eslint-env browser */
/* global document */
/**
 * Chart interactivity functions for SVG charts
 */
(function () {
  'use strict';

  // Initialize tooltip container
  function initializeTooltip() {
    // Create tooltip container if it doesn't exist
    let tooltipContainer = document.getElementById('chart-tooltip-container');
    if (!tooltipContainer) {
      tooltipContainer = document.createElement('div');
      tooltipContainer.id = 'chart-tooltip-container';
      document.body.appendChild(tooltipContainer);
    }
    return tooltipContainer;
  }

  // Initialize hover events for SVG chart segments
  function initializeChartInteractivity() {
    // Find all SVG elements within mechanism charts
    const chartContainers = document.querySelectorAll('.mechanism-chart');

    chartContainers.forEach((container) => {
      const svg = container.querySelector('svg');
      if (!svg) return;

      // Find all segment groups
      const segments = svg.querySelectorAll('[id^="segment-"]');
      segments.forEach((segment) => {
        // Attach data attributes for HTMX
        const statusKey = segment.id.split('-')[2];
        // eslint-disable-next-line no-unused-vars
        const count = segment.getAttribute('data-count');
        const mechanismId =
          container.querySelector('a')?.href.split('mechanism_id=')[1] || '';

        if (mechanismId) {
          segment.setAttribute(
            'hx-get',
            `/mechanisms/insights/?mechanism_id=${mechanismId}&status=${statusKey}`
          );
          segment.setAttribute('hx-target', '#chart-tooltip-container');
          segment.setAttribute('hx-trigger', 'mouseenter');
          segment.setAttribute('hx-swap', 'innerHTML');
        }
      });
    });
  }

  // Position tooltip near cursor
  function positionTooltip(e) {
    const tooltip = document.querySelector('.obligation-insight-tooltip');
    if (!tooltip) return;

    tooltip.style.left = `${e.pageX}px`;
    tooltip.style.top = `${e.pageY - 15}px`;
    tooltip.classList.add('active');
  }

  // Hide tooltip when mouse leaves
  function hideTooltip() {
    const tooltip = document.querySelector('.obligation-insight-tooltip');
    if (tooltip) {
      tooltip.classList.remove('active');
    }
  }

  // Set up event listeners
  function setupEventListeners() {
    document.addEventListener('htmx:afterSwap', function (e) {
      if (e.detail.target.id === 'chart-tooltip-container') {
        positionTooltip(e.detail.triggeringEvent);
      }
    });

    document.addEventListener('mouseover', function (e) {
      if (e.target.closest('[id^="segment-"]')) {
        const tooltipContainer = document.getElementById(
          'chart-tooltip-container'
        );
        if (tooltipContainer) {
          positionTooltip(e);
        }
      }
    });

    document.addEventListener('mouseout', function (e) {
      if (e.target.closest('[id^="segment-"]')) {
        hideTooltip();
      }
    });
  }

  // Initialize when DOM is loaded
  document.addEventListener('DOMContentLoaded', function () {
    initializeTooltip();
    initializeChartInteractivity();
    setupEventListeners();
  });

  // Also initialize when charts are loaded via HTMX
  document.addEventListener('htmx:afterSettle', function () {
    initializeTooltip();
    initializeChartInteractivity();
  });
})();
