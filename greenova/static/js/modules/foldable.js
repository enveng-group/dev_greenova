/**
 * Foldable Component
 *
 * Provides collapsible/expandable UI elements with progressive enhancement:
 * 1. Works with semantic HTML structure
 * 2. Uses hyperscript for simple interactions when possible
 * 3. Falls back to this JavaScript when needed
 */

(() => {
	// Configuration
	const SELECTORS = {
		foldable: "[data-foldable]",
		trigger: "[data-foldable-trigger]",
		content: "[data-foldable-content]",
		expanded: '[data-foldable-expanded="true"]',
	};

	const CLASSES = {
		hidden: "hidden",
		expanded: "expanded",
		collapsed: "collapsed",
		animating: "animating",
	};

	const ATTRS = {
		expanded: "data-foldable-expanded",
		animationDuration: "data-animation-duration",
	};

	/**
	 * Initialize all foldable components on the page
	 */
	function initFoldables() {
		// Skip initialization if hyperscript is handling foldables
		if (typeof window._hyperscript !== "undefined") {
			// Hyperscript takes precedence - only initialize elements not handled by hyperscript
			const foldables = document.querySelectorAll(
				`${SELECTORS.foldable}:not([_])`,
			);
			initElements(foldables);
		} else {
			// No hyperscript, initialize all foldables
			const foldables = document.querySelectorAll(SELECTORS.foldable);
			initElements(foldables);
		}
	}

	/**
	 * Initialize a collection of foldable elements
	 * @param {NodeListOf<Element>} elements - Collection of foldable elements
	 */
	function initElements(elements) {
		elements.forEach((foldable) => {
			// Skip if already initialized
			if (foldable.hasAttribute("data-foldable-initialized")) {
				return;
			}

			// Find trigger and content elements
			const trigger = foldable.querySelector(SELECTORS.trigger);
			const content = foldable.querySelector(SELECTORS.content);

			// Skip if missing required elements
			if (!trigger || !content) {
				console.warn("Foldable missing trigger or content:", foldable);
				return;
			}

			// Set initial state
			const isExpanded =
				foldable.hasAttribute(ATTRS.expanded) &&
				foldable.getAttribute(ATTRS.expanded) === "true";

			// Set ARIA attributes for accessibility
			trigger.setAttribute("aria-expanded", isExpanded ? "true" : "false");
			trigger.setAttribute("aria-controls", ensureId(content));

			// Set initial visibility
			if (!isExpanded) {
				content.classList.add(CLASSES.hidden);
			}

			// Add event listener to trigger
			trigger.addEventListener("click", (event) => {
				event.preventDefault();
				toggleFoldable(foldable);
			});

			// Mark as initialized
			foldable.setAttribute("data-foldable-initialized", "true");
		});
	}

	/**
	 * Toggle foldable element state
	 * @param {Element} foldable - The foldable container element
	 */
	function toggleFoldable(foldable) {
		const trigger = foldable.querySelector(SELECTORS.trigger);
		const content = foldable.querySelector(SELECTORS.content);

		// Don't toggle if currently animating
		if (content.classList.contains(CLASSES.animating)) {
			return;
		}

		// Get current state
		const isExpanded = trigger.getAttribute("aria-expanded") === "true";

		// Update ARIA states
		trigger.setAttribute("aria-expanded", !isExpanded ? "true" : "false");

		// Toggle classes with animation
		if (isExpanded) {
			// Collapse animation
			content.style.height = `${content.scrollHeight}px`;

			// Force reflow
			content.offsetHeight;

			content.classList.add(CLASSES.animating);
			content.style.height = "0";

			// Set timing from attribute or default
			const duration =
				parseInt(foldable.getAttribute(ATTRS.animationDuration), 10) || 300;

			setTimeout(() => {
				content.classList.add(CLASSES.hidden);
				content.classList.remove(CLASSES.animating);
				content.style.height = "";

				// Update data attribute for state persistency
				foldable.setAttribute(ATTRS.expanded, "false");

				// Dispatch custom event
				foldable.dispatchEvent(
					new CustomEvent("foldable:collapsed", {
						bubbles: true,
						detail: { foldable },
					}),
				);
			}, duration);
		} else {
			// Expand animation
			content.classList.remove(CLASSES.hidden);

			// Temporarily set height to auto to measure
			const height = content.scrollHeight;

			// Start collapsed
			content.style.height = "0";

			// Force reflow
			content.offsetHeight;

			// Begin transition
			content.classList.add(CLASSES.animating);
			content.style.height = `${height}px`;

			// Set timing from attribute or default
			const duration =
				parseInt(foldable.getAttribute(ATTRS.animationDuration), 10) || 300;

			setTimeout(() => {
				content.classList.remove(CLASSES.animating);
				content.style.height = "";

				// Update data attribute for state persistency
				foldable.setAttribute(ATTRS.expanded, "true");

				// Dispatch custom event
				foldable.dispatchEvent(
					new CustomEvent("foldable:expanded", {
						bubbles: true,
						detail: { foldable },
					}),
				);
			}, duration);
		}
	}

	/**
	 * Ensure an element has an ID, generating one if needed
	 * @param {Element} element - Element to ensure ID for
	 * @returns {string} The element's ID
	 */
	function ensureId(element) {
		if (!element.id) {
			element.id = `foldable-content-${Math.random().toString(36).substr(2, 9)}`;
		}
		return element.id;
	}

	/**
	 * Handle content that's added dynamically via AJAX/HTMX
	 */
	function setupMutationObserver() {
		// Skip if not supported
		if (!window.MutationObserver) {
			return;
		}

		const observer = new MutationObserver((mutations) => {
			let needsCheck = false;

			mutations.forEach((mutation) => {
				if (mutation.type === "childList" && mutation.addedNodes.length) {
					needsCheck = true;
				}
			});

			if (needsCheck) {
				initFoldables();
			}
		});

		observer.observe(document.body, {
			childList: true,
			subtree: true,
		});
	}

	// Initialize on DOM ready
	document.addEventListener("DOMContentLoaded", () => {
		initFoldables();
		setupMutationObserver();
	});

	// Handle HTMX content swaps
	document.addEventListener("htmx:afterSwap", () => {
		initFoldables();
	});

	// Export API for programmatic usage
	window.Foldable = {
		init: initFoldables,
		toggle: (element) => {
			const foldable = element.closest(SELECTORS.foldable);
			if (foldable) {
				toggleFoldable(foldable);
			}
		},
		expand: (element) => {
			const foldable = element.closest(SELECTORS.foldable);
			if (foldable) {
				const trigger = foldable.querySelector(SELECTORS.trigger);
				if (trigger && trigger.getAttribute("aria-expanded") === "false") {
					toggleFoldable(foldable);
				}
			}
		},
		collapse: (element) => {
			const foldable = element.closest(SELECTORS.foldable);
			if (foldable) {
				const trigger = foldable.querySelector(SELECTORS.trigger);
				if (trigger && trigger.getAttribute("aria-expanded") === "true") {
					toggleFoldable(foldable);
				}
			}
		},
	};
})();
