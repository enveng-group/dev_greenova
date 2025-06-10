// AssemblyScript entry point for Greenova
// Simple implementation without complex protobuf dependencies

/**
 * Theme constants
 */
export const THEME_LIGHT: u8 = 0;
export const THEME_DARK: u8 = 1;
export const THEME_AUTO: u8 = 2;

// Error codes
export const ERROR_NONE: u8 = 0;
export const ERROR_GENERAL: u8 = 1;
export const ERROR_THEME: u8 = 2;
export const ERROR_ANIMATION: u8 = 3;

// Memory layout constants
const THEME_OFFSET: i32 = 0;
const ERROR_BUFFER_OFFSET: i32 = 8;

/**
 * Set the theme preference
 */
export function setTheme(theme: u8): void {
  if (theme > 2) {
    store<u8>(ERROR_BUFFER_OFFSET, ERROR_THEME);
    return;
  }
  store<u8>(THEME_OFFSET, theme);
}

/**
 * Get the current theme
 */
export function getTheme(): u8 {
  return load<u8>(THEME_OFFSET);
}

/**
 * Detect if system prefers dark mode
 */
export function resolveTheme(systemPrefersDark: i32): u8 {
  const theme = getTheme();
  if (theme === THEME_AUTO) {
    return systemPrefersDark ? THEME_DARK : THEME_LIGHT;
  }
  return theme;
}

/**
 * Record an error
 */
export function recordError(code: u8, details: u32): void {
  store<u8>(ERROR_BUFFER_OFFSET, code);
  store<u32>(ERROR_BUFFER_OFFSET + 1, details);
}

/**
 * Get the last error code
 */
export function getLastErrorCode(): u8 {
  return load<u8>(ERROR_BUFFER_OFFSET);
}

/**
 * Get the last error details
 */
export function getLastErrorDetails(): u32 {
  return load<u32>(ERROR_BUFFER_OFFSET + 1);
}

/**
 * Clear the last error
 */
export function clearError(): void {
  store<u8>(ERROR_BUFFER_OFFSET, ERROR_NONE);
  store<u32>(ERROR_BUFFER_OFFSET + 1, 0);
}

/**
 * Animation easing functions
 */
export function linearEasing(current: f32, duration: f32): f32 {
  if (current >= duration) return 1.0;
  if (current <= 0) return 0.0;
  return current / duration;
}

export function easeInOutEasing(current: f32, duration: f32): f32 {
  if (current >= duration) return 1.0;
  if (current <= 0) return 0.0;

  const progress = current / duration;
  if (progress < 0.5) {
    return 2.0 * progress * progress;
  } else {
    return 1.0 - f32(Math.pow(-2.0 * progress + 2.0, 2)) / 2.0;
  }
}

export function calculateAnimationHeight(
  isExpanding: boolean,
  progress: f32,
  startHeight: f32,
  endHeight: f32
): f32 {
  if (progress >= 1.0) return endHeight;
  if (progress <= 0.0) return startHeight;

  const heightDiff = endHeight - startHeight;
  const currentDiff = heightDiff * progress;
  return startHeight + currentDiff;
}

/**
 * Simple WASM interop stubs for protobuf processing
 * These just return the data length to indicate successful processing
 */
export function decodeGreenovaObligationWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeProjectProtoWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeObligationProtoWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeChartDataProtoWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeObligationInsightResponseWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeChartResponseWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeLandingPageContentWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeChartDataWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeAuditLogProtoWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function decodeAuditLogCollectionWasm(ptr: usize, len: i32): i32 {
  return len;
}

export function getAuditLogCountWasm(ptr: usize, len: i32): i32 {
  // Return a dummy count of 1 to indicate data was processed
  return 1;
}
