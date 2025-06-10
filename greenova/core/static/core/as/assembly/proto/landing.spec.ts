import { NewsletterSignupRequest, NewsletterSignupResponse, Feature, Stat, Testimonial, LandingPageContent } from "./landing";
import { assert, describe, it } from "as-pect";

function assertEqual(a: unknown, b: unknown, msg: string = ""): void {
  assert(
    JSON.stringify(a) === JSON.stringify(b),
    msg || `Not equal: ${JSON.stringify(a)} !== ${JSON.stringify(b)}`
  );
}

describe("Landing Protobuf encode/decode", () => {
  it("NewsletterSignupRequest encode/decode roundtrip", () => {
    const req = new NewsletterSignupRequest();
    req.email = "test@example.com";
    const encoded = NewsletterSignupRequest.encode(req);
    const decoded = NewsletterSignupRequest.decode(encoded);
    assertEqual(decoded, req, "NewsletterSignupRequest roundtrip failed");
  });

  it("NewsletterSignupResponse encode/decode roundtrip", () => {
    const resp = new NewsletterSignupResponse();
    resp.success = true;
    resp.message = "Signed up!";
    const encoded = NewsletterSignupResponse.encode(resp);
    const decoded = NewsletterSignupResponse.decode(encoded);
    assertEqual(decoded, resp, "NewsletterSignupResponse roundtrip failed");
  });

  it("LandingPageContent encode/decode roundtrip", () => {
    const content = new LandingPageContent();
    content.hero_title = "Welcome";
    content.hero_subtitle = "To Greenova";
    content.features.push(Object.assign(new Feature(), { title: "F1", description: "D1" }));
    content.stats.push(Object.assign(new Stat(), { name: "Users", value: 42 }));
    content.benefits.push("Benefit1");
    content.testimonials.push(Object.assign(new Testimonial(), { name: "Alice", content: "Great!" }));
    content.cta_title = "Join";
    content.cta_subtitle = "Now";
    const encoded = LandingPageContent.encode(content);
    const decoded = LandingPageContent.decode(encoded);
    assertEqual(decoded, content, "LandingPageContent roundtrip failed");
  });

  it("NewsletterSignupRequest edge case: empty email", () => {
    const req = new NewsletterSignupRequest();
    req.email = "";
    const encoded = NewsletterSignupRequest.encode(req);
    const decoded = NewsletterSignupRequest.decode(encoded);
    assertEqual(decoded, req, "NewsletterSignupRequest empty email failed");
  });

  it("NewsletterSignupResponse edge case: false success, empty message", () => {
    const resp = new NewsletterSignupResponse();
    resp.success = false;
    resp.message = "";
    const encoded = NewsletterSignupResponse.encode(resp);
    const decoded = NewsletterSignupResponse.decode(encoded);
    assertEqual(decoded, resp, "NewsletterSignupResponse empty message failed");
  });
});
