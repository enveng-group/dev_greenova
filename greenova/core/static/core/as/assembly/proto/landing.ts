// AssemblyScript Protobuf stubs for landing.proto
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class NewsletterSignupRequest {
  email = "";
  static encode(message: NewsletterSignupRequest): Uint8Array {
    return Protobuf.encode<NewsletterSignupRequest>(message, (m, w) => {
      if (m.email.length > 0) w.string(1, m.email);
    });
  }
  static decode(buffer: Uint8Array): NewsletterSignupRequest {
    return Protobuf.decode<NewsletterSignupRequest>(buffer, (r, l) => {
      const m = new NewsletterSignupRequest();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.email = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class NewsletterSignupResponse {
  success: bool = false;
  message = "";
  static encode(message: NewsletterSignupResponse): Uint8Array {
    return Protobuf.encode<NewsletterSignupResponse>(message, (m, w) => {
      if (m.success) w.bool(1, m.success);
      if (m.message.length > 0) w.string(2, m.message);
    });
  }
  static decode(buffer: Uint8Array): NewsletterSignupResponse {
    return Protobuf.decode<NewsletterSignupResponse>(buffer, (r, l) => {
      const m = new NewsletterSignupResponse();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.success = r.bool(); break;
          case 2: m.message = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class Feature {
  title = "";
  description = "";
  static encode(message: Feature): Uint8Array {
    return Protobuf.encode<Feature>(message, (m, w) => {
      if (m.title.length > 0) w.string(1, m.title);
      if (m.description.length > 0) w.string(2, m.description);
    });
  }
  static decode(buffer: Uint8Array): Feature {
    return Protobuf.decode<Feature>(buffer, (r, l) => {
      const m = new Feature();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.title = r.string(); break;
          case 2: m.description = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class Stat {
  name = "";
  value: i32 = 0;
  static encode(message: Stat): Uint8Array {
    return Protobuf.encode<Stat>(message, (m, w) => {
      if (m.name.length > 0) w.string(1, m.name);
      if (m.value != 0) w.int32(2, m.value);
    });
  }
  static decode(buffer: Uint8Array): Stat {
    return Protobuf.decode<Stat>(buffer, (r, l) => {
      const m = new Stat();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.name = r.string(); break;
          case 2: m.value = r.int32(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class Testimonial {
  name = "";
  content = "";
  static encode(message: Testimonial): Uint8Array {
    return Protobuf.encode<Testimonial>(message, (m, w) => {
      if (m.name.length > 0) w.string(1, m.name);
      if (m.content.length > 0) w.string(2, m.content);
    });
  }
  static decode(buffer: Uint8Array): Testimonial {
    return Protobuf.decode<Testimonial>(buffer, (r, l) => {
      const m = new Testimonial();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.name = r.string(); break;
          case 2: m.content = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class LandingPageContent {
  hero_title = "";
  hero_subtitle = "";
  features: Array<Feature> = new Array<Feature>();
  stats: Array<Stat> = new Array<Stat>();
  benefits: Array<string> = new Array<string>();
  testimonials: Array<Testimonial> = new Array<Testimonial>();
  cta_title = "";
  cta_subtitle = "";
  static encode(message: LandingPageContent): Uint8Array {
    return Protobuf.encode<LandingPageContent>(message, (m, w) => {
      if (m.hero_title.length > 0) w.string(1, m.hero_title);
      if (m.hero_subtitle.length > 0) w.string(2, m.hero_subtitle);
      for (let i = 0; i < m.features.length; i++) w.bytes(3, Feature.encode(m.features[i]));
      for (let i = 0; i < m.stats.length; i++) w.bytes(4, Stat.encode(m.stats[i]));
      for (let i = 0; i < m.benefits.length; i++) w.string(5, m.benefits[i]);
      for (let i = 0; i < m.testimonials.length; i++) w.bytes(6, Testimonial.encode(m.testimonials[i]));
      if (m.cta_title.length > 0) w.string(7, m.cta_title);
      if (m.cta_subtitle.length > 0) w.string(8, m.cta_subtitle);
    });
  }
  static decode(buffer: Uint8Array): LandingPageContent {
    return Protobuf.decode<LandingPageContent>(buffer, (r, l) => {
      const m = new LandingPageContent();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.hero_title = r.string(); break;
          case 2: m.hero_subtitle = r.string(); break;
          case 3: m.features.push(Feature.decode(r.bytes())); break;
          case 4: m.stats.push(Stat.decode(r.bytes())); break;
          case 5: m.benefits.push(r.string()); break;
          case 6: m.testimonials.push(Testimonial.decode(r.bytes())); break;
          case 7: m.cta_title = r.string(); break;
          case 8: m.cta_subtitle = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
