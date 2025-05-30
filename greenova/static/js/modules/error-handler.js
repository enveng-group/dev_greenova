/**
 * Greenova Error Handler
 *
 * This module provides centralized error handling for JavaScript errors
 * that may occur during runtime. It follows a minimalist approach focused
 * on reliability while maintaining user experience.
 */

(() => {
	/**
	 * Global error handler to catch unhandled exceptions
	 * @param {Error} error - The error object
	 * @param {string} source - Source of the error
	 * @param {number} lineno - Line number where error occurred
	 * @param {number} colno - Column number where error occurred
	 * @param {ErrorEvent} event - The original error event
	 * @returns {boolean} - Returns true to prevent default browser error handler
	 */
	window.addEventListener("error", (event) => {
		handleError({
			type: "unhandled",
			message: event.error?.message || "Unknown error",
			source: event.filename || "unknown",
			lineno: event.lineno,
			stack: event.error?.stack,
		});
		return true;
	});

	/**
	 * Promise rejection handler for unhandled promise rejections
	 */
	window.addEventListener("unhandledrejection", (event) => {
		handleError({
			type: "promise",
			message: event.reason?.message || "Unhandled promise rejection",
			stack: event.reason?.stack,
		});
	});

	/**
	 * HTMX specific error handler for request failures
	 */
	document.body.addEventListener("htmx:responseError", (event) => {
		const response = event.detail.xhr;

		handleError({
			type: "htmx",
			status: response.status,
			url: event.detail.requestConfig.path,
			message: `HTMX request failed with status ${response.status}`,
		});

		// For 5xx errors, show a user-friendly message in the target
		if (response.status >= 500) {
			const target = event.detail.target;
			if (target) {
				target.innerHTML = `
          <div class="notice error" role="alert">
            <p>Sorry, something went wrong with this request. Please try again.</p>
          </div>
        `;
			}
		}
	});

	/**
	 * Central error handling function
	 * @param {Object} errorInfo - Information about the error
	 */
	function handleError(errorInfo) {
		// Log to console for debugging
		console.error("[Greenova Error]", errorInfo);

		// Create a standardized error object
		const errorData = {
			message: errorInfo.message,
			type: errorInfo.type,
			url: window.location.href,
			timestamp: new Date().toISOString(),
			userAgent: navigator.userAgent,
			...errorInfo,
		};

		// If we have a viable error and are in production mode, send to server
		if (errorInfo.message && !isLocalDevelopment()) {
			sendErrorToServer(errorData);
		}
	}

	/**
	 * Send error data to server for logging
	 * @param {Object} errorData - Error information to send
	 */
	function sendErrorToServer(errorData) {
		// Use a simple fetch with keep-alive: false to ensure error reporting
		// doesn't hang if the page is being unloaded
		const blob = new Blob([JSON.stringify(errorData)], {
			type: "application/json",
		});

		// Only attempt to send if navigator.sendBeacon is available
		if (navigator.sendBeacon) {
			navigator.sendBeacon("/api/log-client-error/", blob);
		} else {
			// Fallback to fetch for older browsers
			fetch("/api/log-client-error/", {
				method: "POST",
				body: blob,
				headers: {
					"Content-Type": "application/json",
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": getCSRFToken(),
				},
				keepalive: true,
			}).catch(() => {
				// Silent catch - we don't want errors in error reporting
			});
		}
	}

	/**
	 * Check if we're in local development mode
	 * @returns {boolean} True if local development
	 */
	function isLocalDevelopment() {
		const host = window.location.hostname;
		return host === "localhost" || host === "127.0.0.1";
	}

	/**
	 * Get CSRF token from cookies for secure requests
	 * @returns {string} CSRF token
	 */
	function getCSRFToken() {
		const name = "csrftoken";
		const value = `; ${document.cookie}`;
		const parts = value.split(`; ${name}=`);
		if (parts.length === 2) {
			return parts.pop().split(";").shift() || "";
		}
		return "";
	}

	// Expose limited API for manual error reporting
	window.GreenovaErrorHandler = {
		/**
		 * Report an error manually
		 * @param {Error|string} error - Error object or message
		 * @param {Object} context - Additional context information
		 */
		reportError: (error, context = {}) => {
			handleError({
				type: "manual",
				message: error instanceof Error ? error.message : String(error),
				stack: error instanceof Error ? error.stack : null,
				context,
			});
		},
	};
})();
