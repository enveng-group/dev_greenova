// AssemblyScript Protobuf stubs for core_audit.proto
// Generated for as-proto runtime to match server-side implementation

import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

/**
 * Audit log entry for the core app (client-side)
 * Mirrors the server-side AuditLogProto message
 */
export class AuditLogProto {
  id = "";
  user_id = "";
  action = "";
  object_type = "";
  object_id = "";
  message = "";
  ip_address = "";
  timestamp = "";

  static encode(message: AuditLogProto): Uint8Array {
    return Protobuf.encode<AuditLogProto>(message, (message: AuditLogProto, writer: Writer) => {
      if (message.id.length > 0) writer.string(1, message.id);
      if (message.user_id.length > 0) writer.string(2, message.user_id);
      if (message.action.length > 0) writer.string(3, message.action);
      if (message.object_type.length > 0) writer.string(4, message.object_type);
      if (message.object_id.length > 0) writer.string(5, message.object_id);
      if (message.message.length > 0) writer.string(6, message.message);
      if (message.ip_address.length > 0) writer.string(7, message.ip_address);
      if (message.timestamp.length > 0) writer.string(8, message.timestamp);
    });
  }

  static decode(buffer: Uint8Array): AuditLogProto {
    return Protobuf.decode<AuditLogProto>(buffer, AuditLogProto.decodeInner);
  }

  static decodeInner(message: AuditLogProto, reader: Reader): AuditLogProto {
    const end = reader.pos + reader.uint32();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          message.id = reader.string();
          break;
        case 2:
          message.user_id = reader.string();
          break;
        case 3:
          message.action = reader.string();
          break;
        case 4:
          message.object_type = reader.string();
          break;
        case 5:
          message.object_id = reader.string();
          break;
        case 6:
          message.message = reader.string();
          break;
        case 7:
          message.ip_address = reader.string();
          break;
        case 8:
          message.timestamp = reader.string();
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  }

  /**
   * Convert to a plain object for JavaScript interop
   */
  toObject(): any {
    return {
      id: this.id,
      user_id: this.user_id,
      action: this.action,
      object_type: this.object_type,
      object_id: this.object_id,
      message: this.message,
      ip_address: this.ip_address,
      timestamp: this.timestamp,
    };
  }

  /**
   * Create from a plain object
   */
  static fromObject(obj: any): AuditLogProto {
    const message = new AuditLogProto();
    if (obj.id) message.id = obj.id;
    if (obj.user_id) message.user_id = obj.user_id;
    if (obj.action) message.action = obj.action;
    if (obj.object_type) message.object_type = obj.object_type;
    if (obj.object_id) message.object_id = obj.object_id;
    if (obj.message) message.message = obj.message;
    if (obj.ip_address) message.ip_address = obj.ip_address;
    if (obj.timestamp) message.timestamp = obj.timestamp;
    return message;
  }
}

/**
 * Collection of audit log entries (client-side)
 * Mirrors the server-side AuditLogCollection message
 */
export class AuditLogCollection {
  audit_logs: Array<AuditLogProto> = new Array<AuditLogProto>();

  static encode(message: AuditLogCollection): Uint8Array {
    return Protobuf.encode<AuditLogCollection>(message, (message: AuditLogCollection, writer: Writer) => {
      for (let i = 0; i < message.audit_logs.length; i++) {
        writer.bytes(1, AuditLogProto.encode(message.audit_logs[i]));
      }
    });
  }

  static decode(buffer: Uint8Array): AuditLogCollection {
    return Protobuf.decode<AuditLogCollection>(buffer, AuditLogCollection.decodeInner);
  }

