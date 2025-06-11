/**
 * Login redirect handler for dashboard
 *
 * This script ensures that after login, the dashboard loads with a full page reload
 * instead of via HTMX, which can cause session context issues.
 */

(function () {
  'use strict'

  const hasReloaded = false

  // Check if we're on the dashboard page after login
  function checkDashboardState () {
    // Only run on dashboard pages
    if (!window.location.pathname.includes('/dashboard/')) {
      return
    }

    // Prevent infinite reload loops (persist across reloads)
    if (window.sessionStorage.getItem('dashboardReloaded') === 'true') {
      return
    }

    // Check if user is authenticated but no project is selected
    const isAuthenticated = document.body.dataset.authenticated === 'true'
    const projectSelect = document.querySelector('#project_id')
    const hasProjects =
      projectSelect &&
      projectSelect.querySelector('option:not([value=""])') &&
      !projectSelect.disabled &&
      projectSelect.offsetParent !== null // visible
    const showingEmptyState = document.querySelector('.dashboard-empty-state')

    if (
      isAuthenticated &&
      hasProjects &&
      showingEmptyState &&
      projectSelect // must be visible and enabled
    ) {
      // Only reload if the project select is visible and enabled
      window.sessionStorage.setItem('dashboardReloaded', 'true')
      console.log('Dashboard state inconsistent, forcing reload...')
      window.location.reload()
    }
  }

  // Run the check when the DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkDashboardState)
  } else {
    checkDashboardState()
  }

  // Also run after HTMX requests complete (but with more restrictive conditions)
  document.addEventListener('htmx:afterRequest', function (event) {
    // Only check after specific HTMX requests, not all of them
    if (
      event.detail.target &&
      (event.detail.target.id === 'main-content' ||
        event.detail.target.classList.contains('dashboard-content'))
    ) {
      // Small delay to allow DOM updates
      setTimeout(checkDashboardState, 100)
    }
  })
})()
