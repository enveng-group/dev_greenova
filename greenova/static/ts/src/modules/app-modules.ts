/**
 * Greenova Application Modules
 *
 * TypeScript implementation of the original JavaScript modules from app.js.
 * This class provides the structure for all the application modules.
 */

// Module interfaces
interface ModuleInterface {
	init(): void;
	[key: string]: any;
}

/**
 * Core utilities module
 */
class CoreModule implements ModuleInterface {
	setupGlobalEventListeners(): void {
		// Handle flash messages with auto-dismiss
		const flashMessages = document.querySelectorAll(
			".message[data-auto-dismiss]",
		);
		flashMessages.forEach((message) => {
			setTimeout(() => {
				if (message instanceof HTMLElement && message.setAttribute) {
					message.setAttribute("classes", "add fade-out:0s, remove message:1s");
				}
			}, 5000); // 5 second delay before starting fade-out
		});
	}

	loadStylesheet(href: string, id?: string): void {
		const link = document.createElement("link");
		link.rel = "stylesheet";
		link.href = href;
		if (id) {
			link.id = id;
		}
		document.head.appendChild(link);
	}

	init(): void {
		// Initialize only if browser supports essential features
		if (!document.querySelector || !window.addEventListener) {
			console.warn("Browser unsupported, skipping JS initialization");
			return;
		}

		// Verify htmx is loaded
		if (typeof window.htmx === "undefined") {
			console.warn("HTMX not loaded");
		} else {
			console.log("HTMX loaded successfully");
		}

		// Set up global event listeners
		this.setupGlobalEventListeners();
	}
}

/**
 * Projects module
 */
class ProjectsModule implements ModuleInterface {
	init(): void {
		// Handle project selection changes
		document.addEventListener("change", (e: Event) => {
			const target = e.target as HTMLSelectElement;
			if (target && target.matches("#project-select")) {
				this.handleProjectChange(target.value);
			}
		});

		// Restore project selection when returning from another page
		this.restoreProjectSelection();

		// Update Add Obligation button to include the current project_id
		this.updateAddObligationButton();
	}

	handleProjectChange(projectId: string): void {
		// Store the selection in session storage
		if (projectId) {
			sessionStorage.setItem("lastProjectId", projectId);
		}

		// Trigger updates for data containers
		if (window.htmx) {
			window.htmx.trigger("#chart-container", "refreshCharts");
			window.htmx.trigger("#obligations-container", "refreshObligations");
		}

		// Update the Add Obligation button URL
		this.updateAddObligationButton();
	}

	restoreProjectSelection(): void {
		const projectSelect = document.getElementById(
			"project-select",
		) as HTMLSelectElement;
		const lastProjectId = sessionStorage.getItem("lastProjectId");

		if (projectSelect && lastProjectId) {
			projectSelect.value = lastProjectId;
			// Trigger change event to update dependent components
			projectSelect.dispatchEvent(new Event("change"));
		}
	}

	updateAddObligationButton(): void {
		const projectSelect = document.getElementById(
			"project-select",
		) as HTMLSelectElement;
		const addObligationBtn = document.querySelector(
			".add-obligation-btn",
		) as HTMLAnchorElement;

		if (projectSelect && addObligationBtn) {
			const projectId = projectSelect.value;
			if (projectId) {
				const currentHref = addObligationBtn.getAttribute("href") || "";
				const baseUrl = currentHref.split("?")[0];
				addObligationBtn.setAttribute(
					"href",
					`${baseUrl}?project_id=${projectId}`,
				);
			}
		}
	}
}

/**
 * Charts module
 */
class ChartsModule implements ModuleInterface {
	init(): void {
		// Set up chart scrolling functionality
		document.addEventListener("htmx:afterSettle", () => {
			const chartScroll = document.getElementById("chartScroll");
			if (chartScroll) {
				this.setupChartNavigation(chartScroll);
			}
		});
	}

	setupChartNavigation(container: HTMLElement): void {
		// Add keyboard navigation
		container.addEventListener("keydown", (e: KeyboardEvent) => {
			if (e.key === "ArrowLeft") {
				e.preventDefault();
				this.scrollCharts(container, "left");
			} else if (e.key === "ArrowRight") {
				e.preventDefault();
				this.scrollCharts(container, "right");
			}
		});
	}

	scrollCharts(container: HTMLElement, direction: "left" | "right"): void {
		if (!container) return;

		const scrollAmount = 320;
		container.scrollBy({
			left: direction === "left" ? -scrollAmount : scrollAmount,
			behavior: "smooth",
		});
	}
}

