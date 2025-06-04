/* eslint-env browser */
/* global document, Plotly */
/**
 * Dashboard drilldown chart interactivity
 * Integrates Matplotlib SVG charts with Plotly.js for enhanced interactivity
 */
(() => {
  // Initialize dashboard drilldown functionality
  function initializeDashboardDrilldown () {
    // Initialize tooltip container
    initializeTooltip()

    // Set up chart interactivity
    initializeChartInteractivity()

    // Initialize Plotly.js enhancements
    initializePlotlyEnhancements()
  }

  // Initialize tooltip container
  function initializeTooltip () {
    let tooltipContainer = document.getElementById('chart-tooltip')
    if (!tooltipContainer) {
      tooltipContainer = document.createElement('div')
      tooltipContainer.id = 'chart-tooltip'
      tooltipContainer.className = 'chart-tooltip'
      tooltipContainer.setAttribute('role', 'tooltip')
      tooltipContainer.setAttribute('aria-live', 'polite')
      document.body.appendChild(tooltipContainer)
    }
    return tooltipContainer
  }

  // Initialize chart interactivity for SVG charts
  function initializeChartInteractivity () {
    // Find all interactive SVG charts
    const interactiveCharts = document.querySelectorAll(
      'svg.interactive-chart'
    )

    interactiveCharts.forEach((chart) => {
      setupSVGInteractivity(chart)
    })

    // Handle mechanism charts
    const mechanismCharts = document.querySelectorAll('.mechanism-chart')
    mechanismCharts.forEach((chart) => {
      setupMechanismChartInteractivity(chart)
    })

    // Handle procedure charts
    const procedureCharts = document.querySelectorAll('.procedure-chart')
    procedureCharts.forEach((chart) => {
      setupProcedureChartInteractivity(chart)
    })

    // Handle obligation list interactions
    const obligationRows = document.querySelectorAll('.obligation-row')
    obligationRows.forEach((row) => {
      setupObligationRowInteractivity(row)
    })
  }

  // Set up SVG chart interactivity
  function setupSVGInteractivity (svg) {
    // Find pie chart segments (paths)
    const segments = svg.querySelectorAll('path[fill]')

    segments.forEach((segment, index) => {
      // Add data attributes for identification
      segment.setAttribute('data-segment-index', index)
      segment.setAttribute('tabindex', '0')
      segment.setAttribute('role', 'button')

      // Add hover effects
      segment.addEventListener('mouseenter', (e) => {
        handleSegmentHover(e, segment)
      })

      segment.addEventListener('mouseleave', (e) => {
        handleSegmentLeave(e, segment)
      })

      // Add click handlers
      segment.addEventListener('click', (e) => {
        handleSegmentClick(e, segment)
      })

      // Add keyboard support
      segment.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          handleSegmentClick(e, segment)
        }
      })
    })
  }

  // Set up mechanism chart interactivity
  function setupMechanismChartInteractivity (chartContainer) {
    const svg = chartContainer.querySelector('svg')
    if (!svg) {
      return;
    }

    // Extract mechanism data from data attributes
    const mechanismId = chartContainer.getAttribute('data-mechanism-id')
    const projectId = chartContainer.getAttribute('data-project-id')

    if (!mechanismId || !projectId) {
      return;
    }

    // Make entire chart clickable for drilldown
    chartContainer.addEventListener('click', (e) => {
      // Prevent default if clicking on specific segments
      if (e.target.tagName === 'path') {
        return;
      }

      // Navigate to procedure drilldown
      navigateToProcedureDrilldown(mechanismId, projectId)
    })

    // Add hover effects for entire chart
    chartContainer.addEventListener('mouseenter', () => {
      chartContainer.style.transform = 'scale(1.02)'
      chartContainer.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)'
    })

    chartContainer.addEventListener('mouseleave', () => {
      chartContainer.style.transform = 'scale(1)'
      chartContainer.style.boxShadow = ''
    })
  }

  // Set up procedure chart interactivity
  function setupProcedureChartInteractivity (chartContainer) {
    const svg = chartContainer.querySelector('svg')
    if (!svg) {
      return;
    }

    const procedureId = chartContainer.getAttribute('data-procedure-id')
    const mechanismId = chartContainer.getAttribute('data-mechanism-id')

    if (!procedureId || !mechanismId) {
      return;
    }

    // Make chart clickable for drilldown to obligations
    chartContainer.addEventListener('click', (e) => {
      if (e.target.tagName === 'path') {
        return;
      }

      navigateToObligationList(procedureId, mechanismId)
    })

    // Add hover effects
    chartContainer.addEventListener('mouseenter', () => {
      chartContainer.style.transform = 'scale(1.02)'
      chartContainer.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)'
    })

    chartContainer.addEventListener('mouseleave', () => {
      chartContainer.style.transform = 'scale(1)'
      chartContainer.style.boxShadow = ''
    })
  }

  // Set up obligation row interactivity
  function setupObligationRowInteractivity (row) {
    // Add hover effects for overdue obligations
    if (row.classList.contains('overdue')) {
      row.addEventListener('mouseenter', () => {
        row.style.backgroundColor = '#fff5f5'
        row.style.borderLeft = '4px solid #f94144'
      })

      row.addEventListener('mouseleave', () => {
        row.style.backgroundColor = ''
        row.style.borderLeft = ''
      })
    }

    // Add click handler for row selection
    row.addEventListener('click', (e) => {
      // Don't interfere with button clicks
      if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {
        return;
      }

      const obligationId = row.getAttribute('data-obligation-id')
      if (obligationId) {
        navigateToObligationDetail(obligationId)
      }
    })
  }

  // Handle segment hover
  function handleSegmentHover (event, segment) {
    // Highlight segment
    const originalFill = segment.getAttribute('fill')
    segment.setAttribute('data-original-fill', originalFill)

    // Brighten the color
    const brighterColor = adjustBrightness(originalFill, 20)
    segment.setAttribute('fill', brighterColor)

    // Show tooltip
    showTooltip(event, segment)
  }

  // Handle segment leave
  function handleSegmentLeave (event, segment) {
    // Restore original color
    const originalFill = segment.getAttribute('data-original-fill')
    if (originalFill) {
      segment.setAttribute('fill', originalFill)
    }

    // Hide tooltip
    hideTooltip()
  }

  // Handle segment click
  function handleSegmentClick (event, segment) {
    event.preventDefault()
    event.stopPropagation()

    // Get chart context
    const svg = segment.closest('svg')
    const chartContainer = svg.closest(
      '.chart-container, .mechanism-chart, .procedure-chart'
    )

    if (!chartContainer) {
      return;
    }

    // Determine chart type and handle accordingly
    if (chartContainer.classList.contains('mechanism-chart')) {
      const mechanismId = chartContainer.getAttribute('data-mechanism-id')
      const projectId = chartContainer.getAttribute('data-project-id')

      if (mechanismId && projectId) {
        navigateToProcedureDrilldown(mechanismId, projectId)
      }
    } else if (chartContainer.classList.contains('procedure-chart')) {
      const procedureId = chartContainer.getAttribute('data-procedure-id')
      const mechanismId = chartContainer.getAttribute('data-mechanism-id')

      if (procedureId && mechanismId) {
        navigateToObligationList(procedureId, mechanismId)
      }
    }
  }

  // Show tooltip
  function showTooltip (event, segment) {
    const tooltip = document.getElementById('chart-tooltip')
    if (!tooltip) {
      return;
    }

    // Get segment data
    const segmentIndex = segment.getAttribute('data-segment-index')
    const svg = segment.closest('svg')
    const chartContainer = svg.closest(
      '.chart-container, .mechanism-chart, .procedure-chart'
    )

    // Extract tooltip content from chart context
    let tooltipContent = `Segment ${segmentIndex}`

    if (chartContainer) {
      const chartTitle = chartContainer.querySelector('h3, h4, .chart-title')
      if (chartTitle) {
        tooltipContent = `${chartTitle.textContent} - Click to drill down`
      }
    }

    tooltip.innerHTML = tooltipContent
    tooltip.style.display = 'block'
    tooltip.style.left = `${event.pageX + 10}px`
    tooltip.style.top = `${event.pageY - 10}px`
  }

  // Hide tooltip
  function hideTooltip () {
    const tooltip = document.getElementById('chart-tooltip')
    if (tooltip) {
      tooltip.style.display = 'none'
    }
  }

  // Navigation functions
  function navigateToProcedureDrilldown (mechanismId, projectId) {
    const url = `/dashboard/procedures/?mechanism_id=${mechanismId}&project_id=${projectId}`

    // Use HTMX if available, otherwise standard navigation
    if (window.htmx) {
      htmx.ajax('GET', url, {
        target: '#main-content',
        swap: 'innerHTML'
      })
    } else {
      window.location.href = url
    }
  }

  function navigateToObligationList (procedureId, mechanismId) {
    const url = `/dashboard/obligations/?procedure_id=${procedureId}&mechanism_id=${mechanismId}`

    if (window.htmx) {
      htmx.ajax('GET', url, {
        target: '#main-content',
        swap: 'innerHTML'
      })
    } else {
      window.location.href = url
    }
  }

  function navigateToObligationDetail (obligationId) {
    const url = `/obligations/${obligationId}/`

    if (window.htmx) {
      htmx.ajax('GET', url, {
        target: '#main-content',
        swap: 'innerHTML'
      })
    } else {
      window.location.href = url
    }
  }

  // Initialize Plotly.js enhancements
  function initializePlotlyEnhancements () {
    // Only initialize if Plotly is available
    if (typeof Plotly === 'undefined') {
      console.warn('Plotly.js not loaded, skipping Plotly enhancements')
      return
    }

    // Find elements with plotly data
    const plotlyElements = document.querySelectorAll('[data-plotly-data]')

    plotlyElements.forEach((element) => {
      try {
        const plotlyData = JSON.parse(element.getAttribute('data-plotly-data'))
        createPlotlyChart(element, plotlyData)
      } catch (error) {
        console.error('Error creating Plotly chart:', error)
      }
    })
  }

  // Create Plotly chart
  function createPlotlyChart (element, data) {
    const layout = {
      ...data.layout,
      responsive: true,
      displayModeBar: false,
      staticPlot: false
    }

    const config = {
      displaylogo: false,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
      responsive: true
    }

    Plotly.newPlot(element, data.data, layout, config)

    // Add click handlers for drilldown
    element.on('plotly_click', (data) => {
      handlePlotlyClick(data)
    })

    element.on('plotly_hover', (data) => {
      handlePlotlyHover(data)
    })
  }

  // Handle Plotly click events
  function handlePlotlyClick (data) {
    if (data.points && data.points.length > 0) {
      const point = data.points[0]

      // Extract drilldown information from point data
      const customData = point.customdata

      if (customData && customData.drilldown_url) {
        if (window.htmx) {
          htmx.ajax('GET', customData.drilldown_url, {
            target: '#main-content',
            swap: 'innerHTML'
          })
        } else {
          window.location.href = customData.drilldown_url
        }
      }
    }
  }

  // Handle Plotly hover events
  function handlePlotlyHover (data) {
    if (data.points && data.points.length > 0) {
      const point = data.points[0]
      console.log('Plotly hover:', point.label, point.value)
    }
  }

  // Utility function to adjust color brightness
  function adjustBrightness (color, percent) {
    // Simple color adjustment - works with hex colors
    if (color.startsWith('#')) {
      const num = parseInt(color.slice(1), 16)
      const amt = Math.round(2.55 * percent)
      const R = (num >> 16) + amt
      const G = ((num >> 8) & 0x00ff) + amt
      const B = (num & 0x0000ff) + amt

      return (
        '#' +
				(
				  (0x1000000 +
					(R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
					(G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 + ((B < 255 ? B < 1 ? 0 : B : 255)))
				)
				  .toString(16)
				  .slice(1)
      )
    }

    return color // Return original if not hex
  }

  // Initialize when DOM is loaded
  document.addEventListener('DOMContentLoaded', initializeDashboardDrilldown)

  // Re-initialize when content is loaded via HTMX
  document.addEventListener('htmx:afterSettle', initializeDashboardDrilldown)

  // Re-initialize when charts are dynamically loaded
  document.addEventListener('htmx:afterSwap', initializeDashboardDrilldown)
})()
