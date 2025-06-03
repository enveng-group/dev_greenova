/**
 * Greenova Application TypeScript Entry Point
 *
 * This file serves as the main coordination point between:
 * 1. JavaScript modules that have been migrated to TypeScript
 * 2. The AssemblyScript WASM module for performance-critical operations
 * 3. The DOM and browser environment
 */

import { AppModules } from "./modules/app-modules";
import { ErrorHandler } from "./modules/error-handler";
import { Foldable } from "./modules/foldable";
import { ThemeManager } from "./modules/theme-manager";
import { initializeWasmModule } from "./utils/wasm-loader";

// Module interfaces
interface GreenovaApp {
	core: {
		init: () => void;
		loadStylesheet: (href: string, id?: string) => void;
	};
	modules: AppModules;
	errorHandler: ErrorHandler;
	foldable: Foldable;
	theme: ThemeManager;
}

/**
 * Initialize the application when WASM is ready
 */
async function initializeApp(): Promise<GreenovaApp | void> {
	try {
		// Load WASM module first for critical operations
		const wasmModule = await initializeWasmModule();

		// Create the main application object
		const app: GreenovaApp = {
			core: {
				init: () => {
					console.log("Greenova application initialized");

					// Initialize all modules
					Object.keys(app.modules).forEach((module) => {
						if (
							module !== "core" &&
							typeof app.modules[module]?.init === "function"
						) {
							try {
								app.modules[module].init();
							} catch (err) {
								app.errorHandler.reportError(
									`Error initializing module ${module}:`,
									err as Record<string, unknown>,
								);
							}
						}
					});

					// Set up global event listeners
					document.addEventListener("htmx:afterSettle", () => {
						// Re-initialize modules on htmx content changes
						app.foldable.init();
					});
				},

				loadStylesheet: (href: string, id?: string): void => {
					const link = document.createElement("link");
					link.rel = "stylesheet";
					link.href = href;
					if (id) {
						link.id = id;
					}
					document.head.appendChild(link);
				},
			},
			modules: new AppModules(),
			errorHandler: new ErrorHandler(wasmModule),
			foldable: new Foldable(wasmModule),
			theme: new ThemeManager(wasmModule),
		};

		// Initialize the error handler first
		app.errorHandler.init();

		// Initialize theme early to prevent flash
		app.theme.init();

		// Export the app to global scope
		window.GreenovaApp = app;

		// Initialize the core application
		app.core.init();

		return app;
	} catch (err) {
		console.error("Failed to initialize application:", err);

		// Fallback to traditional JS if WASM fails
		const legacyScripts = [
			"/static/js/modules/error-handler.js",
			"/static/js/modules/theme-init.js",
			"/static/js/modules/foldable.js",
			"/static/js/app.js",
		];

		// Load the legacy JavaScript as fallback
		legacyScripts.forEach((script) => {
			const scriptEl = document.createElement("script");
			scriptEl.src = script;
			document.body.appendChild(scriptEl);
		});
	}
}

// Initialize the application when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
	initializeApp().catch((err) => {
		console.error("Critical application initialization error:", err);
	});
});

// Type declaration for global app object
declare global {
	interface Window {
		GreenovaApp: GreenovaApp;
	}
}

export { ThemeManager } from "./modules/theme-manager";
/**
 * Entry point for Greenova TypeScript modules
 */
export { initializeWasmModule } from "./utils/wasm-loader";
