// AssemblyScript Protobuf stubs for obligations.proto
// Simple implementation without complex protobuf dependencies

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
    // Simple stub implementation
    return new Uint8Array(0);
  }

  static decode(buffer: Uint8Array): ObligationProto {
    // Simple stub implementation
    return new ObligationProto();
  }
}

export class ObligationCollection {
  obligations: Array<ObligationProto> = new Array<ObligationProto>();

  static encode(message: ObligationCollection): Uint8Array {
    // Simple stub implementation
    return new Uint8Array(0);
  }

  static decode(buffer: Uint8Array): ObligationCollection {
    // Simple stub implementation
    return new ObligationCollection();
  }
}