/**
 * Tables module
 */
class TablesModule implements ModuleInterface {
	init(): void {
		// Initial setup of table scrolling
		this.setupTableScrolling();

		// Listen for new content that may contain tables
		document.addEventListener("htmx:afterSettle", () =>
			this.setupTableScrolling(),
		);
	}

	setupTableScrolling(): void {
		const tableContainers = document.querySelectorAll(".table-container");
		tableContainers.forEach((container) => {
			const scrollArea = container.querySelector(
				".horizontal-scroll",
			) as HTMLElement;
			const scrollIndicator = container.querySelector(
				".scroll-indicator",
			) as HTMLElement;

			// Create scroll indicator if it doesn't exist
			if (scrollArea && !scrollIndicator) {
				const indicator = document.createElement("div");
				indicator.className = "scroll-indicator";

				const thumb = document.createElement("div");
				thumb.className = "scroll-thumb";
				indicator.appendChild(thumb);

				container.appendChild(indicator);

				// Update scroll indicator on scroll
				scrollArea.addEventListener("scroll", () =>
					this.updateScrollIndicator(scrollArea, thumb),
				);

				// Initial update
				this.updateScrollIndicator(scrollArea, thumb);
			}
		});
	}

	updateScrollIndicator(scrollArea: HTMLElement, thumb: HTMLElement): void {
		if (!scrollArea || !thumb) return;

		// Calculate thumb width and position
		const scrollWidth = scrollArea.scrollWidth;
		const viewportWidth = scrollArea.clientWidth;
		const scrollLeft = scrollArea.scrollLeft;

		const thumbWidth = (viewportWidth / scrollWidth) * 100;
		const thumbPosition =
			(scrollLeft / (scrollWidth - viewportWidth)) * (100 - thumbWidth);

		// Update thumb style
		thumb.style.width = `${thumbWidth}%`;
		thumb.style.marginLeft = `${thumbPosition}%`;
	}

	exportToCSV(table: HTMLTableElement, filename: string): void {
		if (!table) return;

		// Extract headers
		const rows = Array.from(table.querySelectorAll("tr"));
		const headers = Array.from(rows[0].querySelectorAll("th")).map(
			(cell) => `"${cell.textContent?.trim().replace(/"/g, '""') || ""}"`,
		);

		// Extract data rows
		const data = rows.slice(1).map((row) => {
			return Array.from(row.querySelectorAll("td")).map(
				(cell) => `"${cell.textContent?.trim().replace(/"/g, '""') || ""}"`,
			);
		});

		// Combine headers and data
		const csvContent = [
			headers.join(","),
			...data.map((row) => row.join(",")),
		].join("\n");

		// Create download link
		const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
		const url = URL.createObjectURL(blob);
		const link = document.createElement("a");

		link.setAttribute("href", url);
		link.setAttribute("download", filename);
		link.style.display = "none";

		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
}

/**
 * HTMX handlers module
 */
class HtmxHandlersModule implements ModuleInterface {
	init(): void {
		// Set up HTMX event handlers if HTMX is available
		if (typeof window.htmx === "undefined") return;

		// Setup loading states
		document.body.addEventListener("htmx:beforeRequest", (e: Event) => {
			const htmxEvent = e as CustomEvent;
			const target = htmxEvent.detail.target as HTMLElement;
			if (target.matches("#obligations-container, #chart-container")) {
				target.innerHTML =
					'<div class="notice" role="status" aria-busy="true">Loading...</div>';
			}
		});

		// Handle HTMX response errors
		document.body.addEventListener("htmx:responseError", (e: Event) => {
			const htmxEvent = e as CustomEvent;
			const target = htmxEvent.detail.target as HTMLElement;
			target.innerHTML = `
        <div class="notice error" role="alert">
          <p>Error loading data. Please try again.</p>
        </div>
      `;
		});

		// Handle obligation status changes
		document.addEventListener("htmx:afterSettle", (e: Event) => {
			const htmxEvent = e as CustomEvent;
			if (
				htmxEvent.detail.triggerSpec &&
				htmxEvent.detail.triggerSpec.includes("obligation:statusChanged")
			) {
				window.htmx.trigger("#chart-container", "refreshCharts");
			}
		});

		// Add entrance animations to newly swapped content
		document.body.addEventListener("htmx:afterSwap", (e: Event) => {
			const htmxEvent = e as CustomEvent;
			const target = htmxEvent.detail.target as HTMLElement;
			if (target.hasAttribute("data-animate-entrance")) {
				target.setAttribute("classes", "add fade-in");
			}
		});

		// Integration with PathDeps extension
		if (typeof window.PathDeps !== "undefined") {
			document.body.addEventListener("htmx:afterRequest", (e: Event) => {
				const htmxEvent = e as CustomEvent;

				// Only handle successful POST/PUT/DELETE requests (mutations)
				if (
					!htmxEvent.detail.successful ||
					htmxEvent.detail.xhr.method === "GET"
				)
					return;

				const path = htmxEvent.detail.requestConfig.path;
				if (path && path.includes("/obligations/")) {
					// Manually refresh related components
					if (window.PathDeps) {
						window.PathDeps.refresh("/obligations/");
						window.PathDeps.refresh("/mechanisms/charts/");
						window.PathDeps.refresh("/dashboard/overdue-count/");
					}
				}
			});
		}
	}
}

/**
 * Forms module
 */
class FormsModule implements ModuleInterface {
	init(): void {
		// Handle filter form submission
		document.addEventListener("submit", (e: Event) => {
			const target = e.target as HTMLFormElement;
			if (target.matches("#obligations-filter-form")) {
				e.preventDefault();
				this.handleFilterFormSubmit(target);
			}
		});

		// Set up filter removal handlers
		document.addEventListener("click", (e: Event) => {
			const target = e.target as HTMLElement;
			if (target.matches(".remove-filter")) {
				e.preventDefault();
				const type = target.getAttribute("data-filter-type");
				const value = target.getAttribute("data-filter-value");
				if (type && value) {
					this.removeFilter(type, value);
				}
			}
		});
	}

