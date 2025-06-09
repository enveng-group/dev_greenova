// AssemblyScript Protobuf stubs for chatbot.proto
// Generated for as-proto runtime
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class ChatbotMessage {
  id = "";
  sender = "";
  content = "";
  timestamp = "";

  static encode(message: ChatbotMessage): Uint8Array {
    return Protobuf.encode<ChatbotMessage>(message, (m, w) => {
      if (m.id.length > 0) w.string(1, m.id);
      if (m.sender.length > 0) w.string(2, m.sender);
      if (m.content.length > 0) w.string(3, m.content);
      if (m.timestamp.length > 0) w.string(4, m.timestamp);
    });
  }
  static decode(buffer: Uint8Array): ChatbotMessage {
    return Protobuf.decode<ChatbotMessage>(buffer, (r, l) => {
      const m = new ChatbotMessage();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.id = r.string(); break;
          case 2: m.sender = r.string(); break;
          case 3: m.content = r.string(); break;
          case 4: m.timestamp = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChatbotResponse {
  messages: Array<ChatbotMessage> = new Array<ChatbotMessage>();
  error = "";

  static encode(message: ChatbotResponse): Uint8Array {
    return Protobuf.encode<ChatbotResponse>(message, (m, w) => {
      for (let i = 0; i < m.messages.length; i++) w.bytes(1, ChatbotMessage.encode(m.messages[i]));
      if (m.error.length > 0) w.string(2, m.error);
    });
  }
  static decode(buffer: Uint8Array): ChatbotResponse {
    return Protobuf.decode<ChatbotResponse>(buffer, (r, l) => {
      const m = new ChatbotResponse();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.messages.push(ChatbotMessage.decode(r.bytes())); break;
          case 2: m.error = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
