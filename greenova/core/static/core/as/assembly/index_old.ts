// AssemblyScript entry point for Greenova
// Simple implementation without complex protobuf dependencies

/**
 * Greenova AssemblyScript Core Implementation
 *
 * This module provides high-performance implementations for:
 * 1. Theme management
 * 2. Animation calculations
 * 3. Error handling core
 * 4. Protobuf3 obligations processing
 */

// Memory layout constants
const THEME_OFFSET: i32 = 0;         // 1 byte for theme (0=light, 1=dark, 2=auto)
const ERROR_BUFFER_OFFSET: i32 = 8;  // Start of error buffer (64 bytes)
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
    return 1.0 - f32(Math.pow(-2.0 * progress + 2.0, 2)) / 2.0;
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
  endHeight: f32
): f32 {
  if (progress >= 1.0) return endHeight;
  if (progress <= 0.0) return startHeight;

  const heightDiff = endHeight - startHeight;
  const currentDiff = heightDiff * progress;

  return startHeight + currentDiff;
}

/**
 * Protobuf Integration Stub
 * Simple WASM interop functions for Protobuf3 data processing
 * These functions provide a bridge between JS and WASM for high-performance data processing
 */

/**
 * WASM interop function for decoding greenova_data.proto Obligation
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeGreenovaObligationWasm(ptr: usize, len: i32): i32 {
  // Stub implementation - returns data length for JS to handle
  return len;
}

/**
 * WASM interop function for decoding projects.proto ProjectProto
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeProjectProtoWasm(ptr: usize, len: i32): i32 {
  // Stub implementation - returns data length for JS to handle
  return len;
}

/**
 * WASM interop function for decoding obligations.proto ObligationProto
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data using ObligationProto.decode
 */
export function decodeObligationProtoWasm(ptr: usize, len: i32): i32 {
  // Get the binary data from memory
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }

  // Decode using our ObligationProto class
  const obligation = ObligationProto.decode(data);

  // For now, just return the length to indicate successful processing
  // In a real implementation, you might store the decoded object somewhere
  return len;
}

/**
 * WASM interop function for decoding chart_data.proto ChartData
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeChartDataProtoWasm(ptr: usize, len: i32): i32 {
  // Stub implementation - returns data length for JS to handle
  return len;
}

/**
 * WASM interop function for decoding mechanism.proto ObligationInsightResponse
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeObligationInsightResponseWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const response = ObligationInsightResponse.decode(data);
  return len;
}

/**
 * WASM interop function for decoding mechanism.proto ChartResponse
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeChartResponseWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const response = ChartResponse.decode(data);
  return len;
}

/**
 * WASM interop function for decoding landing.proto LandingPageContent
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeLandingPageContentWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const content = LandingPageContent.decode(data);
  return len;
}

/**
 * WASM interop function for decoding chart_data.proto ChartData
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data (stub implementation)
 */
export function decodeChartDataWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const chart = ChartDataProto.decode(data);
  return len;
}

/**
 * WASM interop function for decoding core_audit.proto AuditLogProto
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data using AuditLogProto.decode
 */
export function decodeAuditLogProtoWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const auditLog = AuditLogProto.decode(data);
  return len;
}

/**
 * WASM interop function for decoding core_audit.proto AuditLogCollection
 * @param ptr Pointer to protobuf binary data
 * @param len Length of binary data
 * @returns Length of processed data using AuditLogCollection.decode
 */
export function decodeAuditLogCollectionWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const collection = AuditLogCollection.decode(data);
  return len;
}

/**
 * WASM interop function for encoding AuditLogProto to protobuf binary
 * @param id Audit log ID
 * @param userId User ID
 * @param action Action performed
 * @param objectType Object type affected
 * @param objectId Object ID affected
 * @param message Audit log message
 * @param ipAddress IP address
 * @param timestamp Timestamp
 * @returns Pointer to encoded binary data
 */
export function encodeAuditLogProtoWasm(
  id: string,
  userId: string,
  action: string,
  objectType: string,
  objectId: string,
  message: string,
  ipAddress: string,
  timestamp: string
): usize {
  const auditLog = AuditLogUtils.createAuditLog(
    id, userId, action, objectType, objectId, message, ipAddress, timestamp
  );
  const encoded = AuditLogProto.encode(auditLog);
  // Return pointer to the encoded data for JS to retrieve
  return changetype<usize>(encoded.buffer);
}