	handleFilterFormSubmit(form: HTMLFormElement): void {
		// Update UI elements related to filtering
		const filterCount = document.getElementById("filter-count");
		if (filterCount) {
			const activeFilters = Array.from(
				form.querySelectorAll('select, input[type="text"]'),
			).filter((el) => {
				const element = el as HTMLInputElement | HTMLSelectElement;
				return element.value && element.value !== "";
			}).length;

			filterCount.textContent = activeFilters.toString();
			filterCount.hidden = activeFilters === 0;
		}
	}

	removeFilter(type: string, value: string): void {
		const select = document.querySelector(
			`select[name="${type}"]`,
		) as HTMLSelectElement;
		if (select) {
			Array.from(select.options).forEach((option) => {
				if (option.value === value) {
					option.selected = false;
				}
			});
			select.dispatchEvent(new Event("change"));
		}
	}
}

/**
 * Document actions module
 */
class DocumentActionsModule implements ModuleInterface {
	init(): void {
		// Handle print button clicks
		document.addEventListener("click", (e: Event) => {
			const target = e.target as HTMLElement;
			if (target.matches("#print-obligations")) {
				e.preventDefault();
				window.print();
			}
		});

		// Handle export button clicks
		document.addEventListener("click", (e: Event) => {
			const target = e.target as HTMLElement;
			if (target.matches("#export-obligations")) {
				e.preventDefault();
				const table = document.querySelector("table") as HTMLTableElement;
				if (table) {
					const tablesModule = new TablesModule();
					tablesModule.exportToCSV(table, "obligations_export.csv");
				}
			}
		});

		// Handle obligation link clicks
		document.addEventListener("click", (e: Event) => {
			const target = e.target as HTMLElement;
			if (
				target.matches(".obligation-link") ||
				target.closest(".obligation-link")
			) {
				// Show loading indicator
				document.body.classList.add("loading");

				// Store the current project ID in session storage
				const projectId = document.querySelector<HTMLInputElement>(
					'input[name="project_id"]',
				)?.value;
				if (projectId) {
					sessionStorage.setItem("lastProjectId", projectId);
				}
			}
		});
	}
}

/**
 * AppModules class that contains all application modules
 */
export class AppModules {
	// Core is a special module imported directly
	core: CoreModule;
	projects: ProjectsModule;
	charts: ChartsModule;
	tables: TablesModule;
	htmxHandlers: HtmxHandlersModule;
	forms: FormsModule;
	documentActions: DocumentActionsModule;
	[key: string]: any;

	constructor() {
		this.core = new CoreModule();
		this.projects = new ProjectsModule();
		this.charts = new ChartsModule();
		this.tables = new TablesModule();
		this.htmxHandlers = new HtmxHandlersModule();
		this.forms = new FormsModule();
		this.documentActions = new DocumentActionsModule();
	}
}

// Augment global Window interface to include HTMX and PathDeps for TypeScript
declare global {
	interface Window {
		htmx: any;
		PathDeps?: {
			refresh: (path: string) => void;
		};
	}
}
