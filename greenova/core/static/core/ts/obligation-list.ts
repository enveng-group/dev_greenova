// Obligation List Page Logic (TypeScript version)
import type { Type, Root } from "protobufjs";
import * as protobuf from "protobufjs/minimal";
import * as MechanismProto from "../js/proto/mechanism_pb";
import * as ObligationsProto from "../js/proto/obligations_pb";
import * as ProjectsProto from "../js/proto/projects_pb";
import * as ChartDataProto from "../js/proto/chart_data_pb";

declare global {
  interface Window {
    wasmModule: any;
    wasmReady: boolean;
    decodeObligationProtoWasm: (buffer: Uint8Array) => Promise<any>;
    OBLIGATIONS_API_URL: string;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  if (window.wasmReady) {
    initializeObligationList();
  } else {
    document.addEventListener("wasmReady", initializeObligationList);
  }

  function initializeObligationList() {
    const themeSelector = document.getElementById("theme-selector") as HTMLSelectElement;
    const applyThemeBtn = document.getElementById("apply-theme") as HTMLButtonElement;
    const obligationCount = document.getElementById("obligation-count");
    if (window.wasmModule) {
      const currentTheme = window.wasmModule.getTheme();
      themeSelector.value = currentTheme.toString();
    }
    function handleThemeChange() {
      const selectedTheme = parseInt(themeSelector.value, 10);
      if (window.wasmModule) {
        try {
          window.wasmModule.setTheme(selectedTheme);
          const resolvedTheme = window.wasmModule.resolveTheme(selectedTheme);
          document.documentElement.classList.remove("theme-light", "theme-dark");
          document.documentElement.classList.add(resolvedTheme === 0 ? "theme-light" : "theme-dark");
          showNotification("Theme updated successfully", "success");
        } catch (error) {
          console.error("Error applying theme:", error);
          showNotification("Error applying theme", "error");
        }
      }
    }
    applyThemeBtn.addEventListener("click", handleThemeChange);
    themeSelector.addEventListener("change", handleThemeChange);
    loadObligationsData();
    setInterval(loadObligationsData, 30000);
  }

  async function loadObligationsData() {
    const obligationCount = document.getElementById("obligation-count");
    if (obligationCount) {
      obligationCount.innerHTML = '<span class="loading-spinner"></span> Loading...';
    }
    try {
      // Use protobuf API endpoint for type safety
      const response = await fetch(window.OBLIGATIONS_API_URL + "?format=pb");
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const buffer = new Uint8Array(await response.arrayBuffer());
      const decoded = await window.decodeObligationProtoWasm(buffer);
      const obligations = decoded.obligations || [];
      updateObligationCount(obligations.length);
      updateObligationTable(obligations);
    } catch (error) {
      console.error("Error loading obligations:", error);
      if (obligationCount) {
        obligationCount.textContent = "Error";
      }
      showNotification("Failed to load obligations data", "error");
    }
  }

  function updateObligationCount(count: number) {
    const obligationCount = document.getElementById("obligation-count");
    if (obligationCount) {
      obligationCount.textContent = `${count} obligations`;
      obligationCount.classList.add("fade-in");
    }
  }

  function updateObligationTable(obligations: any[]) {
    const tableRows = document.querySelectorAll("#obligations-table tbody tr");
    if (window.wasmModule) {
      tableRows.forEach((row, index) => {
        const delay = window.wasmModule.linearEasing(index * 0.1, 1.0);
        setTimeout(() => {
          row.classList.add("row-highlight");
          setTimeout(() => row.classList.remove("row-highlight"), 1000);
        }, delay * 100);
      });
    }
    // TODO: Render obligations into the table if needed
  }

  function showNotification(message: string, type: "info" | "success" | "error" = "info") {
    const notification = document.createElement("div");
    notification.className = `alert alert-${type === "error" ? "danger" : type === "success" ? "success" : "info"} alert-dismissible fade show position-fixed greenova-notification`;
    notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }

  const filterForm = document.getElementById("filter-form") as HTMLFormElement;
  if (filterForm) {
    filterForm.addEventListener("submit", function (e) {
      const submitBtn = filterForm.querySelector("button[type='submit']") as HTMLButtonElement;
      if (submitBtn) {
        submitBtn.innerHTML = '<span class="loading-spinner"></span> Applying...';
        submitBtn.disabled = true;
      }
    });
  }

  // Optionally, call this on page load or when obligations need to be loaded
  // fetchAndDecodeObligations();
});

// Example: decode mechanism data from backend
function decodeMechanism(buffer: Uint8Array) {
  return MechanismProto.decodeObligationInsight(buffer);
}

// Example: encode mechanism data for backend
function encodeMechanism(mechanism: any) {
  return MechanismProto.encodeObligationInsight(mechanism);
}

// Example: decode obligation data from backend
function decodeObligationProto(buffer: Uint8Array) {
  return ObligationsProto.decodeObligationProto(buffer);
}

// Example: decode project data from backend
function decodeProjectProto(buffer: Uint8Array) {
  return ProjectsProto.decodeProjectProto(buffer);
}
