// AssemblyScript Protobuf stubs for obligations.proto
// Simple implementation without decorators using as-proto runtime

import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class ObligationProto {
  obligation_number: string = "";
  project_id: string = "";
  primary_environmental_mechanism_id: string = "";
  procedure: string = "";
  environmental_aspect: string = "";
  custom_environmental_aspect: string = "";
  obligation: string = "";
  accountability: string = "";
  responsible_user_ids: Array<string> = new Array<string>();
  project_phase: string = "";
  action_due_date: string = "";
  close_out_date: string = "";
  status: string = "";
  supporting_information: string = "";
  general_comments: string = "";
  evidence_notes: string = "";
  recurring_obligation: boolean = false;
  recurring_frequency: string = "";
  recurring_status: string = "";
  recurring_forecasted_date: string = "";
  inspection: boolean = false;
  inspection_frequency: string = "";
  site_or_desktop: string = "";
  new_control_action_required: boolean = false;
  obligation_type: string = "";
  gap_analysis: boolean = false;
  notes_for_gap_analysis: string = "";
  created_at: string = "";
  updated_at: string = "";

  static encode(message: ObligationProto): Uint8Array {
    return Protobuf.encode<ObligationProto>(message, (message: ObligationProto, writer: Writer) => {
      if (message.obligation_number.length > 0) writer.string(1, message.obligation_number);
      if (message.project_id.length > 0) writer.string(2, message.project_id);
      if (message.primary_environmental_mechanism_id.length > 0) writer.string(3, message.primary_environmental_mechanism_id);
      if (message.procedure.length > 0) writer.string(4, message.procedure);
      if (message.environmental_aspect.length > 0) writer.string(5, message.environmental_aspect);
      if (message.custom_environmental_aspect.length > 0) writer.string(6, message.custom_environmental_aspect);
      if (message.obligation.length > 0) writer.string(7, message.obligation);
      if (message.accountability.length > 0) writer.string(8, message.accountability);
      for (let i = 0; i < message.responsible_user_ids.length; i++) {
        writer.string(9, message.responsible_user_ids[i]);
      }
      if (message.project_phase.length > 0) writer.string(10, message.project_phase);
      if (message.action_due_date.length > 0) writer.string(11, message.action_due_date);
      if (message.close_out_date.length > 0) writer.string(12, message.close_out_date);
      if (message.status.length > 0) writer.string(13, message.status);
      if (message.supporting_information.length > 0) writer.string(14, message.supporting_information);
      if (message.general_comments.length > 0) writer.string(15, message.general_comments);
      if (message.evidence_notes.length > 0) writer.string(16, message.evidence_notes);
      if (message.recurring_obligation) writer.bool(17, message.recurring_obligation);
      if (message.recurring_frequency.length > 0) writer.string(18, message.recurring_frequency);
      if (message.recurring_status.length > 0) writer.string(19, message.recurring_status);
      if (message.recurring_forecasted_date.length > 0) writer.string(20, message.recurring_forecasted_date);
      if (message.inspection) writer.bool(21, message.inspection);
      if (message.inspection_frequency.length > 0) writer.string(22, message.inspection_frequency);
      if (message.site_or_desktop.length > 0) writer.string(23, message.site_or_desktop);
      if (message.new_control_action_required) writer.bool(24, message.new_control_action_required);
      if (message.obligation_type.length > 0) writer.string(25, message.obligation_type);
      if (message.gap_analysis) writer.bool(26, message.gap_analysis);
      if (message.notes_for_gap_analysis.length > 0) writer.string(27, message.notes_for_gap_analysis);
      if (message.created_at.length > 0) writer.string(28, message.created_at);
      if (message.updated_at.length > 0) writer.string(29, message.updated_at);
    });
  }

  static decode(buffer: Uint8Array): ObligationProto {
    return Protobuf.decode<ObligationProto>(buffer, (reader: Reader, length: i32) => {
      const message = new ObligationProto();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.obligation_number = reader.string(); break;
          case 2: message.project_id = reader.string(); break;
          case 3: message.primary_environmental_mechanism_id = reader.string(); break;
          case 4: message.procedure = reader.string(); break;
          case 5: message.environmental_aspect = reader.string(); break;
          case 6: message.custom_environmental_aspect = reader.string(); break;
          case 7: message.obligation = reader.string(); break;
          case 8: message.accountability = reader.string(); break;
          case 9: message.responsible_user_ids.push(reader.string()); break;
          case 10: message.project_phase = reader.string(); break;
          case 11: message.action_due_date = reader.string(); break;
          case 12: message.close_out_date = reader.string(); break;
          case 13: message.status = reader.string(); break;
          case 14: message.supporting_information = reader.string(); break;
          case 15: message.general_comments = reader.string(); break;
          case 16: message.evidence_notes = reader.string(); break;
          case 17: message.recurring_obligation = reader.bool(); break;
          case 18: message.recurring_frequency = reader.string(); break;
          case 19: message.recurring_status = reader.string(); break;
          case 20: message.recurring_forecasted_date = reader.string(); break;
          case 21: message.inspection = reader.bool(); break;
          case 22: message.inspection_frequency = reader.string(); break;
          case 23: message.site_or_desktop = reader.string(); break;
          case 24: message.new_control_action_required = reader.bool(); break;
          case 25: message.obligation_type = reader.string(); break;
          case 26: message.gap_analysis = reader.bool(); break;
          case 27: message.notes_for_gap_analysis = reader.string(); break;
          case 28: message.created_at = reader.string(); break;
          case 29: message.updated_at = reader.string(); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}

export class ObligationCollection {
  obligations: Array<ObligationProto> = new Array<ObligationProto>();

  static encode(message: ObligationCollection): Uint8Array {
    return Protobuf.encode<ObligationCollection>(message, (message: ObligationCollection, writer: Writer) => {
      for (let i = 0; i < message.obligations.length; i++) {
        writer.bytes(1, ObligationProto.encode(message.obligations[i]));
      }
    });
  }

  static decode(buffer: Uint8Array): ObligationCollection {
    return Protobuf.decode<ObligationCollection>(buffer, (reader: Reader, length: i32) => {
      const message = new ObligationCollection();
      const end = length < 0 ? reader.ptr + reader.uint32() : reader.ptr + length;
      while (reader.ptr < end) {
        const tag = reader.uint32();
        switch (tag >>> 3) {
          case 1: message.obligations.push(ObligationProto.decode(reader.bytes())); break;
          default: reader.skipType(tag & 7); break;
        }
      }
      return message;
    });
  }
}
