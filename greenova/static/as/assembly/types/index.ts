// This file exports custom types and interfaces that are used throughout the AssemblyScript codebase.

/**
 * Theme options enum
 */
export enum Theme {
	LIGHT = 0,
	DARK = 1,
	AUTO = 2,
}

/**
 * Error code enum
 */
export enum ErrorCode {
	NONE = 0,
	GENERAL = 1,
	THEME = 2,
	ANIMATION = 3,
}

/**
 * Animation type enum
 */
export enum AnimationType {
	LINEAR = 0,
	EASE_IN_OUT = 1,
	EASE_IN = 2,
	EASE_OUT = 3,
}

/**
 * Animation configuration
 */
export class AnimationConfig {
	type: AnimationType;
	duration: f32;
	startValue: f32;
	endValue: f32;

	constructor(
		type: AnimationType = AnimationType.LINEAR,
		duration: f32 = 300.0,
		startValue: f32 = 0.0,
		endValue: f32 = 1.0,
	) {
		this.type = type;
		this.duration = duration;
		this.startValue = startValue;
		this.endValue = endValue;
	}
}

/**
 * Error details
 */
export class ErrorDetails {
	code: ErrorCode;
	message: string;
	timestamp: i64;

	constructor(code: ErrorCode = ErrorCode.NONE, message: string = "") {
		this.code = code;
		this.message = message;
		this.timestamp = i64(new Date().getTime());
	}
}
