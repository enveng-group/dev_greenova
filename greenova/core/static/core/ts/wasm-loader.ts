/**
 * WASM Loader for Greenova AssemblyScript Module (TypeScript version)
 * Integrates WebAssembly compiled from TypeScript for theme management and animations
 */

export {};

(window as any).wasmModule = null;
(window as any).wasmReady = false;

// WASM module loading and initialization
async function loadWasmModule(): Promise<any> {
  try {
    const wasmPath = "/static/core/as/build/release.wasm";
    const wasmModule = await WebAssembly.instantiateStreaming(fetch(wasmPath));
    const exports = wasmModule.instance.exports;

    (window as any).wasmModule = {
      // Theme management functions
      setTheme: exports.setTheme || (() => {}),
      getTheme: exports.getTheme || (() => 0),
      resolveTheme: exports.resolveTheme || ((prefersDark: number) => prefersDark ? 1 : 0),

      // Animation functions
      linearEasing: exports.linearEasing || ((t: number, d: number) => t / d),
      easeInOut: exports.easeInOut || ((t: number, d: number) => t / d),
      bounceEasing: exports.bounceEasing || ((t: number, d: number) => t / d),
      elasticEasing: exports.elasticEasing || ((t: number, d: number) => t / d),

      // Protobuf WASM integration functions
      decodeGreenovaObligationWasm: exports.decodeGreenovaObligationWasm || (() => 0),
      decodeProjectProtoWasm: exports.decodeProjectProtoWasm || (() => 0),
      decodeObligationProtoWasm: exports.decodeObligationProtoWasm || (() => 0),
      decodeChartDataProtoWasm: exports.decodeChartDataProtoWasm || (() => 0),

      // Memory management
      memory: exports.memory,
      __newString: exports.__newString,
      __getString: exports.__getString,
      __newArray: exports.__newArray,
      __getArray: exports.__getArray,
      Uint8Array_ID: exports.Uint8Array_ID,
    };

    (window as any).wasmReady = true;
    document.dispatchEvent(new CustomEvent("wasmReady"));
    console.log("WASM module loaded successfully with Protobuf3 support");
    return wasmModule;
  } catch (error) {
    console.warn("Failed to load WASM module, using fallback:", error);
    (window as any).wasmModule = createFallbackModule();
    (window as any).wasmReady = true;
    document.dispatchEvent(new CustomEvent("wasmReady"));
    return null;
  }
}

function createFallbackModule() {
  return {
    setTheme: (theme: number) => localStorage.setItem("theme", theme.toString()),
    getTheme: () => parseInt(localStorage.getItem("theme") || "2", 10),
    resolveTheme: (prefersDark: number) => prefersDark ? 1 : 0,
    linearEasing: (t: number, d: number) => t / d,
    easeInOut: (t: number, d: number) => {
      t /= d / 2;
      if (t < 1) return 0.5 * t * t;
      t--;
      return -0.5 * (t * (t - 2) - 1);
    },
    bounceEasing: (t: number, d: number) => Math.sin((t / d) * Math.PI),
    elasticEasing: (t: number, d: number) => Math.sin((t / d) * Math.PI * 2),
    decodeGreenovaObligationWasm: () => 0,
    decodeProjectProtoWasm: () => 0,
    decodeObligationProtoWasm: () => 0,
    decodeChartDataProtoWasm: () => 0,
  };
}

// WASM decode wrappers
(window as any).decodeObligationProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeObligationProtoWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.decodeObligationProtoWasm(ptr, buffer.length);
  return result;
};

(window as any).decodeGreenovaObligationWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeGreenovaObligationWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.decodeGreenovaObligationWasm(ptr, buffer.length);
  return result;
};

(window as any).decodeProjectProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeProjectProtoWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.decodeProjectProtoWasm(ptr, buffer.length);
  return result;
};

(window as any).decodeChartDataProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeChartDataProtoWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.decodeChartDataProtoWasm(ptr, buffer.length);
  return result;
};

function initializeTheme(): void {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  if ((window as any).wasmModule) {
    const currentTheme = (window as any).wasmModule.getTheme();
    const resolvedTheme = (window as any).wasmModule.resolveTheme(prefersDark ? 1 : 0);
    document.documentElement.classList.remove("theme-light", "theme-dark");
    document.documentElement.classList.add(resolvedTheme === 0 ? "theme-light" : "theme-dark");
  }
}

if (window.matchMedia) {
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", initializeTheme);
}

// Enhanced Animation utilities with Protobuf3 support
(window as any).GreenovaAnimation = {
  easeInOut: function(element: HTMLElement, duration = 300, callback?: () => void) {
    let start: number | null = null;
    const animate = (timestamp: number) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const easedProgress = (window as any).wasmModule ?
        (window as any).wasmModule.easeInOut(progress, 1.0) :
        progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;

      element.style.opacity = easedProgress.toString();

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else if (callback) {
        callback();
      }
    };
    requestAnimationFrame(animate);
  },

  fadeIn: function(element: HTMLElement, duration = 300) {
    element.style.opacity = "0";
    element.style.display = "block";
    this.easeInOut(element, duration, () => {
      element.style.opacity = "1";
    });
  },

  slideDown: function(element: HTMLElement, duration = 300) {
    const height = element.scrollHeight;
    element.style.height = "0px";
    element.style.overflow = "hidden";
    element.style.display = "block";

    let start: number | null = null;
    const animate = (timestamp: number) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const easedProgress = (window as any).wasmModule ?
        (window as any).wasmModule.linearEasing(progress, 1.0) : progress;

      element.style.height = (height * easedProgress) + "px";

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        element.style.height = "auto";
        element.style.overflow = "visible";
      }
    };
    requestAnimationFrame(animate);
  },
};

// Load WASM module immediately
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", loadWasmModule);
} else {
  loadWasmModule();
}
