// AssemblyScript tests for core_audit.ts (as-proto)
import { AuditLogProto, AuditLogCollection, AuditLogUtils } from "./core_audit";

// Helper to create a sample audit log
function makeAuditLog(id: string, user: string, action: string, ts: string): AuditLogProto {
  return AuditLogUtils.createAuditLog(
    id, user, action, "object", "objid", "msg", "127.0.0.1", ts
  );
}

// Test encoding/decoding a single AuditLogProto
export function test_encode_decode_audit_log(): void {
  const log = makeAuditLog("1", "u1", "login", "2025-06-10T12:00:00Z");
  const encoded = AuditLogProto.encode(log);
  const decoded = AuditLogProto.decode(encoded);
  assert(decoded.id == log.id, "ID should match");
  assert(decoded.user_id == log.user_id, "User ID should match");
  assert(decoded.action == log.action, "Action should match");
  assert(decoded.timestamp == log.timestamp, "Timestamp should match");
}

// Test encoding/decoding a collection
export function test_encode_decode_audit_log_collection(): void {
  const c = new AuditLogCollection();
  c.addAuditLog(makeAuditLog("1", "u1", "login", "2025-06-10T12:00:00Z"));
  c.addAuditLog(makeAuditLog("2", "u2", "logout", "2025-06-10T13:00:00Z"));
  const encoded = AuditLogCollection.encode(c);
  const decoded = AuditLogCollection.decode(encoded);
  assert(decoded.count() == 2, "Should decode 2 audit logs");
  assert(decoded.getAuditLog(0)!.action == "login", "First action should be login");
  assert(decoded.getAuditLog(1)!.action == "logout", "Second action should be logout");
}

// Test filtering by action
export function test_filter_by_action(): void {
  const c = new AuditLogCollection();
  c.addAuditLog(makeAuditLog("1", "u1", "login", "2025-06-10T12:00:00Z"));
  c.addAuditLog(makeAuditLog("2", "u2", "logout", "2025-06-10T13:00:00Z"));
  c.addAuditLog(makeAuditLog("3", "u1", "login", "2025-06-10T14:00:00Z"));
  const filtered = c.filterByAction("login");
  assert(filtered.count() == 2, "Should filter 2 login actions");
}

// Test filtering by user
export function test_filter_by_user(): void {
  const c = new AuditLogCollection();
  c.addAuditLog(makeAuditLog("1", "u1", "login", "2025-06-10T12:00:00Z"));
  c.addAuditLog(makeAuditLog("2", "u2", "logout", "2025-06-10T13:00:00Z"));
  c.addAuditLog(makeAuditLog("3", "u1", "login", "2025-06-10T14:00:00Z"));
  const filtered = c.filterByUser("u1");
  assert(filtered.count() == 2, "Should filter 2 logs for user u1");
}

// Test most recent audit log
export function test_get_most_recent(): void {
  const c = new AuditLogCollection();
  c.addAuditLog(makeAuditLog("1", "u1", "login", "2025-06-10T12:00:00Z"));
  c.addAuditLog(makeAuditLog("2", "u2", "logout", "2025-06-10T15:00:00Z"));
  c.addAuditLog(makeAuditLog("3", "u1", "login", "2025-06-10T14:00:00Z"));
  const mostRecent = AuditLogUtils.getMostRecent(c);
  assert(mostRecent !== null && mostRecent!.id == "2", "Most recent should be id 2");
}
