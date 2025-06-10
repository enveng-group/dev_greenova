/**
 * WASM Loader for Greenova AssemblyScript Module (TypeScript version)
 * Integrates WebAssembly compiled from TypeScript for theme management and animations
 */

import "./shared/api";
import "./shared/dom";
import "./shared/types";
import "./core/proto";
import "./core/index";
import "./landing/proto";
import "./landing/index";
import "./obligations/proto";
import "./obligations/index";

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

      // Audit log protobuf functions
      decodeAuditLogProtoWasm: exports.decodeAuditLogProtoWasm || (() => 0),
      decodeAuditLogCollectionWasm: exports.decodeAuditLogCollectionWasm || (() => 0),
      encodeAuditLogProtoWasm: exports.encodeAuditLogProtoWasm || (() => 0),
      filterAuditLogsByActionWasm: exports.filterAuditLogsByActionWasm || (() => 0),
      filterAuditLogsByUserWasm: exports.filterAuditLogsByUserWasm || (() => 0),
      getAuditLogCountWasm: exports.getAuditLogCountWasm || (() => 0),

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

    // Audit log fallback functions
    decodeAuditLogProtoWasm: () => 0,
    decodeAuditLogCollectionWasm: () => 0,
    encodeAuditLogProtoWasm: () => 0,
    filterAuditLogsByActionWasm: () => 0,
    filterAuditLogsByUserWasm: () => 0,
    getAuditLogCountWasm: () => 0,
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

(window as any).decodeAuditLogProtoWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeAuditLogProtoWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.decodeAuditLogProtoWasm(ptr, buffer.length);
  return result;
};

(window as any).decodeAuditLogCollectionWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeAuditLogCollectionWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.decodeAuditLogCollectionWasm(ptr, buffer.length);
  return result;
};

(window as any).encodeAuditLogProtoWasm = async function(auditLog: any): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.encodeAuditLogProtoWasm) {
    throw new Error("WASM module not loaded");
  }
  // Convert auditLog fields to strings as needed
  const ptr = (window as any).wasmModule.encodeAuditLogProtoWasm(
    auditLog.id || "",
    auditLog.user_id || "",
    auditLog.action || "",
    auditLog.object_type || "",
    auditLog.object_id || "",
    auditLog.message || "",
    auditLog.ip_address || "",
    auditLog.timestamp || ""
  );
  return ptr;
};

(window as any).filterAuditLogsByActionWasm = async function(buffer: Uint8Array, action: string): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.filterAuditLogsByActionWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.filterAuditLogsByActionWasm(ptr, buffer.length, action);
  return result;
};

(window as any).filterAuditLogsByUserWasm = async function(buffer: Uint8Array, userId: string): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.filterAuditLogsByUserWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const result = (window as any).wasmModule.filterAuditLogsByUserWasm(ptr, buffer.length, userId);
  return result;
};

(window as any).getAuditLogCountWasm = async function(buffer: Uint8Array): Promise<number> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.getAuditLogCountWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  const count = (window as any).wasmModule.getAuditLogCountWasm(ptr, buffer.length);
  return count;
};

// === Greenova Landing Protobuf WASM wrappers ===
(window as any).decodeLandingPageContentWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeLandingPageContentWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  return (window as any).wasmModule.decodeLandingPageContentWasm(ptr, buffer.length);
};

(window as any).encodeLandingPageContentWasm = async function(content: any): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.encodeLandingPageContentWasm) {
    throw new Error("WASM module not loaded");
  }
  // content: JS object with fields matching LandingPageContent
  return (window as any).wasmModule.encodeLandingPageContentWasm(content);
};

(window as any).decodeNewsletterSignupRequestWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeNewsletterSignupRequestWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  return (window as any).wasmModule.decodeNewsletterSignupRequestWasm(ptr, buffer.length);
};

(window as any).encodeNewsletterSignupRequestWasm = async function(req: any): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.encodeNewsletterSignupRequestWasm) {
    throw new Error("WASM module not loaded");
  }
  // req: JS object with field 'email'
  return (window as any).wasmModule.encodeNewsletterSignupRequestWasm(req.email || "");
};

(window as any).decodeNewsletterSignupResponseWasm = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeNewsletterSignupResponseWasm) {
    throw new Error("WASM module not loaded");
  }
  const ptr = (window as any).wasmModule.__newArray((window as any).wasmModule.Uint8Array_ID, buffer);
  return (window as any).wasmModule.decodeNewsletterSignupResponseWasm(ptr, buffer.length);
};

(window as any).encodeNewsletterSignupResponseWasm = async function(resp: any): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.encodeNewsletterSignupResponseWasm) {
    throw new Error("WASM module not loaded");
  }
  // resp: JS object with fields 'success', 'message'
  return (window as any).wasmModule.encodeNewsletterSignupResponseWasm(
    !!resp.success,
    resp.message || ""
  );
};

// Real usage: encode a single audit log to protobuf using WASM
(window as any).encodeAuditLogProto = async function(auditLog: any): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.encodeAuditLogProto) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.encodeAuditLogProto(
    auditLog.id || "",
    auditLog.user_id || "",
    auditLog.action || "",
    auditLog.object_type || "",
    auditLog.object_id || "",
    auditLog.message || "",
    auditLog.ip_address || "",
    auditLog.timestamp || ""
  );
};

// Real usage: decode a single audit log from protobuf using WASM
(window as any).decodeAuditLogProto = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeAuditLogProto) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.decodeAuditLogProto(buffer);
};

// Real usage: encode a collection of audit logs to protobuf using WASM
(window as any).encodeAuditLogCollection = async function(logs: any[]): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.encodeAuditLogCollection) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.encodeAuditLogCollection(logs);
};

// Real usage: decode a collection of audit logs from protobuf using WASM
(window as any).decodeAuditLogCollection = async function(buffer: Uint8Array): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.decodeAuditLogCollection) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.decodeAuditLogCollection(buffer);
};

// Real usage: filter audit logs by action using WASM
(window as any).filterAuditLogsByAction = async function(logs: any[], action: string): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.filterAuditLogsByAction) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.filterAuditLogsByAction(logs, action);
};

// Real usage: filter audit logs by user using WASM
(window as any).filterAuditLogsByUser = async function(logs: any[], userId: string): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.filterAuditLogsByUser) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.filterAuditLogsByUser(logs, userId);
};

// Real usage: get most recent audit log from a collection using WASM
(window as any).getMostRecentAuditLog = async function(logs: any[]): Promise<any> {
  if (!(window as any).wasmModule || !(window as any).wasmModule.getMostRecentAuditLog) {
    throw new Error("WASM module not loaded");
  }
  return (window as any).wasmModule.getMostRecentAuditLog(logs);
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