  static decodeInner(message: AuditLogCollection, reader: Reader): AuditLogCollection {
    const end = reader.pos + reader.uint32();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          const audit_log = new AuditLogProto();
          reader.bytes(audit_log, AuditLogProto.decodeInner);
          message.audit_logs.push(audit_log);
          break;
        default:
          reader.skipType(tag & 7);
          break;
      }
    }
    return message;
  }

  /**
   * Convert to a plain object for JavaScript interop
   */
  toObject(): any {
    const result: any = {
      audit_logs: new Array<any>(),
    };
    for (let i = 0; i < this.audit_logs.length; i++) {
      result.audit_logs.push(this.audit_logs[i].toObject());
    }
    return result;
  }

  /**
   * Create from a plain object
   */
  static fromObject(obj: any): AuditLogCollection {
    const message = new AuditLogCollection();
    if (obj.audit_logs && obj.audit_logs.length > 0) {
      for (let i = 0; i < obj.audit_logs.length; i++) {
        message.audit_logs.push(AuditLogProto.fromObject(obj.audit_logs[i]));
      }
    }
    return message;
  }

  /**
   * Get the count of audit logs
   */
  count(): i32 {
    return this.audit_logs.length;
  }

  /**
   * Add an audit log to the collection
   */
  addAuditLog(auditLog: AuditLogProto): void {
    this.audit_logs.push(auditLog);
  }

  /**
   * Get audit log by index
   */
  getAuditLog(index: i32): AuditLogProto | null {
    if (index < 0 || index >= this.audit_logs.length) {
      return null;
    }
    return this.audit_logs[index];
  }

  /**
   * Filter audit logs by action
   */
  filterByAction(action: string): AuditLogCollection {
    const filtered = new AuditLogCollection();
    for (let i = 0; i < this.audit_logs.length; i++) {
      if (this.audit_logs[i].action === action) {
        filtered.addAuditLog(this.audit_logs[i]);
      }
    }
    return filtered;
  }

  /**
   * Filter audit logs by user_id
   */
  filterByUser(userId: string): AuditLogCollection {
    const filtered = new AuditLogCollection();
    for (let i = 0; i < this.audit_logs.length; i++) {
      if (this.audit_logs[i].user_id === userId) {
        filtered.addAuditLog(this.audit_logs[i]);
      }
    }
    return filtered;
  }

  /**
   * Filter audit logs by object_type
   */
  filterByObjectType(objectType: string): AuditLogCollection {
    const filtered = new AuditLogCollection();
    for (let i = 0; i < this.audit_logs.length; i++) {
      if (this.audit_logs[i].object_type === objectType) {
        filtered.addAuditLog(this.audit_logs[i]);
      }
    }
    return filtered;
  }
}

/**
 * Utility functions for audit log processing
 */
export class AuditLogUtils {
  /**
   * Create a new audit log entry
   */
  static createAuditLog(
    id: string,
    userId: string,
    action: string,
    objectType: string,
    objectId: string,
    message: string,
    ipAddress: string,
    timestamp: string
  ): AuditLogProto {
    const auditLog = new AuditLogProto();
    auditLog.id = id;
    auditLog.user_id = userId;
    auditLog.action = action;
    auditLog.object_type = objectType;
    auditLog.object_id = objectId;
    auditLog.message = message;
    auditLog.ip_address = ipAddress;
    auditLog.timestamp = timestamp;
    return auditLog;
  }

  /**
   * Validate audit log entry
   */
  static isValidAuditLog(auditLog: AuditLogProto): bool {
    return auditLog.id.length > 0 &&
           auditLog.action.length > 0 &&
           auditLog.timestamp.length > 0;
  }

  /**
   * Get the most recent audit log from a collection
   */
  static getMostRecent(collection: AuditLogCollection): AuditLogProto | null {
    if (collection.count() === 0) {
      return null;
    }

    let mostRecent = collection.getAuditLog(0);
    if (mostRecent === null) return null;

    for (let i = 1; i < collection.count(); i++) {
      const current = collection.getAuditLog(i);
      if (current !== null && current.timestamp > mostRecent.timestamp) {
        mostRecent = current;
      }
    }
    return mostRecent;
  }
}
