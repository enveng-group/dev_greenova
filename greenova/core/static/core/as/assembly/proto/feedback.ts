// AssemblyScript Protobuf stubs for feedback.proto
// Generated for as-proto runtime
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class Feedback {
  id = "";
  user_id = "";
  message = "";
  rating: i32 = 0;
  timestamp = "";

  static encode(message: Feedback): Uint8Array {
    return Protobuf.encode<Feedback>(message, (m, w) => {
      if (m.id.length > 0) w.string(1, m.id);
      if (m.user_id.length > 0) w.string(2, m.user_id);
      if (m.message.length > 0) w.string(3, m.message);
      if (m.rating != 0) w.int32(4, m.rating);
      if (m.timestamp.length > 0) w.string(5, m.timestamp);
    });
  }
  static decode(buffer: Uint8Array): Feedback {
    return Protobuf.decode<Feedback>(buffer, (r, l) => {
      const m = new Feedback();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.id = r.string(); break;
          case 2: m.user_id = r.string(); break;
          case 3: m.message = r.string(); break;
          case 4: m.rating = r.int32(); break;
          case 5: m.timestamp = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class FeedbackList {
  feedbacks: Array<Feedback> = new Array<Feedback>();
  error = "";

  static encode(message: FeedbackList): Uint8Array {
    return Protobuf.encode<FeedbackList>(message, (m, w) => {
      for (let i = 0; i < m.feedbacks.length; i++) w.bytes(1, Feedback.encode(m.feedbacks[i]));
      if (m.error.length > 0) w.string(2, m.error);
    });
  }
  static decode(buffer: Uint8Array): FeedbackList {
    return Protobuf.decode<FeedbackList>(buffer, (r, l) => {
      const m = new FeedbackList();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.feedbacks.push(Feedback.decode(r.bytes())); break;
          case 2: m.error = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
