/**
 * WASM Loader for Greenova AssemblyScript Module
 * Integrates WebAssembly compiled from TypeScript for theme management and animations
 */

// Global state
window.wasmModule = null
window.wasmReady = false

// WASM module loading and initialization
async function loadWasmModule () {
  try {
    // Load the WebAssembly module
    const wasmModule = await WebAssembly.instantiateStreaming(
      fetch('/static/core/as/build/release.wasm')
    )

    // Store the module globally
    window.wasmModule = wasmModule.instance.exports
    window.wasmReady = true

    console.log('WASM module loaded successfully')

    // Initialize default theme
    initializeTheme()

    // Dispatch ready event
    document.dispatchEvent(new CustomEvent('wasmReady'))

    return window.wasmModule
  } catch (error) {
    console.error('Failed to load WASM module:', error)

    // Fallback implementations
    window.wasmModule = createFallbackModule()
    window.wasmReady = true

    document.dispatchEvent(new CustomEvent('wasmReady'))
    return window.wasmModule
  }
}

// Fallback JavaScript implementations
function createFallbackModule () {
  console.warn('Using JavaScript fallback for WASM functions')

  return {
    setTheme: function (theme) {
      localStorage.setItem('greenova-theme', theme.toString())
      return theme
    },

    getTheme: function () {
      const stored = localStorage.getItem('greenova-theme')
      return stored ? parseInt(stored, 10) : 2 // Default to auto
    },

    resolveTheme: function (theme) {
      if (theme === 2) {
        // Auto theme
        const prefersDark = window.matchMedia(
          '(prefers-color-scheme: dark)'
        ).matches
        return prefersDark ? 1 : 0
      }
      return theme
    },

    linearEasing: function (t) {
      return Math.max(0, Math.min(1, t))
    },

    easeInOutEasing: function (t) {
      return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2
    },

    calculateAnimationHeight: function (startHeight, endHeight, progress) {
      const p = Math.max(0, Math.min(1, progress))
      return startHeight + (endHeight - startHeight) * p
    }
  }
}

// Theme initialization
function initializeTheme () {
  if (!window.wasmModule) {
    return;
  }

  try {
    const currentTheme = window.wasmModule.getTheme()
    const resolvedTheme = window.wasmModule.resolveTheme(currentTheme)

    // Apply theme to document
    document.documentElement.classList.remove('theme-light', 'theme-dark')
    document.documentElement.classList.add(
      resolvedTheme === 0 ? 'theme-light' : 'theme-dark'
    )

    console.log(
      'Theme initialized: ' +
        currentTheme +
        ' (resolved: ' +
        resolvedTheme +
        ')'
    )
  } catch (error) {
    console.error('Error initializing theme:', error)
  }
}

// Listen for system theme changes
if (window.matchMedia) {
  window
    .matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', function (e) {
      if (window.wasmModule) {
        const currentTheme = window.wasmModule.getTheme()
        if (currentTheme === 2) {
          // Auto theme
          initializeTheme()
        }
      }
    })
}

// Animation utilities using WASM functions
window.GreenovaAnimation = {
  easeInOut: function (element, duration, callback) {
    if (!window.wasmModule) {
      if (callback) {
        callback();
      }
      return
    }

    const startTime = performance.now()

    function animate (currentTime) {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easedProgress = window.wasmModule.easeInOutEasing(progress)

      if (callback) {
        callback(easedProgress);
      }

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  },

  fadeIn: function (element, duration = 300) {
    element.style.opacity = '0'
    element.style.transition = 'opacity ' + duration + 'ms ease-in-out'

    requestAnimationFrame(() => {
      element.style.opacity = '1'
    })
  },

  slideDown: function (element, duration = 300) {
    if (!window.wasmModule) {
      element.style.display = 'block'
      return
    }

    const startHeight = 0
    const endHeight = element.scrollHeight

    element.style.height = '0px'
    element.style.overflow = 'hidden'
    element.style.display = 'block'

    this.easeInOut(element, duration, (progress) => {
      const height = window.wasmModule.calculateAnimationHeight(
        startHeight,
        endHeight,
        progress
      )
      element.style.height = height + 'px'

      if (progress >= 1) {
        element.style.height = ''
        element.style.overflow = ''
      }
    })
  }
}

// Load WASM module when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadWasmModule)
} else {
  loadWasmModule()
}
