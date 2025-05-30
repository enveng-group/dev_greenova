/**
 * Greenova Theme Initialization
 *
 * This script initializes the theme early in the page load process to prevent
 * flash of unstyled content (FOUC) and flash of incorrect theme (FOIT).
 * It's kept separate from the main app.js to ensure fast execution.
 */

(() => {
	// Config
	const CONFIG = {
		rootAttribute: "data-theme",
		localStorageKey: "picoPreferredColorScheme",
		defaultScheme: "auto",
	};

	// Get theme from local storage or use default
	function getStoredTheme() {
		return (
			window.localStorage?.getItem(CONFIG.localStorageKey) ||
			CONFIG.defaultScheme
		);
	}

	// Get preferred system theme
	function getSystemPreference() {
		return window.matchMedia("(prefers-color-scheme: dark)").matches
			? "dark"
			: "light";
	}

	// Apply theme to document
	function applyTheme(theme) {
		const rootElement = document.documentElement;
		if (!rootElement) return;

		if (theme === "auto") {
			rootElement.setAttribute(CONFIG.rootAttribute, getSystemPreference());
		} else {
			rootElement.setAttribute(CONFIG.rootAttribute, theme);
		}
	}

	// Initialize theme as early as possible
	function initTheme() {
		const savedTheme = getStoredTheme();
		applyTheme(savedTheme);

		// Set up listener for system preference changes
		window
			.matchMedia("(prefers-color-scheme: dark)")
			.addEventListener("change", (event) => {
				if (getStoredTheme() === "auto") {
					applyTheme("auto");
				}
			});

		// Listen for themeChanged event from hyperscript
		document.addEventListener("themeChanged", (e) => {
			const theme = e.detail?.theme;
			if (!theme) return;
			// Persist theme selection
			window.localStorage.setItem(CONFIG.localStorageKey, theme);
			applyTheme(theme);
		});
	}

	// Expose setTheme globally for hyperscript
	window.setTheme = (theme) => {
		if (!theme) return;
		window.localStorage.setItem(CONFIG.localStorageKey, theme);
		applyTheme(theme);
	};

	// Execute immediately
	initTheme();
})();
