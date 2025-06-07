/**
 * WASM Loader for Greenova AssemblyScript Module (TypeScript version)
 * Integrates WebAssembly compiled from TypeScript for theme management and animations
 */

import type { Root, Type } from "protobufjs";
import * as protobuf from "protobufjs/minimal";
import * as MechanismProto from "../js/proto/mechanism_pb";
import * as ObligationsProto from "../js/proto/obligations_pb";
import * as ProjectsProto from "../js/proto/projects_pb";
import * as ChartDataProto from "../js/proto/chart_data_pb";
import * as GreenovaDataProto from "../js/proto/greenova_data_pb";

// Declare global window extensions for type safety
declare global {
  interface Window {
    wasmModule: any;
    wasmReady: boolean;
    protobuf?: typeof import("protobufjs");
    decodeProtoWasm: (
      protoFile: string,
      messageType: string,
      buffer: Uint8Array,
      wasmFuncName?: string
    ) => Promise<any>;
    decodeObligationProtoWasm: (buffer: Uint8Array) => Promise<any>;
    decodeGreenovaObligationWasm: (buffer: Uint8Array) => Promise<any>;
    decodeProjectProtoWasm: (buffer: Uint8Array) => Promise<any>;
    decodeChartDataProtoWasm: (buffer: Uint8Array) => Promise<any>;
    GreenovaAnimation: any;
  }
}

window.wasmModule = null;
window.wasmReady = false;

// WASM module loading and initialization
async function loadWasmModule(): Promise<any> {
  try {
    const wasmPath = "/static/core/as/build/release.wasm";
    const wasmModule = await WebAssembly.instantiateStreaming(fetch(wasmPath));
    const exports = wasmModule.instance.exports;

    window.wasmModule = {
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
    };

    window.wasmReady = true;
    document.dispatchEvent(new CustomEvent("wasmReady"));
    console.log("WASM module loaded successfully with Protobuf3 support");
    return wasmModule;
  } catch (error) {
    console.warn("Failed to load WASM module, using fallback:", error);
    window.wasmModule = createFallbackModule();
    window.wasmReady = true;
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

// Protobuf3 integration functions for TypeScript/JS
window.decodeObligationProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  try {
    // Decode using the generated JS protobuf module
    const obligationCollection = ObligationsProto.decodeObligationCollection(buffer);

    // Optionally pass to WASM for additional processing
    if (window.wasmModule && window.wasmModule.decodeObligationProtoWasm) {
      window.wasmModule.decodeObligationProtoWasm(buffer.byteOffset, buffer.length);
    }

    return obligationCollection;
  } catch (error) {
    console.error("Error decoding obligation proto:", error);
    return { obligations: [], total_count: 0, error: String(error) };
  }
};

window.decodeGreenovaObligationWasm = async function(buffer: Uint8Array): Promise<any> {
  try {
    const obligation = GreenovaDataProto.decodeObligation(buffer);

    if (window.wasmModule && window.wasmModule.decodeGreenovaObligationWasm) {
      window.wasmModule.decodeGreenovaObligationWasm(buffer.byteOffset, buffer.length);
    }

    return obligation;
  } catch (error) {
    console.error("Error decoding greenova obligation:", error);
    return { id: 0, title: "", description: "", status: "", due_date: "", error: String(error) };
  }
};

window.decodeProjectProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  try {
    const project = ProjectsProto.decodeProjectProto(buffer);

    if (window.wasmModule && window.wasmModule.decodeProjectProtoWasm) {
      window.wasmModule.decodeProjectProtoWasm(buffer.byteOffset, buffer.length);
    }

    return project;
  } catch (error) {
    console.error("Error decoding project proto:", error);
    return { id: "", name: "", description: "", error: String(error) };
  }
};

window.decodeChartDataProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  try {
    const chartData = ChartDataProto.decodeChartData(buffer);

    if (window.wasmModule && window.wasmModule.decodeChartDataProtoWasm) {
      window.wasmModule.decodeChartDataProtoWasm(buffer.byteOffset, buffer.length);
    }

    return chartData;
  } catch (error) {
    console.error("Error decoding chart data proto:", error);
    return { charts: [], error: String(error) };
  }
};

function initializeTheme(): void {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  if (window.wasmModule) {
    const currentTheme = window.wasmModule.getTheme();
    const resolvedTheme = window.wasmModule.resolveTheme(prefersDark ? 1 : 0);
    document.documentElement.classList.remove("theme-light", "theme-dark");
    document.documentElement.classList.add(resolvedTheme === 0 ? "theme-light" : "theme-dark");
  }
}

if (window.matchMedia) {
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", initializeTheme);
}

// Enhanced Animation utilities with Protobuf3 support
window.GreenovaAnimation = {
  easeInOut: function(element: HTMLElement, duration = 300, callback?: () => void) {
    let start: number | null = null;
    const animate = (timestamp: number) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const easedProgress = window.wasmModule ?
        window.wasmModule.easeInOut(progress, 1.0) :
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
      const easedProgress = window.wasmModule ?
        window.wasmModule.linearEasing(progress, 1.0) : progress;

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

// Protobuf encode/decode utility functions using generated modules
export function decodeMechanism(buffer: Uint8Array) {
  return MechanismProto.decodeObligationInsight(buffer);
}

export function encodeMechanism(mechanism: any) {
  return MechanismProto.encodeObligationInsight(mechanism);
}

export function decodeObligation(buffer: Uint8Array) {
  return ObligationsProto.decodeObligationProto(buffer);
}

export function encodeObligation(obligation: any) {
  return ObligationsProto.encodeObligationProto(obligation);
}

export function decodeProject(buffer: Uint8Array) {
  return ProjectsProto.decodeProjectProto(buffer);
}

export function encodeProject(project: any) {
  return ProjectsProto.encodeProjectProto(project);
}

export function decodeChartData(buffer: Uint8Array) {
  return ChartDataProto.decodeChartData(buffer);
}

export function encodeChartData(chartData: any) {
  return ChartDataProto.encodeChartData(chartData);
}

// Load WASM module immediately
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", loadWasmModule);
} else {
  loadWasmModule();
}
