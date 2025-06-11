/**
 * Login redirect handler for dashboard
 *
 * This script ensures that after login, the dashboard loads with a full page reload
 * instead of via HTMX, which can cause session context issues.
 */

(function () {
  'use strict'

  // Check if we're on the dashboard page after login
  function checkDashboardState () {
    // Only run on dashboard pages
    if (!window.location.pathname.includes('/dashboard/')) {
      return
    }

    // Check if user is authenticated but no project is selected
    const isAuthenticated = document.body.dataset.authenticated === 'true'
    const hasProjects =
      document.querySelector('#project_id') &&
      document.querySelector('#project_id option[value!=""]')
    const showingEmptyState = document.querySelector('.dashboard-empty-state')

    if (isAuthenticated && hasProjects && showingEmptyState) {
      // This suggests we're showing the empty state even though the user has projects
      // This can happen when the session isn't properly loaded via HTMX
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

  // Also run after HTMX requests complete
  document.addEventListener('htmx:afterRequest', function (event) {
    // Small delay to allow DOM updates
    setTimeout(checkDashboardState, 100)
  })
})()
