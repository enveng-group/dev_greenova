// shared/dom.ts
// Common DOM utilities for Greenova frontend

export function showNotification(message: string, type: "info" | "success" | "error" = "info"): void {
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
