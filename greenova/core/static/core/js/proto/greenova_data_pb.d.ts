export interface Obligation {
  id?: number;
  title?: string;
  description?: string;
  status?: string;
  due_date?: string;
  project_id?: number;
  requirements?: Requirement[];
  created_at?: Long;
  updated_at?: Long;
}

export function encodeObligation(message: Obligation): Uint8Array {
  let bb = popByteBuffer();
  _encodeObligation(message, bb);
  return toUint8Array(bb);
}

function _encodeObligation(message: Obligation, bb: ByteBuffer): void {
  // optional int32 id = 1;
  let $id = message.id;
  if ($id !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($id));
  }

  // optional string title = 2;
  let $title = message.title;
  if ($title !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $title);
  }

  // optional string description = 3;
  let $description = message.description;
  if ($description !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $description);
  }

  // optional string status = 4;
  let $status = message.status;
  if ($status !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $status);
  }

  // optional string due_date = 5;
  let $due_date = message.due_date;
  if ($due_date !== undefined) {
    writeVarint32(bb, 42);
    writeString(bb, $due_date);
  }

  // optional int32 project_id = 6;
  let $project_id = message.project_id;
  if ($project_id !== undefined) {
    writeVarint32(bb, 48);
    writeVarint64(bb, intToLong($project_id));
  }

  // repeated Requirement requirements = 7;
  let array$requirements = message.requirements;
  if (array$requirements !== undefined) {
    for (let value of array$requirements) {
      writeVarint32(bb, 58);
      let nested = popByteBuffer();
      _encodeRequirement(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional int64 created_at = 8;
  let $created_at = message.created_at;
  if ($created_at !== undefined) {
    writeVarint32(bb, 64);
    writeVarint64(bb, $created_at);
  }

  // optional int64 updated_at = 9;
  let $updated_at = message.updated_at;
  if ($updated_at !== undefined) {
    writeVarint32(bb, 72);
    writeVarint64(bb, $updated_at);
  }
}

export function decodeObligation(binary: Uint8Array): Obligation {
  return _decodeObligation(wrapByteBuffer(binary));
}

function _decodeObligation(bb: ByteBuffer): Obligation {
  let message: Obligation = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 id = 1;
      case 1: {
        message.id = readVarint32(bb);
        break;
      }

      // optional string title = 2;
      case 2: {
        message.title = readString(bb, readVarint32(bb));
        break;
      }

      // optional string description = 3;
      case 3: {
        message.description = readString(bb, readVarint32(bb));
        break;
      }

      // optional string status = 4;
      case 4: {
        message.status = readString(bb, readVarint32(bb));
        break;
      }

      // optional string due_date = 5;
      case 5: {
        message.due_date = readString(bb, readVarint32(bb));
        break;
      }

      // optional int32 project_id = 6;
      case 6: {
        message.project_id = readVarint32(bb);
        break;
      }

      // repeated Requirement requirements = 7;
      case 7: {
        let limit = pushTemporaryLength(bb);
        let values = message.requirements || (message.requirements = []);
        values.push(_decodeRequirement(bb));
        bb.limit = limit;
        break;
      }

      // optional int64 created_at = 8;
      case 8: {
        message.created_at = readVarint64(bb, /* unsigned */ false);
        break;
      }

      // optional int64 updated_at = 9;
      case 9: {
        message.updated_at = readVarint64(bb, /* unsigned */ false);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface Requirement {
  id?: number;
  name?: string;
  description?: string;
  compliance_status?: string;
  tags?: string[];
}

export function encodeRequirement(message: Requirement): Uint8Array {
  let bb = popByteBuffer();
  _encodeRequirement(message, bb);
  return toUint8Array(bb);
}

function _encodeRequirement(message: Requirement, bb: ByteBuffer): void {
  // optional int32 id = 1;
  let $id = message.id;
  if ($id !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($id));
  }

  // optional string name = 2;
  let $name = message.name;
  if ($name !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $name);
  }

  // optional string description = 3;
  let $description = message.description;
  if ($description !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $description);
  }

  // optional string compliance_status = 4;
  let $compliance_status = message.compliance_status;
  if ($compliance_status !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $compliance_status);
  }

  // repeated string tags = 5;
  let array$tags = message.tags;
  if (array$tags !== undefined) {
    for (let value of array$tags) {
      writeVarint32(bb, 42);
      writeString(bb, value);
    }
  }
}

export function decodeRequirement(binary: Uint8Array): Requirement {
  return _decodeRequirement(wrapByteBuffer(binary));
}

