import { fetchAuditLogs, fetchCoreData } from "./proto";
import { showNotification } from "../shared/dom";

// Example: fetch and display audit logs on page load
export async function initializeCoreAuditLog(): Promise<void> {
  try {
    const logs = await fetchAuditLogs();
    // TODO: Render logs into the DOM
    console.log("Loaded audit logs:", logs);
  } catch (err) {
    showNotification("Failed to load audit logs", "error");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initializeCoreAuditLog();
});
