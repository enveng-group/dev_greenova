/**
 * Theme Manager Module
 *
 * This module manages the application's theme system, handling:
 * - Theme switching (light/dark/auto)
 * - System preference detection
 * - Local storage persistence
 * - WASM-based theme calculations
 */

import type { GreenovaWasmModule } from "../utils/wasm-loader";

interface ThemeConfig {
	rootAttribute: string;
	localStorageKey: string;
	defaultScheme: string;
}

type ThemeScheme = "light" | "dark" | "auto";

export class ThemeManager {
	private readonly config: ThemeConfig;
	private readonly mediaQuery: MediaQueryList;
	private currentTheme: ThemeScheme;

	constructor(private readonly wasmModule: GreenovaWasmModule) {
		this.config = {
			rootAttribute: "data-theme",
			localStorageKey: "greenova-theme",
			defaultScheme: "auto",
		};
		this.mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
		this.currentTheme = this.getStoredTheme();
	}

	/**
	 * Initialize the theme manager
	 */
	public init(): void {
		try {
			const savedTheme = this.getStoredTheme();
			this.setThemeInWasm(savedTheme);
			this.applyTheme(savedTheme);
			this.setupSystemPreferenceListener();
			this.setupThemeToggleListeners();
		} catch (error) {
			console.error("Theme initialization failed:", error);
			this.applyThemeWithoutWasm("light");
		}
	}

	/**
	 * Apply theme without WASM support
	 */
	private applyThemeWithoutWasm(theme: ThemeScheme): void {
		const rootElement = document.documentElement;
		if (!rootElement) return;

		const effectiveTheme =
			theme === "auto"
				? this.getSystemPreference()
					? "dark"
					: "light"
				: theme;

		rootElement.setAttribute(this.config.rootAttribute, effectiveTheme);
		this.currentTheme = theme;
	}

	/**
	 * Get stored theme preference
	 */
	private getStoredTheme(): ThemeScheme {
		try {
			return (window.localStorage?.getItem(this.config.localStorageKey) ||
				this.config.defaultScheme) as ThemeScheme;
		} catch {
			return this.config.defaultScheme as ThemeScheme;
		}
	}

	/**
	 * Set theme in WASM module
	 */
	private setThemeInWasm(theme: ThemeScheme): void {
		try {
			const themeValue = this.getThemeValue(theme);
			this.wasmModule.setTheme(themeValue);
		} catch (error) {
			console.error("Failed to set theme in WASM:", error);
		}
	}

	/**
	 * Get theme value for WASM module
	 */
	private getThemeValue(theme: ThemeScheme): number {
		switch (theme) {
			case "light":
				return this.wasmModule.THEME_LIGHT;
			case "dark":
				return this.wasmModule.THEME_DARK;
			case "auto":
			default:
				return this.wasmModule.THEME_AUTO;
		}
	}

	/**
	 * Get system color scheme preference
	 */
	private getSystemPreference(): boolean {
		return this.mediaQuery?.matches ?? false;
	}

	/**
	 * Apply theme to document
	 */
	public applyTheme(theme: ThemeScheme): void {
		const rootElement = document.documentElement;
		if (!rootElement) return;

		try {
			if (theme === "auto") {
				const systemPrefersDark = this.getSystemPreference() ? 1 : 0;
				const resolvedTheme = this.wasmModule.resolveTheme(systemPrefersDark);
				rootElement.setAttribute(
					this.config.rootAttribute,
					resolvedTheme === this.wasmModule.THEME_DARK ? "dark" : "light",
				);
			} else {
				rootElement.setAttribute(this.config.rootAttribute, theme);
			}

			this.currentTheme = theme;
			this.dispatchThemeChangedEvent(theme);
		} catch (error) {
			console.error("Failed to apply theme:", error);
			this.applyThemeWithoutWasm(theme);
		}
	}

	/**
	 * Set up system preference change listener
	 */
	private setupSystemPreferenceListener(): void {
		if (!this.mediaQuery?.addEventListener) return;

		this.mediaQuery.addEventListener("change", () => {
			if (this.currentTheme === "auto") {
				this.applyTheme("auto");
			}
		});
	}

	/**
	 * Set up theme toggle button listeners
	 */
	private setupThemeToggleListeners(): void {
		document.querySelectorAll("[data-theme-toggle]").forEach((toggle) => {
			toggle.addEventListener("click", (e) => {
				e.preventDefault();
				const targetTheme = (toggle.getAttribute("data-theme-value") ||
					"auto") as ThemeScheme;
				this.setTheme(targetTheme);
			});
		});
	}

	/**
	 * Set and save theme preference
	 */
	public setTheme(theme: ThemeScheme): void {
		try {
			window.localStorage?.setItem(this.config.localStorageKey, theme);
			this.setThemeInWasm(theme);
			this.applyTheme(theme);
		} catch (error) {
			console.error("Failed to set theme:", error);
			this.applyThemeWithoutWasm(theme);
		}
	}

	/**
	 * Dispatch theme changed event
	 */
	private dispatchThemeChangedEvent(theme: ThemeScheme): void {
		try {
			window.dispatchEvent(
				new CustomEvent("themeChanged", {
					detail: { theme },
				}),
			);
		} catch (error) {
			console.error("Failed to dispatch theme changed event:", error);
		}
	}

	/**
	 * Get current theme
	 */
	public getCurrentTheme(): ThemeScheme {
		return this.currentTheme;
	}

	/**
	 * Toggle between light and dark themes
	 */
	public toggleTheme(): void {
		const currentTheme = this.getCurrentTheme();
		const newTheme: ThemeScheme = currentTheme === "light" ? "dark" : "light";
		this.setTheme(newTheme);
	}
}
