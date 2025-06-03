/**
 * WebAssembly Module Loader
 *
 * This utility handles loading and initializing the AssemblyScript WASM module
 * and provides a typed interface for interacting with it.
 */

/**
 * Interface for the WASM module exports
 */
export interface GreenovaWasmModule {
	memory: WebAssembly.Memory;
	getTheme: () => number;
	setTheme: (theme: number) => void;
	resolveTheme: (systemPrefersDark: number) => number;
	THEME_LIGHT: number;
	THEME_DARK: number;
	THEME_AUTO: number;
	getLastErrorCode: () => number;
	getLastErrorDetails: () => number;
	recordError: (code: number, details: number) => void;
	clearError: () => void;
	ERROR_NONE: number;
	ERROR_GENERAL: number;
	ERROR_THEME: number;
	ERROR_ANIMATION: number;
	linearEasing: (current: number, duration: number) => number;
	easeInOutEasing: (current: number, duration: number) => number;
	calculateAnimationHeight: (
		isExpanding: boolean,
		progress: number,
		startHeight: number,
		endHeight: number,
	) => number;
}

/**
 * Implementation of a fallback module when WASM is not available
 */
class FallbackWasmModule implements GreenovaWasmModule {
	memory: WebAssembly.Memory;
	THEME_LIGHT = 0;
	THEME_DARK = 1;
	THEME_AUTO = 2;
	ERROR_NONE = 0;
	ERROR_GENERAL = 1;
	ERROR_THEME = 2;
	ERROR_ANIMATION = 3;

	constructor() {
		this.memory = new WebAssembly.Memory({ initial: 1 });
	}

	getTheme(): number {
		return 0;
	}
	setTheme(): void {
		/* no-op */
	}
	resolveTheme(systemPrefersDark: number): number {
		return systemPrefersDark ? 1 : 0;
	}
	getLastErrorCode(): number {
		return 0;
	}
	getLastErrorDetails(): number {
		return 0;
	}
	recordError(): void {
		/* no-op */
	}
	clearError(): void {
		/* no-op */
	}
	linearEasing(current: number, duration: number): number {
		return current / duration;
	}
	easeInOutEasing(current: number, duration: number): number {
		return current / duration;
	}
	calculateAnimationHeight(): number {
		return 0;
	}
}

/**
 * Initialize the WebAssembly module with proper fallback
 */
export async function initializeWasmModule(): Promise<GreenovaWasmModule> {
	if (!isWasmSupported()) {
		console.warn("WebAssembly is not supported, using fallback module");
		return new FallbackWasmModule();
	}

	try {
		const wasmPath = new URL(
			"/static/as/build/optimized.wasm",
			window.location.origin,
		).href;
		const response = await fetchWithRetry(wasmPath);

		if (!response.ok) {
			throw new Error(`Failed to fetch WASM module: ${response.statusText}`);
		}

		const buffer = await response.arrayBuffer();
		if (!buffer) {
			throw new Error("Empty WASM buffer received");
		}

		const memory = new WebAssembly.Memory({
			initial: 2,
			maximum: 10,
		});

		const { instance } = await WebAssembly.instantiate(buffer, {
			env: {
				memory,
				abort: (
					message: number,
					fileName: number,
					lineNumber: number,
					columnNumber: number,
				) => {
					console.error("WASM module aborted:", {
						message,
						fileName,
						lineNumber,
						columnNumber,
					});
					throw new Error("WASM module aborted");
				},
			},
		});

		if (!instance?.exports) {
			throw new Error("WASM instance exports not found");
		}

		return instance.exports as unknown as GreenovaWasmModule;
	} catch (error) {
		console.error("WASM initialization failed:", error);
		console.warn("Falling back to JavaScript implementation");
		return new FallbackWasmModule();
	}
}

/**
 * Fetch with retry logic
 */
async function fetchWithRetry(
	url: string,
	retries = 3,
	backoff = 1000,
): Promise<Response> {
	let lastError: Error | undefined;

	for (let i = 0; i < retries; i++) {
		try {
			return await fetch(url);
		} catch (error) {
			lastError = error as Error;
			if (i === retries - 1) break;
			await new Promise((resolve) => setTimeout(resolve, backoff * (i + 1)));
		}
	}

	throw lastError || new Error("Failed to fetch after retries");
}

/**
 * Check if WebAssembly is supported in the current browser
 */
function isWasmSupported(): boolean {
	try {
		if (typeof WebAssembly !== "object") return false;

		// Check if required WebAssembly functions exist and are callable
		if (typeof WebAssembly.instantiate !== "function") return false;
		if (typeof WebAssembly.Memory !== "function") return false;
		if (typeof WebAssembly.compile !== "function") return false;
		if (typeof WebAssembly.Instance !== "function") return false;

		return true;
	} catch {
		return false;
	}
}
