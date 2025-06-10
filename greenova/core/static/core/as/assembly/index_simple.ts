// AssemblyScript file (not standard TypeScript)
// Simple implementation for Greenova WASM module

export const ERROR_NONE: u8 = 0;
export const ERROR_GENERAL: u8 = 1;
export const ERROR_THEME: u8 = 2;
export const ERROR_ANIMATION: u8 = 3;

export const THEME_LIGHT: u8 = 0;
export const THEME_DARK: u8 = 1;

/**
 * Simple theme management function
 */
export function setTheme(theme: u8): u8 {
  if (theme > THEME_DARK) {
    return ERROR_THEME;
  }
  return ERROR_NONE;
}

/**
 * Simple animation calculation
 */
export function calculateAnimation(progress: f32): f32 {
  if (progress < 0.0 || progress > 1.0) {
    return 0.0;
  }
  return progress * progress; // Simple quadratic easing
}

/**
 * Simple data processing stub
 */
export function processData(data: i32): i32 {
  return data * 2;
}

/**
 * Simple math utilities
 */
export function add(a: i32, b: i32): i32 {
  return a + b;
}

export function multiply(a: f32, b: f32): f32 {
  return a * b;
}
