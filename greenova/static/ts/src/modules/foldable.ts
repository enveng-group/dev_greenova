/**
 * Foldable Component TypeScript Implementation
 *
 * This module provides collapsible/expandable UI elements with progressive enhancement
 * and leverages AssemblyScript for performance-critical animation calculations.
 */

import type { GreenovaWasmModule } from "../utils/wasm-loader";

/**
 * Configuration interfaces
 */
interface FoldableSelectors {
	foldable: string;
	trigger: string;
	content: string;
	expanded: string;
}

interface FoldableClasses {
	hidden: string;
	expanded: string;
	collapsed: string;
	animating: string;
}

interface FoldableAttributes {
	expanded: string;
	animationDuration: string;
}

/**
 * Foldable component implementation
 */
export class Foldable {
	private wasmModule: GreenovaWasmModule;
	private selectors: FoldableSelectors;
	private classes: FoldableClasses;
	private attrs: FoldableAttributes;

	constructor(wasmModule: GreenovaWasmModule) {
		this.wasmModule = wasmModule;

		// Configuration
		this.selectors = {
			foldable: "[data-foldable]",
			trigger: "[data-foldable-trigger]",
			content: "[data-foldable-content]",
			expanded: '[data-foldable-expanded="true"]',
		};

		this.classes = {
			hidden: "hidden",
			expanded: "expanded",
			collapsed: "collapsed",
			animating: "animating",
		};

		this.attrs = {
			expanded: "data-foldable-expanded",
			animationDuration: "data-animation-duration",
		};
	}

	/**
	 * Initialize foldable components
	 */
	public init(): void {
		// Skip initialization if hyperscript is handling foldables
		if (typeof (window as any)._hyperscript !== "undefined") {
			// Hyperscript takes precedence - only initialize elements not handled by hyperscript
			const foldables = document.querySelectorAll(
				`${this.selectors.foldable}:not([_])`,
			);
			this.initElements(foldables);
		} else {
			// No hyperscript, initialize all foldables
			const foldables = document.querySelectorAll(this.selectors.foldable);
			this.initElements(foldables);
		}

		this.setupMutationObserver();
		this.setupHtmxHandlers();
	}

	/**
	 * Initialize a collection of foldable elements
	 * @param elements Collection of foldable elements
	 */
	private initElements(elements: NodeListOf<Element>): void {
		elements.forEach((foldable) => {
			// Skip if already initialized
			if (foldable.hasAttribute("data-foldable-initialized")) {
				return;
			}

			// Find trigger and content elements
			const trigger = foldable.querySelector(this.selectors.trigger);
			const content = foldable.querySelector(this.selectors.content);

			// Skip if missing required elements
			if (!trigger || !content) {
				console.warn("Foldable missing trigger or content:", foldable);
				return;
			}

			// Set initial state
			const isExpanded =
				foldable.hasAttribute(this.attrs.expanded) &&
				foldable.getAttribute(this.attrs.expanded) === "true";

			// Set ARIA attributes for accessibility
			trigger.setAttribute("aria-expanded", isExpanded ? "true" : "false");
			trigger.setAttribute("aria-controls", this.ensureId(content));

			// Set initial visibility
			if (!isExpanded) {
				content.classList.add(this.classes.hidden);
			}

			// Add event listener to trigger
			trigger.addEventListener("click", (event) => {
				event.preventDefault();
				this.toggleFoldable(foldable);
			});

			// Mark as initialized
			foldable.setAttribute("data-foldable-initialized", "true");
		});
	}

	/**
	 * Toggle foldable element state
	 * @param foldable The foldable container element
	 */
	private toggleFoldable(foldable: Element): void {
		const trigger = foldable.querySelector(
			this.selectors.trigger,
		) as HTMLElement;
		const content = foldable.querySelector(
			this.selectors.content,
		) as HTMLElement;

		// Don't toggle if currently animating
		if (content.classList.contains(this.classes.animating)) {
			return;
		}

		// Get current state
		const isExpanded = trigger.getAttribute("aria-expanded") === "true";

		// Update ARIA states
		trigger.setAttribute("aria-expanded", !isExpanded ? "true" : "false");

		// Toggle classes with animation using AssemblyScript for calculations
		if (isExpanded) {
			// Collapse animation
			this.animateCollapse(foldable, content);
		} else {
			// Expand animation
			this.animateExpand(foldable, content);
		}
	}

