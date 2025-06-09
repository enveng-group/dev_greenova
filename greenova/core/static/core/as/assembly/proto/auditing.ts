// AssemblyScript Protobuf stubs for auditing.proto
// Generated for as-proto runtime
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class AuditRecord {
  id = "";
  user_id = "";
  action = "";
  timestamp = "";
  details = "";

  static encode(message: AuditRecord): Uint8Array {
    return Protobuf.encode<AuditRecord>(message, (m, w) => {
      if (m.id.length > 0) w.string(1, m.id);
      if (m.user_id.length > 0) w.string(2, m.user_id);
      if (m.action.length > 0) w.string(3, m.action);
      if (m.timestamp.length > 0) w.string(4, m.timestamp);
      if (m.details.length > 0) w.string(5, m.details);
    });
  }
  static decode(buffer: Uint8Array): AuditRecord {
    return Protobuf.decode<AuditRecord>(buffer, (r, l) => {
      const m = new AuditRecord();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.id = r.string(); break;
          case 2: m.user_id = r.string(); break;
          case 3: m.action = r.string(); break;
          case 4: m.timestamp = r.string(); break;
          case 5: m.details = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class AuditLog {
  records: Array<AuditRecord> = new Array<AuditRecord>();
  error = "";

  static encode(message: AuditLog): Uint8Array {
    return Protobuf.encode<AuditLog>(message, (m, w) => {
      for (let i = 0; i < m.records.length; i++) w.bytes(1, AuditRecord.encode(m.records[i]));
      if (m.error.length > 0) w.string(2, m.error);
    });
  }
  static decode(buffer: Uint8Array): AuditLog {
    return Protobuf.decode<AuditLog>(buffer, (r, l) => {
      const m = new AuditLog();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.records.push(AuditRecord.decode(r.bytes())); break;
          case 2: m.error = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
