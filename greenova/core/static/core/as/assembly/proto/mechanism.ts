// AssemblyScript Protobuf stubs for mechanism.proto
// Generated for as-proto runtime
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export enum ObligationStatus {
  STATUS_UNKNOWN = 0,
  STATUS_NOT_STARTED = 1,
  STATUS_IN_PROGRESS = 2,
  STATUS_COMPLETED = 3,
  STATUS_OVERDUE = 4,
}

export class ObligationInsight {
  obligation_number = "";
  due_date = "";
  close_out_date = "";

  static encode(message: ObligationInsight): Uint8Array {
    return Protobuf.encode<ObligationInsight>(message, (m, w) => {
      if (m.obligation_number.length > 0) w.string(1, m.obligation_number);
      if (m.due_date.length > 0) w.string(2, m.due_date);
      if (m.close_out_date.length > 0) w.string(3, m.close_out_date);
    });
  }
  static decode(buffer: Uint8Array): ObligationInsight {
    return Protobuf.decode<ObligationInsight>(buffer, (r, l) => {
      const m = new ObligationInsight();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.obligation_number = r.string(); break;
          case 2: m.due_date = r.string(); break;
          case 3: m.close_out_date = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ObligationInsightResponse {
  mechanism_id: i32 = 0;
  status = "";
  status_key = "";
  count: i32 = 0;
  total_count: i32 = 0;
  obligations: Array<ObligationInsight> = new Array<ObligationInsight>();
  error = "";

  static encode(message: ObligationInsightResponse): Uint8Array {
    return Protobuf.encode<ObligationInsightResponse>(message, (m, w) => {
      if (m.mechanism_id != 0) w.int32(1, m.mechanism_id);
      if (m.status.length > 0) w.string(2, m.status);
      if (m.status_key.length > 0) w.string(3, m.status_key);
      if (m.count != 0) w.int32(4, m.count);
      if (m.total_count != 0) w.int32(5, m.total_count);
      for (let i = 0; i < m.obligations.length; i++) w.bytes(6, ObligationInsight.encode(m.obligations[i]));
      if (m.error.length > 0) w.string(7, m.error);
    });
  }
  static decode(buffer: Uint8Array): ObligationInsightResponse {
    return Protobuf.decode<ObligationInsightResponse>(buffer, (r, l) => {
      const m = new ObligationInsightResponse();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.mechanism_id = r.int32(); break;
          case 2: m.status = r.string(); break;
          case 3: m.status_key = r.string(); break;
          case 4: m.count = r.int32(); break;
          case 5: m.total_count = r.int32(); break;
          case 6: m.obligations.push(ObligationInsight.decode(r.bytes())); break;
          case 7: m.error = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChartSegment {
  label = "";
  value: i32 = 0;
  color = "";

  static encode(message: ChartSegment): Uint8Array {
    return Protobuf.encode<ChartSegment>(message, (m, w) => {
      if (m.label.length > 0) w.string(1, m.label);
      if (m.value != 0) w.int32(2, m.value);
      if (m.color.length > 0) w.string(3, m.color);
    });
  }
  static decode(buffer: Uint8Array): ChartSegment {
    return Protobuf.decode<ChartSegment>(buffer, (r, l) => {
      const m = new ChartSegment();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.label = r.string(); break;
          case 2: m.value = r.int32(); break;
          case 3: m.color = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChartData {
  segments: Array<ChartSegment> = new Array<ChartSegment>();
  mechanism_id: i32 = 0;
  mechanism_name = "";

  static encode(message: ChartData): Uint8Array {
    return Protobuf.encode<ChartData>(message, (m, w) => {
      for (let i = 0; i < m.segments.length; i++) w.bytes(1, ChartSegment.encode(m.segments[i]));
      if (m.mechanism_id != 0) w.int32(2, m.mechanism_id);
      if (m.mechanism_name.length > 0) w.string(3, m.mechanism_name);
    });
  }
  static decode(buffer: Uint8Array): ChartData {
    return Protobuf.decode<ChartData>(buffer, (r, l) => {
      const m = new ChartData();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.segments.push(ChartSegment.decode(r.bytes())); break;
          case 2: m.mechanism_id = r.int32(); break;
          case 3: m.mechanism_name = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChartResponse {
  charts: Array<ChartData> = new Array<ChartData>();
  error = "";

  static encode(message: ChartResponse): Uint8Array {
    return Protobuf.encode<ChartResponse>(message, (m, w) => {
      for (let i = 0; i < m.charts.length; i++) w.bytes(1, ChartData.encode(m.charts[i]));
      if (m.error.length > 0) w.string(2, m.error);
    });
  }
  static decode(buffer: Uint8Array): ChartResponse {
    return Protobuf.decode<ChartResponse>(buffer, (r, l) => {
      const m = new ChartResponse();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.charts.push(ChartData.decode(r.bytes())); break;
          case 2: m.error = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