function _decodeRequirement(bb: ByteBuffer): Requirement {
  let message: Requirement = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 id = 1;
      case 1: {
        message.id = readVarint32(bb);
        break;
      }

      // optional string name = 2;
      case 2: {
        message.name = readString(bb, readVarint32(bb));
        break;
      }

      // optional string description = 3;
      case 3: {
        message.description = readString(bb, readVarint32(bb));
        break;
      }

      // optional string compliance_status = 4;
      case 4: {
        message.compliance_status = readString(bb, readVarint32(bb));
        break;
      }

      // repeated string tags = 5;
      case 5: {
        let values = message.tags || (message.tags = []);
        values.push(readString(bb, readVarint32(bb)));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface Project {
  id?: number;
  name?: string;
  description?: string;
  location?: string;
  obligations?: Obligation[];
  metadata?: ProjectMetadata;
  created_at?: Long;
  updated_at?: Long;
}

export function encodeProject(message: Project): Uint8Array {
  let bb = popByteBuffer();
  _encodeProject(message, bb);
  return toUint8Array(bb);
}

function _encodeProject(message: Project, bb: ByteBuffer): void {
  // optional int32 id = 1;
  let $id = message.id;
  if ($id !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($id));
  }

  // optional string name = 2;
  let $name = message.name;
  if ($name !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $name);
  }

  // optional string description = 3;
  let $description = message.description;
  if ($description !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $description);
  }

  // optional string location = 4;
  let $location = message.location;
  if ($location !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $location);
  }

  // repeated Obligation obligations = 5;
  let array$obligations = message.obligations;
  if (array$obligations !== undefined) {
    for (let value of array$obligations) {
      writeVarint32(bb, 42);
      let nested = popByteBuffer();
      _encodeObligation(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional ProjectMetadata metadata = 6;
  let $metadata = message.metadata;
  if ($metadata !== undefined) {
    writeVarint32(bb, 50);
    let nested = popByteBuffer();
    _encodeProjectMetadata($metadata, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional int64 created_at = 7;
  let $created_at = message.created_at;
  if ($created_at !== undefined) {
    writeVarint32(bb, 56);
    writeVarint64(bb, $created_at);
  }

  // optional int64 updated_at = 8;
  let $updated_at = message.updated_at;
  if ($updated_at !== undefined) {
    writeVarint32(bb, 64);
    writeVarint64(bb, $updated_at);
  }
}

export function decodeProject(binary: Uint8Array): Project {
  return _decodeProject(wrapByteBuffer(binary));
}

function _decodeProject(bb: ByteBuffer): Project {
  let message: Project = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 id = 1;
      case 1: {
        message.id = readVarint32(bb);
        break;
      }

      // optional string name = 2;
      case 2: {
        message.name = readString(bb, readVarint32(bb));
        break;
      }

      // optional string description = 3;
      case 3: {
        message.description = readString(bb, readVarint32(bb));
        break;
      }

      // optional string location = 4;
      case 4: {
        message.location = readString(bb, readVarint32(bb));
        break;
      }

      // repeated Obligation obligations = 5;
      case 5: {
        let limit = pushTemporaryLength(bb);
        let values = message.obligations || (message.obligations = []);
        values.push(_decodeObligation(bb));
        bb.limit = limit;
        break;
      }

      // optional ProjectMetadata metadata = 6;
      case 6: {
        let limit = pushTemporaryLength(bb);
        message.metadata = _decodeProjectMetadata(bb);
        bb.limit = limit;
        break;
      }

      // optional int64 created_at = 7;
      case 7: {
        message.created_at = readVarint64(bb, /* unsigned */ false);
        break;
      }

      // optional int64 updated_at = 8;
      case 8: {
        message.updated_at = readVarint64(bb, /* unsigned */ false);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ProjectMetadata {
  environmental_zone?: string;
  compliance_frameworks?: string[];
  project_manager?: string;
  contact_email?: string;
}

export function encodeProjectMetadata(message: ProjectMetadata): Uint8Array {
  let bb = popByteBuffer();
  _encodeProjectMetadata(message, bb);
  return toUint8Array(bb);
}

function _encodeProjectMetadata(message: ProjectMetadata, bb: ByteBuffer): void {
  // optional string environmental_zone = 1;
  let $environmental_zone = message.environmental_zone;
  if ($environmental_zone !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $environmental_zone);
  }

  // repeated string compliance_frameworks = 2;
  let array$compliance_frameworks = message.compliance_frameworks;
  if (array$compliance_frameworks !== undefined) {
    for (let value of array$compliance_frameworks) {
      writeVarint32(bb, 18);
      writeString(bb, value);
    }
  }

  // optional string project_manager = 3;
  let $project_manager = message.project_manager;
  if ($project_manager !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $project_manager);
  }

  // optional string contact_email = 4;
  let $contact_email = message.contact_email;
  if ($contact_email !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $contact_email);
  }
}

export function decodeProjectMetadata(binary: Uint8Array): ProjectMetadata {
  return _decodeProjectMetadata(wrapByteBuffer(binary));
}

function _decodeProjectMetadata(bb: ByteBuffer): ProjectMetadata {
  let message: ProjectMetadata = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string environmental_zone = 1;
      case 1: {
        message.environmental_zone = readString(bb, readVarint32(bb));
        break;
      }

      // repeated string compliance_frameworks = 2;
      case 2: {
        let values = message.compliance_frameworks || (message.compliance_frameworks = []);
        values.push(readString(bb, readVarint32(bb)));
        break;
      }

      // optional string project_manager = 3;
      case 3: {
        message.project_manager = readString(bb, readVarint32(bb));
        break;
      }

      // optional string contact_email = 4;
      case 4: {
        message.contact_email = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface DashboardData {
  project_summary?: ProjectSummary;
  obligation_summaries?: ObligationSummary[];
  compliance_metrics?: ComplianceMetrics;
  last_updated?: Long;
}

export function encodeDashboardData(message: DashboardData): Uint8Array {
  let bb = popByteBuffer();
  _encodeDashboardData(message, bb);
  return toUint8Array(bb);
}

function _encodeDashboardData(message: DashboardData, bb: ByteBuffer): void {
  // optional ProjectSummary project_summary = 1;
  let $project_summary = message.project_summary;
  if ($project_summary !== undefined) {
    writeVarint32(bb, 10);
    let nested = popByteBuffer();
    _encodeProjectSummary($project_summary, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // repeated ObligationSummary obligation_summaries = 2;
  let array$obligation_summaries = message.obligation_summaries;
  if (array$obligation_summaries !== undefined) {
    for (let value of array$obligation_summaries) {
      writeVarint32(bb, 18);
      let nested = popByteBuffer();
      _encodeObligationSummary(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional ComplianceMetrics compliance_metrics = 3;
  let $compliance_metrics = message.compliance_metrics;
  if ($compliance_metrics !== undefined) {
    writeVarint32(bb, 26);
    let nested = popByteBuffer();
    _encodeComplianceMetrics($compliance_metrics, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional int64 last_updated = 4;
  let $last_updated = message.last_updated;
  if ($last_updated !== undefined) {
    writeVarint32(bb, 32);
    writeVarint64(bb, $last_updated);
  }
}

export function decodeDashboardData(binary: Uint8Array): DashboardData {
  return _decodeDashboardData(wrapByteBuffer(binary));
}

function _decodeDashboardData(bb: ByteBuffer): DashboardData {
  let message: DashboardData = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional ProjectSummary project_summary = 1;
      case 1: {
        let limit = pushTemporaryLength(bb);
        message.project_summary = _decodeProjectSummary(bb);
        bb.limit = limit;
        break;
      }

      // repeated ObligationSummary obligation_summaries = 2;
      case 2: {
        let limit = pushTemporaryLength(bb);
        let values = message.obligation_summaries || (message.obligation_summaries = []);
        values.push(_decodeObligationSummary(bb));
        bb.limit = limit;
        break;
      }

      // optional ComplianceMetrics compliance_metrics = 3;
      case 3: {
        let limit = pushTemporaryLength(bb);
        message.compliance_metrics = _decodeComplianceMetrics(bb);
        bb.limit = limit;
        break;
      }

      // optional int64 last_updated = 4;
      case 4: {
        message.last_updated = readVarint64(bb, /* unsigned */ false);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ProjectSummary {
  total_projects?: number;
  active_projects?: number;
  completed_projects?: number;
  recent_projects?: Project[];
}

export function encodeProjectSummary(message: ProjectSummary): Uint8Array {
  let bb = popByteBuffer();
  _encodeProjectSummary(message, bb);
  return toUint8Array(bb);
}

function _encodeProjectSummary(message: ProjectSummary, bb: ByteBuffer): void {
  // optional int32 total_projects = 1;
  let $total_projects = message.total_projects;
  if ($total_projects !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($total_projects));
  }

  // optional int32 active_projects = 2;
  let $active_projects = message.active_projects;
  if ($active_projects !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($active_projects));
  }

  // optional int32 completed_projects = 3;
  let $completed_projects = message.completed_projects;
  if ($completed_projects !== undefined) {
    writeVarint32(bb, 24);
    writeVarint64(bb, intToLong($completed_projects));
  }

  // repeated Project recent_projects = 4;
  let array$recent_projects = message.recent_projects;
  if (array$recent_projects !== undefined) {
    for (let value of array$recent_projects) {
      writeVarint32(bb, 34);
      let nested = popByteBuffer();
      _encodeProject(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }
}

export function decodeProjectSummary(binary: Uint8Array): ProjectSummary {
  return _decodeProjectSummary(wrapByteBuffer(binary));
}

function _decodeProjectSummary(bb: ByteBuffer): ProjectSummary {
  let message: ProjectSummary = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 total_projects = 1;
      case 1: {
        message.total_projects = readVarint32(bb);
        break;
      }

      // optional int32 active_projects = 2;
      case 2: {
        message.active_projects = readVarint32(bb);
        break;
      }

      // optional int32 completed_projects = 3;
      case 3: {
        message.completed_projects = readVarint32(bb);
        break;
      }

      // repeated Project recent_projects = 4;
      case 4: {
        let limit = pushTemporaryLength(bb);
        let values = message.recent_projects || (message.recent_projects = []);
        values.push(_decodeProject(bb));
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ObligationSummary {
  status?: string;
  count?: number;
  upcoming_obligations?: Obligation[];
}

export function encodeObligationSummary(message: ObligationSummary): Uint8Array {
  let bb = popByteBuffer();
  _encodeObligationSummary(message, bb);
  return toUint8Array(bb);
}

function _encodeObligationSummary(message: ObligationSummary, bb: ByteBuffer): void {
  // optional string status = 1;
  let $status = message.status;
  if ($status !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $status);
  }

  // optional int32 count = 2;
  let $count = message.count;
  if ($count !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($count));
  }

  // repeated Obligation upcoming_obligations = 3;
  let array$upcoming_obligations = message.upcoming_obligations;
  if (array$upcoming_obligations !== undefined) {
    for (let value of array$upcoming_obligations) {
      writeVarint32(bb, 26);
      let nested = popByteBuffer();
      _encodeObligation(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }
}

export function decodeObligationSummary(binary: Uint8Array): ObligationSummary {
  return _decodeObligationSummary(wrapByteBuffer(binary));
}

function _decodeObligationSummary(bb: ByteBuffer): ObligationSummary {
  let message: ObligationSummary = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string status = 1;
      case 1: {
        message.status = readString(bb, readVarint32(bb));
        break;
      }

      // optional int32 count = 2;
      case 2: {
        message.count = readVarint32(bb);
        break;
      }

      // repeated Obligation upcoming_obligations = 3;
      case 3: {
        let limit = pushTemporaryLength(bb);
        let values = message.upcoming_obligations || (message.upcoming_obligations = []);
        values.push(_decodeObligation(bb));
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ComplianceMetrics {
  overall_compliance_rate?: number;
  overdue_obligations?: number;
  due_this_week?: number;
  due_this_month?: number;
  compliance_by_framework?: ComplianceByFramework[];
}

export function encodeComplianceMetrics(message: ComplianceMetrics): Uint8Array {
  let bb = popByteBuffer();
  _encodeComplianceMetrics(message, bb);
  return toUint8Array(bb);
}

function _encodeComplianceMetrics(message: ComplianceMetrics, bb: ByteBuffer): void {
  // optional double overall_compliance_rate = 1;
  let $overall_compliance_rate = message.overall_compliance_rate;
  if ($overall_compliance_rate !== undefined) {
    writeVarint32(bb, 9);
    writeDouble(bb, $overall_compliance_rate);
  }

  // optional int32 overdue_obligations = 2;
  let $overdue_obligations = message.overdue_obligations;
  if ($overdue_obligations !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($overdue_obligations));
  }

  // optional int32 due_this_week = 3;
  let $due_this_week = message.due_this_week;
  if ($due_this_week !== undefined) {
    writeVarint32(bb, 24);
    writeVarint64(bb, intToLong($due_this_week));
  }

  // optional int32 due_this_month = 4;
  let $due_this_month = message.due_this_month;
  if ($due_this_month !== undefined) {
    writeVarint32(bb, 32);
    writeVarint64(bb, intToLong($due_this_month));
  }

  // repeated ComplianceByFramework compliance_by_framework = 5;
  let array$compliance_by_framework = message.compliance_by_framework;
  if (array$compliance_by_framework !== undefined) {
    for (let value of array$compliance_by_framework) {
      writeVarint32(bb, 42);
      let nested = popByteBuffer();
      _encodeComplianceByFramework(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }
}

export function decodeComplianceMetrics(binary: Uint8Array): ComplianceMetrics {
  return _decodeComplianceMetrics(wrapByteBuffer(binary));
}

function _decodeComplianceMetrics(bb: ByteBuffer): ComplianceMetrics {
  let message: ComplianceMetrics = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional double overall_compliance_rate = 1;
      case 1: {
        message.overall_compliance_rate = readDouble(bb);
        break;
      }

      // optional int32 overdue_obligations = 2;
      case 2: {
        message.overdue_obligations = readVarint32(bb);
        break;
      }

      // optional int32 due_this_week = 3;
      case 3: {
        message.due_this_week = readVarint32(bb);
        break;
      }

      // optional int32 due_this_month = 4;
      case 4: {
        message.due_this_month = readVarint32(bb);
        break;
      }

      // repeated ComplianceByFramework compliance_by_framework = 5;
      case 5: {
        let limit = pushTemporaryLength(bb);
        let values = message.compliance_by_framework || (message.compliance_by_framework = []);
        values.push(_decodeComplianceByFramework(bb));
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ComplianceByFramework {
  framework_name?: string;
  compliance_rate?: number;
  total_obligations?: number;
  compliant_obligations?: number;
}

export function encodeComplianceByFramework(message: ComplianceByFramework): Uint8Array {
  let bb = popByteBuffer();
  _encodeComplianceByFramework(message, bb);
  return toUint8Array(bb);
}

function _encodeComplianceByFramework(message: ComplianceByFramework, bb: ByteBuffer): void {
  // optional string framework_name = 1;
  let $framework_name = message.framework_name;
  if ($framework_name !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $framework_name);
  }

  // optional double compliance_rate = 2;
  let $compliance_rate = message.compliance_rate;
  if ($compliance_rate !== undefined) {
    writeVarint32(bb, 17);
    writeDouble(bb, $compliance_rate);
  }

  // optional int32 total_obligations = 3;
  let $total_obligations = message.total_obligations;
  if ($total_obligations !== undefined) {
    writeVarint32(bb, 24);
    writeVarint64(bb, intToLong($total_obligations));
  }

  // optional int32 compliant_obligations = 4;
  let $compliant_obligations = message.compliant_obligations;
  if ($compliant_obligations !== undefined) {
    writeVarint32(bb, 32);
    writeVarint64(bb, intToLong($compliant_obligations));
  }
}

export function decodeComplianceByFramework(binary: Uint8Array): ComplianceByFramework {
  return _decodeComplianceByFramework(wrapByteBuffer(binary));
}

function _decodeComplianceByFramework(bb: ByteBuffer): ComplianceByFramework {
  let message: ComplianceByFramework = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string framework_name = 1;
      case 1: {
        message.framework_name = readString(bb, readVarint32(bb));
        break;
      }

      // optional double compliance_rate = 2;
      case 2: {
        message.compliance_rate = readDouble(bb);
        break;
      }

      // optional int32 total_obligations = 3;
      case 3: {
        message.total_obligations = readVarint32(bb);
        break;
      }

      // optional int32 compliant_obligations = 4;
      case 4: {
        message.compliant_obligations = readVarint32(bb);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface Long {
  low: number;
  high: number;
  unsigned: boolean;
}

interface ByteBuffer {
  bytes: Uint8Array;
  offset: number;
  limit: number;
}

function pushTemporaryLength(bb: ByteBuffer): number {
  let length = readVarint32(bb);
  let limit = bb.limit;
  bb.limit = bb.offset + length;
  return limit;
}

function skipUnknownField(bb: ByteBuffer, type: number): void {
  switch (type) {
    case 0: while (readByte(bb) & 0x80) { } break;
    case 2: skip(bb, readVarint32(bb)); break;
    case 5: skip(bb, 4); break;
    case 1: skip(bb, 8); break;
    default: throw new Error("Unimplemented type: " + type);
  }
}

function stringToLong(value: string): Long {
  return {
    low: value.charCodeAt(0) | (value.charCodeAt(1) << 16),
    high: value.charCodeAt(2) | (value.charCodeAt(3) << 16),
    unsigned: false,
  };
}

function longToString(value: Long): string {
  let low = value.low;
  let high = value.high;
  return String.fromCharCode(
    low & 0xFFFF,
    low >>> 16,
    high & 0xFFFF,
    high >>> 16);
}

// The code below was modified from https://github.com/protobufjs/bytebuffer.js
// which is under the Apache License 2.0.

let f32 = new Float32Array(1);
let f32_u8 = new Uint8Array(f32.buffer);

let f64 = new Float64Array(1);
let f64_u8 = new Uint8Array(f64.buffer);

function intToLong(value: number): Long {
  value |= 0;
  return {
    low: value,
    high: value >> 31,
    unsigned: value >= 0,
  };
}

let bbStack: ByteBuffer[] = [];

function popByteBuffer(): ByteBuffer {
  const bb = bbStack.pop();
  if (!bb) return { bytes: new Uint8Array(64), offset: 0, limit: 0 };
  bb.offset = bb.limit = 0;
  return bb;
}

function pushByteBuffer(bb: ByteBuffer): void {
  bbStack.push(bb);
}

function wrapByteBuffer(bytes: Uint8Array): ByteBuffer {
  return { bytes, offset: 0, limit: bytes.length };
}

function toUint8Array(bb: ByteBuffer): Uint8Array {
  let bytes = bb.bytes;
  let limit = bb.limit;
  return bytes.length === limit ? bytes : bytes.subarray(0, limit);
}

function skip(bb: ByteBuffer, offset: number): void {
  if (bb.offset + offset > bb.limit) {
    throw new Error('Skip past limit');
  }
  bb.offset += offset;
}

function isAtEnd(bb: ByteBuffer): boolean {
  return bb.offset >= bb.limit;
}

function grow(bb: ByteBuffer, count: number): number {
  let bytes = bb.bytes;
  let offset = bb.offset;
  let limit = bb.limit;
  let finalOffset = offset + count;
  if (finalOffset > bytes.length) {
    let newBytes = new Uint8Array(finalOffset * 2);
    newBytes.set(bytes);
    bb.bytes = newBytes;
  }
  bb.offset = finalOffset;
  if (finalOffset > limit) {
    bb.limit = finalOffset;
  }
  return offset;
}

function advance(bb: ByteBuffer, count: number): number {
  let offset = bb.offset;
  if (offset + count > bb.limit) {
    throw new Error('Read past limit');
  }
  bb.offset += count;
  return offset;
}

function readBytes(bb: ByteBuffer, count: number): Uint8Array {
  let offset = advance(bb, count);
  return bb.bytes.subarray(offset, offset + count);
}

function writeBytes(bb: ByteBuffer, buffer: Uint8Array): void {
  let offset = grow(bb, buffer.length);
  bb.bytes.set(buffer, offset);
}

function readString(bb: ByteBuffer, count: number): string {
  // Sadly a hand-coded UTF8 decoder is much faster than subarray+TextDecoder in V8
  let offset = advance(bb, count);
  let fromCharCode = String.fromCharCode;
  let bytes = bb.bytes;
  let invalid = '\uFFFD';
  let text = '';

  for (let i = 0; i < count; i++) {
    let c1 = bytes[i + offset], c2: number, c3: number, c4: number, c: number;

    // 1 byte
    if ((c1 & 0x80) === 0) {
      text += fromCharCode(c1);
    }

    // 2 bytes
    else if ((c1 & 0xE0) === 0xC0) {
      if (i + 1 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        if ((c2 & 0xC0) !== 0x80) text += invalid;
        else {
          c = ((c1 & 0x1F) << 6) | (c2 & 0x3F);
          if (c < 0x80) text += invalid;
          else {
            text += fromCharCode(c);
            i++;
          }
        }
      }
    }

    // 3 bytes
    else if ((c1 & 0xF0) == 0xE0) {
      if (i + 2 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        c3 = bytes[i + offset + 2];
        if (((c2 | (c3 << 8)) & 0xC0C0) !== 0x8080) text += invalid;
        else {
          c = ((c1 & 0x0F) << 12) | ((c2 & 0x3F) << 6) | (c3 & 0x3F);
          if (c < 0x0800 || (c >= 0xD800 && c <= 0xDFFF)) text += invalid;
          else {
            text += fromCharCode(c);
            i += 2;
          }
        }
      }
    }

    // 4 bytes
    else if ((c1 & 0xF8) == 0xF0) {
      if (i + 3 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        c3 = bytes[i + offset + 2];
        c4 = bytes[i + offset + 3];
        if (((c2 | (c3 << 8) | (c4 << 16)) & 0xC0C0C0) !== 0x808080) text += invalid;
        else {
          c = ((c1 & 0x07) << 0x12) | ((c2 & 0x3F) << 0x0C) | ((c3 & 0x3F) << 0x06) | (c4 & 0x3F);
          if (c < 0x10000 || c > 0x10FFFF) text += invalid;
          else {
            c -= 0x10000;
            text += fromCharCode((c >> 10) + 0xD800, (c & 0x3FF) + 0xDC00);
            i += 3;
          }
        }
      }
    }

    else text += invalid;
  }

  return text;
}

function writeString(bb: ByteBuffer, text: string): void {
  // Sadly a hand-coded UTF8 encoder is much faster than TextEncoder+set in V8
  let n = text.length;
  let byteCount = 0;

  // Write the byte count first
  for (let i = 0; i < n; i++) {
    let c = text.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF && i + 1 < n) {
      c = (c << 10) + text.charCodeAt(++i) - 0x35FDC00;
    }
    byteCount += c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4;
  }
  writeVarint32(bb, byteCount);

  let offset = grow(bb, byteCount);
  let bytes = bb.bytes;

  // Then write the bytes
  for (let i = 0; i < n; i++) {
    let c = text.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF && i + 1 < n) {
      c = (c << 10) + text.charCodeAt(++i) - 0x35FDC00;
    }
    if (c < 0x80) {
      bytes[offset++] = c;
    } else {
      if (c < 0x800) {
        bytes[offset++] = ((c >> 6) & 0x1F) | 0xC0;
      } else {
        if (c < 0x10000) {
          bytes[offset++] = ((c >> 12) & 0x0F) | 0xE0;
        } else {
          bytes[offset++] = ((c >> 18) & 0x07) | 0xF0;
          bytes[offset++] = ((c >> 12) & 0x3F) | 0x80;
        }
        bytes[offset++] = ((c >> 6) & 0x3F) | 0x80;
      }
      bytes[offset++] = (c & 0x3F) | 0x80;
    }
  }
}

function writeByteBuffer(bb: ByteBuffer, buffer: ByteBuffer): void {
  let offset = grow(bb, buffer.limit);
  let from = bb.bytes;
  let to = buffer.bytes;

  // This for loop is much faster than subarray+set on V8
  for (let i = 0, n = buffer.limit; i < n; i++) {
    from[i + offset] = to[i];
  }
}

function readByte(bb: ByteBuffer): number {
  return bb.bytes[advance(bb, 1)];
}

function writeByte(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 1);
  bb.bytes[offset] = value;
}

function readFloat(bb: ByteBuffer): number {
  let offset = advance(bb, 4);
  let bytes = bb.bytes;

  // Manual copying is much faster than subarray+set in V8
  f32_u8[0] = bytes[offset++];
  f32_u8[1] = bytes[offset++];
  f32_u8[2] = bytes[offset++];
  f32_u8[3] = bytes[offset++];
  return f32[0];
}

function writeFloat(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 4);
  let bytes = bb.bytes;
  f32[0] = value;

  // Manual copying is much faster than subarray+set in V8
  bytes[offset++] = f32_u8[0];
  bytes[offset++] = f32_u8[1];
  bytes[offset++] = f32_u8[2];
  bytes[offset++] = f32_u8[3];
}

function readDouble(bb: ByteBuffer): number {
  let offset = advance(bb, 8);
  let bytes = bb.bytes;

  // Manual copying is much faster than subarray+set in V8
  f64_u8[0] = bytes[offset++];
  f64_u8[1] = bytes[offset++];
  f64_u8[2] = bytes[offset++];
  f64_u8[3] = bytes[offset++];
  f64_u8[4] = bytes[offset++];
  f64_u8[5] = bytes[offset++];
  f64_u8[6] = bytes[offset++];
  f64_u8[7] = bytes[offset++];
  return f64[0];
}

function writeDouble(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 8);
  let bytes = bb.bytes;
  f64[0] = value;

  // Manual copying is much faster than subarray+set in V8
  bytes[offset++] = f64_u8[0];
  bytes[offset++] = f64_u8[1];
  bytes[offset++] = f64_u8[2];
  bytes[offset++] = f64_u8[3];
  bytes[offset++] = f64_u8[4];
  bytes[offset++] = f64_u8[5];
  bytes[offset++] = f64_u8[6];
  bytes[offset++] = f64_u8[7];
}

function readInt32(bb: ByteBuffer): number {
  let offset = advance(bb, 4);
  let bytes = bb.bytes;
  return (
    bytes[offset] |
    (bytes[offset + 1] << 8) |
    (bytes[offset + 2] << 16) |
    (bytes[offset + 3] << 24)
  );
}

function writeInt32(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 4);
  let bytes = bb.bytes;
  bytes[offset] = value;
  bytes[offset + 1] = value >> 8;
  bytes[offset + 2] = value >> 16;
  bytes[offset + 3] = value >> 24;
}

function readInt64(bb: ByteBuffer, unsigned: boolean): Long {
  return {
    low: readInt32(bb),
    high: readInt32(bb),
    unsigned,
  };
}

function writeInt64(bb: ByteBuffer, value: Long): void {
  writeInt32(bb, value.low);
  writeInt32(bb, value.high);
}

function readVarint32(bb: ByteBuffer): number {
  let c = 0;
  let value = 0;
  let b: number;
  do {
    b = readByte(bb);
    if (c < 32) value |= (b & 0x7F) << c;
    c += 7;
  } while (b & 0x80);
  return value;
}

function writeVarint32(bb: ByteBuffer, value: number): void {
  value >>>= 0;
  while (value >= 0x80) {
    writeByte(bb, (value & 0x7f) | 0x80);
    value >>>= 7;
  }
  writeByte(bb, value);
}

function readVarint64(bb: ByteBuffer, unsigned: boolean): Long {
  let part0 = 0;
  let part1 = 0;
  let part2 = 0;
  let b: number;

  b = readByte(bb); part0 = (b & 0x7F); if (b & 0x80) {
    b = readByte(bb); part0 |= (b & 0x7F) << 7; if (b & 0x80) {
      b = readByte(bb); part0 |= (b & 0x7F) << 14; if (b & 0x80) {
        b = readByte(bb); part0 |= (b & 0x7F) << 21; if (b & 0x80) {

          b = readByte(bb); part1 = (b & 0x7F); if (b & 0x80) {
            b = readByte(bb); part1 |= (b & 0x7F) << 7; if (b & 0x80) {
              b = readByte(bb); part1 |= (b & 0x7F) << 14; if (b & 0x80) {
                b = readByte(bb); part1 |= (b & 0x7F) << 21; if (b & 0x80) {

                  b = readByte(bb); part2 = (b & 0x7F); if (b & 0x80) {
                    b = readByte(bb); part2 |= (b & 0x7F) << 7;
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  return {
    low: part0 | (part1 << 28),
    high: (part1 >>> 4) | (part2 << 24),
    unsigned,
  };
}

function writeVarint64(bb: ByteBuffer, value: Long): void {
  let part0 = value.low >>> 0;
  let part1 = ((value.low >>> 28) | (value.high << 4)) >>> 0;
  let part2 = value.high >>> 24;

  // ref: src/google/protobuf/io/coded_stream.cc
  let size =
    part2 === 0 ?
      part1 === 0 ?
        part0 < 1 << 14 ?
          part0 < 1 << 7 ? 1 : 2 :
          part0 < 1 << 21 ? 3 : 4 :
        part1 < 1 << 14 ?
          part1 < 1 << 7 ? 5 : 6 :
          part1 < 1 << 21 ? 7 : 8 :
      part2 < 1 << 7 ? 9 : 10;

  let offset = grow(bb, size);
  let bytes = bb.bytes;

  switch (size) {
    case 10: bytes[offset + 9] = (part2 >>> 7) & 0x01;
    case 9: bytes[offset + 8] = size !== 9 ? part2 | 0x80 : part2 & 0x7F;
    case 8: bytes[offset + 7] = size !== 8 ? (part1 >>> 21) | 0x80 : (part1 >>> 21) & 0x7F;
    case 7: bytes[offset + 6] = size !== 7 ? (part1 >>> 14) | 0x80 : (part1 >>> 14) & 0x7F;
    case 6: bytes[offset + 5] = size !== 6 ? (part1 >>> 7) | 0x80 : (part1 >>> 7) & 0x7F;
    case 5: bytes[offset + 4] = size !== 5 ? part1 | 0x80 : part1 & 0x7F;
    case 4: bytes[offset + 3] = size !== 4 ? (part0 >>> 21) | 0x80 : (part0 >>> 21) & 0x7F;
    case 3: bytes[offset + 2] = size !== 3 ? (part0 >>> 14) | 0x80 : (part0 >>> 14) & 0x7F;
    case 2: bytes[offset + 1] = size !== 2 ? (part0 >>> 7) | 0x80 : (part0 >>> 7) & 0x7F;
    case 1: bytes[offset] = size !== 1 ? part0 | 0x80 : part0 & 0x7F;
  }
}

function readVarint32ZigZag(bb: ByteBuffer): number {
  let value = readVarint32(bb);

  // ref: src/google/protobuf/wire_format_lite.h
  return (value >>> 1) ^ -(value & 1);
}

function writeVarint32ZigZag(bb: ByteBuffer, value: number): void {
  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint32(bb, (value << 1) ^ (value >> 31));
}

function readVarint64ZigZag(bb: ByteBuffer): Long {
  let value = readVarint64(bb, /* unsigned */ false);
  let low = value.low;
  let high = value.high;
  let flip = -(low & 1);

  // ref: src/google/protobuf/wire_format_lite.h
  return {
    low: ((low >>> 1) | (high << 31)) ^ flip,
    high: (high >>> 1) ^ flip,
    unsigned: false,
  };
}

function writeVarint64ZigZag(bb: ByteBuffer, value: Long): void {
  let low = value.low;
  let high = value.high;
  let flip = high >> 31;

  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint64(bb, {
    low: (low << 1) ^ flip,
    high: ((high << 1) | (low >>> 31)) ^ flip,
    unsigned: false,
  });
}
