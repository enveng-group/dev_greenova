// filepath: /assemblyscript-project/assembly/index.ts
// This file serves as the main entry point for the AssemblyScript code.
// It exports functions and types that can be used in other parts of the project.

/**
 * Greenova AssemblyScript Core Implementation
 *
 * This module provides high-performance implementations for:
 * 1. Theme management
 * 2. Animation calculations
 * 3. Error handling core
 */

// Memory layout constants
const THEME_OFFSET: i32 = 0; // 1 byte for theme (0=light, 1=dark, 2=auto)
const ERROR_BUFFER_OFFSET: i32 = 8; // Start of error buffer (64 bytes)
const ANIMATION_DATA_OFFSET: i32 = 72; // Start of animation data

// Error codes
export const ERROR_NONE: u8 = 0;
export const ERROR_GENERAL: u8 = 1;
export const ERROR_THEME: u8 = 2;
export const ERROR_ANIMATION: u8 = 3;

/**
 * Theme constants
 */
export const THEME_LIGHT: u8 = 0;
export const THEME_DARK: u8 = 1;
export const THEME_AUTO: u8 = 2;

/**
 * Set the theme preference
 * @param theme Theme value (0=light, 1=dark, 2=auto)
 */
export function setTheme(theme: u8): void {
	if (theme > 2) {
		recordError(ERROR_THEME, 0);
		return;
	}
	store<u8>(THEME_OFFSET, theme);
}

/**
 * Get the current theme preference
 * @returns Theme value (0=light, 1=dark, 2=auto)
 */
export function getTheme(): u8 {
	return load<u8>(THEME_OFFSET);
}

/**
 * Detect if system prefers dark mode based on input parameter
 * We take this as an input because WASM can't directly access browser APIs
 * @param systemPrefersDark 1 if system prefers dark, 0 otherwise
 * @returns Resolved theme (0=light, 1=dark)
 */
export function resolveTheme(systemPrefersDark: i32): u8 {
	const theme = getTheme();
	if (theme === THEME_AUTO) {
		return systemPrefersDark ? THEME_DARK : THEME_LIGHT;
	}
	return theme;
}

/**
 * Record an error in the error buffer
 * @param code Error code
 * @param details Additional error details
 */
export function recordError(code: u8, details: u32): void {
	store<u8>(ERROR_BUFFER_OFFSET, code);
	store<u32>(ERROR_BUFFER_OFFSET + 1, details);
}

/**
 * Get the last error code
 * @returns Error code
 */
export function getLastErrorCode(): u8 {
	return load<u8>(ERROR_BUFFER_OFFSET);
}

/**
 * Get the last error details
 * @returns Error details
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
 * Animation calculations
 */

/**
 * Calculate linear animation progress
 * @param current Current time in animation
 * @param duration Total duration of animation
 * @returns Progress value from 0 to 1
 */
export function linearEasing(current: f32, duration: f32): f32 {
	if (current >= duration) return 1.0;
	if (current <= 0) return 0.0;
	return current / duration;
}

/**
 * Calculate easeInOut animation progress
 * @param current Current time in animation
 * @param duration Total duration of animation
 * @returns Progress value from 0 to 1
 */
export function easeInOutEasing(current: f32, duration: f32): f32 {
	if (current >= duration) return 1.0;
	if (current <= 0) return 0.0;

	const progress = current / duration;

	if (progress < 0.5) {
		return 2.0 * progress * progress;
	} else {
		return 1.0 - f32((-2.0 * progress + 2.0) ** 2) / 2.0;
	}
}

/**
 * Calculate animation height value for collapsible elements
 * @param isExpanding Whether the animation is expanding (true) or collapsing (false)
 * @param progress Animation progress from 0 to 1
 * @param startHeight Starting height
 * @param endHeight Target height
 * @returns Current height value
 */
export function calculateAnimationHeight(
	isExpanding: boolean,
	progress: f32,
	startHeight: f32,
	endHeight: f32,
): f32 {
	if (progress >= 1.0) return endHeight;
	if (progress <= 0.0) return startHeight;

	const heightDiff = endHeight - startHeight;
	const currentDiff = heightDiff * progress;

	return startHeight + currentDiff;
}

/**
 * Basic arithmetic functions
 */

/**
 * Add two integers
 * @param a First integer
 * @param b Second integer
 * @returns Sum of a and b
 */
export function add(a: i32, b: i32): i32 {
	return a + b;
}

/**
 * Subtract two integers
 * @param a First integer
 * @param b Second integer
 * @returns Difference of a and b
 */
export function subtract(a: i32, b: i32): i32 {
	return a - b;
}