/**
 * Filter audit logs by action using WASM processing
 * @param ptr Pointer to AuditLogCollection protobuf binary data
 * @param len Length of binary data
 * @param action Action to filter by
 * @returns Length of filtered collection
 */
export function filterAuditLogsByActionWasm(ptr: usize, len: i32, action: string): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const collection = AuditLogCollection.decode(data);
  const filtered = collection.filterByAction(action);
  const encoded = AuditLogCollection.encode(filtered);
  return encoded.length;
}

/**
 * Filter audit logs by user using WASM processing
 * @param ptr Pointer to AuditLogCollection protobuf binary data
 * @param len Length of binary data
 * @param userId User ID to filter by
 * @returns Length of filtered collection
 */
export function filterAuditLogsByUserWasm(ptr: usize, len: i32, userId: string): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const collection = AuditLogCollection.decode(data);
  const filtered = collection.filterByUser(userId);
  const encoded = AuditLogCollection.encode(filtered);
  return encoded.length;
}

/**
 * Get audit log count from collection using WASM processing
 * @param ptr Pointer to AuditLogCollection protobuf binary data
 * @param len Length of binary data
 * @returns Number of audit logs in the collection
 */
export function getAuditLogCountWasm(ptr: usize, len: i32): i32 {
  const data = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    data[i] = load<u8>(ptr + i);
  }
  const collection = AuditLogCollection.decode(data);
  return collection.count();
}

/**
 * Encode a single AuditLogProto to protobuf binary (real usage)
 */
export function encodeAuditLogProto(
  id: string,
  userId: string,
  action: string,
  objectType: string,
  objectId: string,
  message: string,
  ipAddress: string,
  timestamp: string
): Uint8Array {
  const auditLog = AuditLogUtils.createAuditLog(
    id, userId, action, objectType, objectId, message, ipAddress, timestamp
  );
  return AuditLogProto.encode(auditLog);
}

/**
 * Decode a single AuditLogProto from protobuf binary (real usage)
 */
export function decodeAuditLogProto(buffer: Uint8Array): AuditLogProto {
  return AuditLogProto.decode(buffer);
}

/**
 * Encode a collection of AuditLogProto to protobuf binary (real usage)
 */
export function encodeAuditLogCollection(logs: Array<AuditLogProto>): Uint8Array {
  const collection = new AuditLogCollection();
  for (let i = 0; i < logs.length; i++) {
    collection.addAuditLog(logs[i]);
  }
  return AuditLogCollection.encode(collection);
}

/**
 * Decode a collection of AuditLogProto from protobuf binary (real usage)
 */
export function decodeAuditLogCollection(buffer: Uint8Array): AuditLogCollection {
  return AuditLogCollection.decode(buffer);
}

/**
 * Filter audit logs by action (real usage)
 */
export function filterAuditLogsByAction(
  logs: Array<AuditLogProto>,
  action: string
): Array<AuditLogProto> {
  const collection = new AuditLogCollection();
  for (let i = 0; i < logs.length; i++) {
    collection.addAuditLog(logs[i]);
  }
  const filtered = collection.filterByAction(action);
  return filtered.audit_logs;
}

/**
 * Filter audit logs by user (real usage)
 */
export function filterAuditLogsByUser(
  logs: Array<AuditLogProto>,
  userId: string
): Array<AuditLogProto> {
  const collection = new AuditLogCollection();
  for (let i = 0; i < logs.length; i++) {
    collection.addAuditLog(logs[i]);
  }
  const filtered = collection.filterByUser(userId);
  return filtered.audit_logs;
}

/**
 * Get the most recent audit log from a collection (real usage)
 */
export function getMostRecentAuditLog(logs: Array<AuditLogProto>): AuditLogProto | null {
  const collection = new AuditLogCollection();
  for (let i = 0; i < logs.length; i++) {
    collection.addAuditLog(logs[i]);
  }
  return AuditLogUtils.getMostRecent(collection);
}
