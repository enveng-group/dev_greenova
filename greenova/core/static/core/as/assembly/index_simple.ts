// Simple AssemblyScript entry point for Greenova
// This file provides basic functionality without complex protobuf imports

/**
 * Theme constants
 */
export const THEME_LIGHT: u8 = 0;
export const THEME_DARK: u8 = 1;
export const THEME_AUTO: u8 = 2;

// Memory layout constants
const THEME_OFFSET: i32 = 0;
const ERROR_BUFFER_OFFSET: i32 = 8;

// Error codes
export const ERROR_NONE: u8 = 0;
export const ERROR_GENERAL: u8 = 1;
export const ERROR_THEME: u8 = 2;
export const ERROR_ANIMATION: u8 = 3;

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
 * Record an error
 */
export function recordError(code: u8, detail: u32): void {
  store<u8>(ERROR_BUFFER_OFFSET, code);
  store<u32>(ERROR_BUFFER_OFFSET + 1, detail);
}

/**
 * Get the last error
 */
export function getLastError(): u8 {
  return load<u8>(ERROR_BUFFER_OFFSET);
}

/**
 * Simple animation easing function
 */
export function easeInOut(current: f32, duration: f32): f32 {
  if (duration <= 0) {
    return 1.0;
  }

  const t = current / duration;
  if (t >= 1.0) {
    return 1.0;
  }

  return t * t * (3.0 - 2.0 * t);
}

/**
 * Basic math utility for animations
 */
export function lerp(start: f32, end: f32, t: f32): f32 {
  return start + (end - start) * t;
}
