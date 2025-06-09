// AssemblyScript Protobuf stubs for projects.proto
// Simple implementation without decorators using as-proto runtime

import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class ProjectProto {
  id = "";
  name = "";
  description = "";
  member_user_ids: Array<string> = new Array<string>();
  created_at = "";
  updated_at = "";

  static encode(message: ProjectProto): Uint8Array {
    return Protobuf.encode<ProjectProto>(message, (message: ProjectProto, writer: Writer) => {
      if (message.id.length > 0) writer.string(1, message.id);
      if (message.name.length > 0) writer.string(2, message.name);
      if (message.description.length > 0) writer.string(3, message.description);
      for (let i = 0; i < message.member_user_ids.length; i++) {
        writer.string(4, message.member_user_ids[i]);
      }
      if (message.created_at.length > 0) writer.string(5, message.created_at);
      if (message.updated_at.length > 0) writer.string(6, message.updated_at);
    });
  }

  static decode(buffer: Uint8Array): ProjectProto {
    return Protobuf.decode<ProjectProto>(buffer, (reader: Reader, length: i32) => {
      const message = new ProjectProto();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.id = reader.string(); break;
          case 2: message.name = reader.string(); break;
          case 3: message.description = reader.string(); break;
          case 4: message.member_user_ids.push(reader.string()); break;
          case 5: message.created_at = reader.string(); break;
          case 6: message.updated_at = reader.string(); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}

export class ProjectMembershipProto {
  id = "";
  project_id = "";
  user_id = "";
  role = "";
  created_at = "";
  updated_at = "";

  static encode(message: ProjectMembershipProto): Uint8Array {
    return Protobuf.encode<ProjectMembershipProto>(message, (message: ProjectMembershipProto, writer: Writer) => {
      if (message.id.length > 0) writer.string(1, message.id);
      if (message.project_id.length > 0) writer.string(2, message.project_id);
      if (message.user_id.length > 0) writer.string(3, message.user_id);
      if (message.role.length > 0) writer.string(4, message.role);
      if (message.created_at.length > 0) writer.string(5, message.created_at);
      if (message.updated_at.length > 0) writer.string(6, message.updated_at);
    });
  }

  static decode(buffer: Uint8Array): ProjectMembershipProto {
    return Protobuf.decode<ProjectMembershipProto>(buffer, (reader: Reader, length: i32) => {
      const message = new ProjectMembershipProto();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.id = reader.string(); break;
          case 2: message.project_id = reader.string(); break;
          case 3: message.user_id = reader.string(); break;
          case 4: message.role = reader.string(); break;
          case 5: message.created_at = reader.string(); break;
          case 6: message.updated_at = reader.string(); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}

export class ProjectObligationProto {
  id = "";
  project_id = "";
  obligation_id = "";
  created_at = "";
  updated_at = "";

  static encode(message: ProjectObligationProto): Uint8Array {
    return Protobuf.encode<ProjectObligationProto>(message, (message: ProjectObligationProto, writer: Writer) => {
      if (message.id.length > 0) writer.string(1, message.id);
      if (message.project_id.length > 0) writer.string(2, message.project_id);
      if (message.obligation_id.length > 0) writer.string(3, message.obligation_id);
      if (message.created_at.length > 0) writer.string(4, message.created_at);
      if (message.updated_at.length > 0) writer.string(5, message.updated_at);
    });
  }

  static decode(buffer: Uint8Array): ProjectObligationProto {
    return Protobuf.decode<ProjectObligationProto>(buffer, (reader: Reader, length: i32) => {
      const message = new ProjectObligationProto();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.id = reader.string(); break;
          case 2: message.project_id = reader.string(); break;
          case 3: message.obligation_id = reader.string(); break;
          case 4: message.created_at = reader.string(); break;
          case 5: message.updated_at = reader.string(); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}

export class ProjectCollection {
  projects: Array<ProjectProto> = new Array<ProjectProto>();

  static encode(message: ProjectCollection): Uint8Array {
    return Protobuf.encode<ProjectCollection>(message, (message: ProjectCollection, writer: Writer) => {
      for (let i = 0; i < message.projects.length; i++) {
        writer.bytes(1, ProjectProto.encode(message.projects[i]));
      }
    });
  }

  static decode(buffer: Uint8Array): ProjectCollection {
    return Protobuf.decode<ProjectCollection>(buffer, (reader: Reader, length: i32) => {
      const message = new ProjectCollection();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.projects.push(ProjectProto.decode(reader.bytes())); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}

export class ProjectMembershipCollection {
  memberships: Array<ProjectMembershipProto> = new Array<ProjectMembershipProto>();

  static encode(message: ProjectMembershipCollection): Uint8Array {
    return Protobuf.encode<ProjectMembershipCollection>(message, (message: ProjectMembershipCollection, writer: Writer) => {
      for (let i = 0; i < message.memberships.length; i++) {
        writer.bytes(1, ProjectMembershipProto.encode(message.memberships[i]));
      }
    });
  }

  static decode(buffer: Uint8Array): ProjectMembershipCollection {
    return Protobuf.decode<ProjectMembershipCollection>(buffer, (reader: Reader, length: i32) => {
      const message = new ProjectMembershipCollection();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.memberships.push(ProjectMembershipProto.decode(reader.bytes())); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}

export class ProjectObligationCollection {
  project_obligations: Array<ProjectObligationProto> = new Array<ProjectObligationProto>();

  static encode(message: ProjectObligationCollection): Uint8Array {
    return Protobuf.encode<ProjectObligationCollection>(message, (message: ProjectObligationCollection, writer: Writer) => {
      for (let i = 0; i < message.project_obligations.length; i++) {
        writer.bytes(1, ProjectObligationProto.encode(message.project_obligations[i]));
      }
    });
  }

  static decode(buffer: Uint8Array): ProjectObligationCollection {
    return Protobuf.decode<ProjectObligationCollection>(buffer, (reader: Reader, length: i32) => {
      const message = new ProjectObligationCollection();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.project_obligations.push(ProjectObligationProto.decode(reader.bytes())); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}
