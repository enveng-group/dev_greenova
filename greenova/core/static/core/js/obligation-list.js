// Obligation List Page Logic (migrated from inline script)
document.addEventListener('DOMContentLoaded', function () {
  // Initialize components after WASM is loaded
  if (window.wasmReady) {
    initializeObligationList()
  } else {
    // Wait for WASM to be ready
    document.addEventListener('wasmReady', initializeObligationList)
  }

  function initializeObligationList () {
    const themeSelector = document.getElementById('theme-selector')
    const applyThemeBtn = document.getElementById('apply-theme')
    const obligationCount = document.getElementById('obligation-count')

    // Initialize theme selector with current theme
    if (window.wasmModule) {
      const currentTheme = window.wasmModule.getTheme()
      themeSelector.value = currentTheme.toString()
    }

    // Theme change handler
    function handleThemeChange () {
      const selectedTheme = parseInt(themeSelector.value, 10)
      if (window.wasmModule) {
        try {
          window.wasmModule.setTheme(selectedTheme)
          const resolvedTheme = window.wasmModule.resolveTheme(selectedTheme)
          document.documentElement.classList.remove(
            'theme-light',
            'theme-dark'
          )
          document.documentElement.classList.add(
            resolvedTheme === 0 ? 'theme-light' : 'theme-dark'
          )
          showNotification('Theme updated successfully', 'success')
        } catch (error) {
          console.error('Error applying theme:', error)
          showNotification('Error applying theme', 'error')
        }
      }
    }

    applyThemeBtn.addEventListener('click', handleThemeChange)
    themeSelector.addEventListener('change', handleThemeChange)
    loadObligationsData()
    setInterval(loadObligationsData, 30000)
  }

  function loadObligationsData () {
    const obligationCount = document.getElementById('obligation-count')
    obligationCount.innerHTML =
      '<span class="loading-spinner"></span> Loading...'
    fetch(window.OBLIGATIONS_API_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        return response.json()
      })
      .then((data) => {
        updateObligationCount(data.obligations.length)
        updateObligationTable(data.obligations)
      })
      .catch((error) => {
        console.error('Error loading obligations:', error)
        obligationCount.textContent = 'Error'
        showNotification('Failed to load obligations data', 'error')
      })
  }

  function updateObligationCount (count) {
    const obligationCount = document.getElementById('obligation-count')
    obligationCount.textContent = `${count} obligations`
    obligationCount.classList.add('fade-in')
  }

  function updateObligationTable (obligations) {
    const tableRows = document.querySelectorAll('#obligations-table tbody tr')
    if (window.wasmModule) {
      tableRows.forEach((row, index) => {
        const delay = window.wasmModule.linearEasing(index * 0.1, 1.0)
        setTimeout(() => {
          row.classList.add('row-highlight')
          setTimeout(() => row.classList.remove('row-highlight'), 1000)
        }, delay * 100)
      })
    }
  }

  function showNotification (message, type = 'info') {
    const notification = document.createElement('div')
    notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed greenova-notification`
    notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `
    document.body.appendChild(notification)
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove()
      }
    }, 5000)
  }

  // Filter form enhancement
  const filterForm = document.getElementById('filter-form')
  if (filterForm) {
    filterForm.addEventListener('submit', function (e) {
      const submitBtn = filterForm.querySelector('button[type="submit"]')
      if (submitBtn) {
        submitBtn.innerHTML =
          '<span class="loading-spinner"></span> Applying...'
        submitBtn.disabled = true
      }
    })
  }
})