	/**
	 * Animate collapse of content
	 * @param foldable The foldable container element
	 * @param content The content element to collapse
	 */
	private animateCollapse(foldable: Element, content: HTMLElement): void {
		// Set initial height to current height
		content.style.height = `${content.scrollHeight}px`;

		// Force reflow
		content.offsetHeight; // eslint-disable-line @typescript-eslint/no-unused-expressions

		content.classList.add(this.classes.animating);
		content.style.height = "0";

		// Get animation duration
		const duration = parseInt(
			foldable.getAttribute(this.attrs.animationDuration) || "300",
			10,
		);

		// Use setTimeout to handle animation completion
		setTimeout(() => {
			content.classList.add(this.classes.hidden);
			content.classList.remove(this.classes.animating);
			content.style.height = "";

			// Update data attribute for state persistence
			foldable.setAttribute(this.attrs.expanded, "false");

			// Dispatch custom event
			foldable.dispatchEvent(
				new CustomEvent("foldable:collapsed", {
					bubbles: true,
					detail: { foldable },
				}),
			);
		}, duration);
	}

	/**
	 * Animate expand of content
	 * @param foldable The foldable container element
	 * @param content The content element to expand
	 */
	private animateExpand(foldable: Element, content: HTMLElement): void {
		// Remove hidden class first
		content.classList.remove(this.classes.hidden);

		// Measure final height
		const height = content.scrollHeight;

		// Start collapsed
		content.style.height = "0";

		// Force reflow
		content.offsetHeight; // eslint-disable-line @typescript-eslint/no-unused-expressions

		// Begin transition
		content.classList.add(this.classes.animating);
		content.style.height = `${height}px`;

		// Get animation duration
		const duration = parseInt(
			foldable.getAttribute(this.attrs.animationDuration) || "300",
			10,
		);

		// Use WASM to calculate animation duration
		const easedDuration = this.wasmModule.easeInOutEasing(duration, duration);

		// Use setTimeout to handle animation completion
		setTimeout(() => {
			content.classList.remove(this.classes.animating);
			content.style.height = "";

			// Update data attribute for state persistency
			foldable.setAttribute(this.attrs.expanded, "true");

			// Dispatch custom event
			foldable.dispatchEvent(
				new CustomEvent("foldable:expanded", {
					bubbles: true,
					detail: { foldable },
				}),
			);
		}, easedDuration);
	}

	/**
	 * Ensure an element has an ID, generating one if needed
	 * @param element Element to ensure ID for
	 * @returns The element's ID
	 */
	private ensureId(element: Element): string {
		if (!element.id) {
			element.id = `foldable-content-${Math.random().toString(36).substr(2, 9)}`;
		}
		return element.id;
	}

	/**
	 * Handle content that's added dynamically via AJAX/HTMX
	 */
	private setupMutationObserver(): void {
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
				this.init();
			}
		});

		observer.observe(document.body, {
			childList: true,
			subtree: true,
		});
	}

	/**
	 * Setup HTMX content swap handlers
	 */
	private setupHtmxHandlers(): void {
		document.addEventListener("htmx:afterSwap", () => {
			this.init();
		});
	}

	/**
	 * Toggle a foldable element
	 * @param element Element within a foldable component
	 */
	public toggle(element: Element): void {
		const foldable = element.closest(this.selectors.foldable);
		if (foldable) {
			this.toggleFoldable(foldable);
		}
	}

	/**
	 * Expand a foldable element
	 * @param element Element within a foldable component
	 */
	public expand(element: Element): void {
		const foldable = element.closest(this.selectors.foldable);
		if (foldable) {
			const trigger = foldable.querySelector(
				this.selectors.trigger,
			) as HTMLElement;
			if (trigger && trigger.getAttribute("aria-expanded") === "false") {
				this.toggleFoldable(foldable);
			}
		}
	}

	/**
	 * Collapse a foldable element
	 * @param element Element within a foldable component
	 */
	public collapse(element: Element): void {
		const foldable = element.closest(this.selectors.foldable);
		if (foldable) {
			const trigger = foldable.querySelector(
				this.selectors.trigger,
			) as HTMLElement;
			if (trigger && trigger.getAttribute("aria-expanded") === "true") {
				this.toggleFoldable(foldable);
			}
		}
	}
}
