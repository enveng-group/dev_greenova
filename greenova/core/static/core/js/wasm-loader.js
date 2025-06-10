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
window.wasmModule = null;
window.wasmReady = false;
// WASM module loading and initialization
async function loadWasmModule() {
    try {
        const wasmPath = "/static/core/as/build/release.wasm";
        const wasmModule = await WebAssembly.instantiateStreaming(fetch(wasmPath));
        const exports = wasmModule.instance.exports;
        window.wasmModule = {
            // Theme management functions
            setTheme: exports.setTheme || (() => { }),
            getTheme: exports.getTheme || (() => 0),
            resolveTheme: exports.resolveTheme || ((prefersDark) => prefersDark ? 1 : 0),
            // Animation functions
            linearEasing: exports.linearEasing || ((t, d) => t / d),
            easeInOut: exports.easeInOut || ((t, d) => t / d),
            bounceEasing: exports.bounceEasing || ((t, d) => t / d),
            elasticEasing: exports.elasticEasing || ((t, d) => t / d),
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
        window.wasmReady = true;
        document.dispatchEvent(new CustomEvent("wasmReady"));
        console.log("WASM module loaded successfully with Protobuf3 support");
        return wasmModule;
    }
    catch (error) {
        console.warn("Failed to load WASM module, using fallback:", error);
        window.wasmModule = createFallbackModule();
        window.wasmReady = true;
        document.dispatchEvent(new CustomEvent("wasmReady"));
        return null;
    }
}
function createFallbackModule() {
    return {
        setTheme: (theme) => localStorage.setItem("theme", theme.toString()),
        getTheme: () => parseInt(localStorage.getItem("theme") || "2", 10),
        resolveTheme: (prefersDark) => prefersDark ? 1 : 0,
        linearEasing: (t, d) => t / d,
        easeInOut: (t, d) => {
            t /= d / 2;
            if (t < 1)
                return 0.5 * t * t;
            t--;
            return -0.5 * (t * (t - 2) - 1);
        },
        bounceEasing: (t, d) => Math.sin((t / d) * Math.PI),
        elasticEasing: (t, d) => Math.sin((t / d) * Math.PI * 2),
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
window.decodeObligationProtoWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeObligationProtoWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.decodeObligationProtoWasm(ptr, buffer.length);
    return result;
};
window.decodeGreenovaObligationWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeGreenovaObligationWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.decodeGreenovaObligationWasm(ptr, buffer.length);
    return result;
};
window.decodeProjectProtoWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeProjectProtoWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.decodeProjectProtoWasm(ptr, buffer.length);
    return result;
};
window.decodeChartDataProtoWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeChartDataProtoWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.decodeChartDataProtoWasm(ptr, buffer.length);
    return result;
};
window.decodeAuditLogProtoWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeAuditLogProtoWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.decodeAuditLogProtoWasm(ptr, buffer.length);
    return result;
};
window.decodeAuditLogCollectionWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeAuditLogCollectionWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.decodeAuditLogCollectionWasm(ptr, buffer.length);
    return result;
};
window.encodeAuditLogProtoWasm = async function (auditLog) {
    if (!window.wasmModule || !window.wasmModule.encodeAuditLogProtoWasm) {
        throw new Error("WASM module not loaded");
    }
    // Convert auditLog fields to strings as needed
    const ptr = window.wasmModule.encodeAuditLogProtoWasm(auditLog.id || "", auditLog.user_id || "", auditLog.action || "", auditLog.object_type || "", auditLog.object_id || "", auditLog.message || "", auditLog.ip_address || "", auditLog.timestamp || "");
    return ptr;
};
window.filterAuditLogsByActionWasm = async function (buffer, action) {
    if (!window.wasmModule || !window.wasmModule.filterAuditLogsByActionWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.filterAuditLogsByActionWasm(ptr, buffer.length, action);
    return result;
};
window.filterAuditLogsByUserWasm = async function (buffer, userId) {
    if (!window.wasmModule || !window.wasmModule.filterAuditLogsByUserWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const result = window.wasmModule.filterAuditLogsByUserWasm(ptr, buffer.length, userId);
    return result;
};
window.getAuditLogCountWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.getAuditLogCountWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    const count = window.wasmModule.getAuditLogCountWasm(ptr, buffer.length);
    return count;
};
// === Greenova Landing Protobuf WASM wrappers ===
window.decodeLandingPageContentWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeLandingPageContentWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    return window.wasmModule.decodeLandingPageContentWasm(ptr, buffer.length);
};
window.encodeLandingPageContentWasm = async function (content) {
    if (!window.wasmModule || !window.wasmModule.encodeLandingPageContentWasm) {
        throw new Error("WASM module not loaded");
    }
    // content: JS object with fields matching LandingPageContent
    return window.wasmModule.encodeLandingPageContentWasm(content);
};
window.decodeNewsletterSignupRequestWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeNewsletterSignupRequestWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    return window.wasmModule.decodeNewsletterSignupRequestWasm(ptr, buffer.length);
};
window.encodeNewsletterSignupRequestWasm = async function (req) {
    if (!window.wasmModule || !window.wasmModule.encodeNewsletterSignupRequestWasm) {
        throw new Error("WASM module not loaded");
    }
    // req: JS object with field 'email'
    return window.wasmModule.encodeNewsletterSignupRequestWasm(req.email || "");
};
window.decodeNewsletterSignupResponseWasm = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeNewsletterSignupResponseWasm) {
        throw new Error("WASM module not loaded");
    }
    const ptr = window.wasmModule.__newArray(window.wasmModule.Uint8Array_ID, buffer);
    return window.wasmModule.decodeNewsletterSignupResponseWasm(ptr, buffer.length);
};
window.encodeNewsletterSignupResponseWasm = async function (resp) {
    if (!window.wasmModule || !window.wasmModule.encodeNewsletterSignupResponseWasm) {
        throw new Error("WASM module not loaded");
    }
    // resp: JS object with fields 'success', 'message'
    return window.wasmModule.encodeNewsletterSignupResponseWasm(!!resp.success, resp.message || "");
};
// Real usage: encode a single audit log to protobuf using WASM
window.encodeAuditLogProto = async function (auditLog) {
    if (!window.wasmModule || !window.wasmModule.encodeAuditLogProto) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.encodeAuditLogProto(auditLog.id || "", auditLog.user_id || "", auditLog.action || "", auditLog.object_type || "", auditLog.object_id || "", auditLog.message || "", auditLog.ip_address || "", auditLog.timestamp || "");
};
// Real usage: decode a single audit log from protobuf using WASM
window.decodeAuditLogProto = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeAuditLogProto) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.decodeAuditLogProto(buffer);
};
// Real usage: encode a collection of audit logs to protobuf using WASM
window.encodeAuditLogCollection = async function (logs) {
    if (!window.wasmModule || !window.wasmModule.encodeAuditLogCollection) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.encodeAuditLogCollection(logs);
};
// Real usage: decode a collection of audit logs from protobuf using WASM
window.decodeAuditLogCollection = async function (buffer) {
    if (!window.wasmModule || !window.wasmModule.decodeAuditLogCollection) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.decodeAuditLogCollection(buffer);
};
// Real usage: filter audit logs by action using WASM
window.filterAuditLogsByAction = async function (logs, action) {
    if (!window.wasmModule || !window.wasmModule.filterAuditLogsByAction) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.filterAuditLogsByAction(logs, action);
};
// Real usage: filter audit logs by user using WASM
window.filterAuditLogsByUser = async function (logs, userId) {
    if (!window.wasmModule || !window.wasmModule.filterAuditLogsByUser) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.filterAuditLogsByUser(logs, userId);
};
// Real usage: get most recent audit log from a collection using WASM
window.getMostRecentAuditLog = async function (logs) {
    if (!window.wasmModule || !window.wasmModule.getMostRecentAuditLog) {
        throw new Error("WASM module not loaded");
    }
    return window.wasmModule.getMostRecentAuditLog(logs);
};
function initializeTheme() {
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
    easeInOut: function (element, duration = 300, callback) {
        let start = null;
        const animate = (timestamp) => {
            if (!start)
                start = timestamp;
            const progress = Math.min((timestamp - start) / duration, 1);
            const easedProgress = window.wasmModule ?
                window.wasmModule.easeInOut(progress, 1.0) :
                progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
            element.style.opacity = easedProgress.toString();
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
            else if (callback) {
                callback();
            }
        };
        requestAnimationFrame(animate);
    },
    fadeIn: function (element, duration = 300) {
        element.style.opacity = "0";
        element.style.display = "block";
        this.easeInOut(element, duration, () => {
            element.style.opacity = "1";
        });
    },
    slideDown: function (element, duration = 300) {
        const height = element.scrollHeight;
        element.style.height = "0px";
        element.style.overflow = "hidden";
        element.style.display = "block";
        let start = null;
        const animate = (timestamp) => {
            if (!start)
                start = timestamp;
            const progress = Math.min((timestamp - start) / duration, 1);
            const easedProgress = window.wasmModule ?
                window.wasmModule.linearEasing(progress, 1.0) : progress;
            element.style.height = (height * easedProgress) + "px";
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
            else {
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
}
else {
    loadWasmModule();
}
