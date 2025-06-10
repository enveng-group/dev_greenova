import { fetchLandingPageContent, submitNewsletterSignup } from "./proto";

describe("Landing Protobuf Bridge", () => {
  it("fetchLandingPageContent calls WASM decode", async () => {
    const mockContent = { hero_title: "Test Hero" };
    (window as any).decodeLandingPageContentWasm = jest.fn().mockResolvedValue(mockContent);
    global.fetch = jest.fn().mockResolvedValue({
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
    }) as any;
    const result = await fetchLandingPageContent();
    expect(result).toEqual(mockContent);
  });

  it("submitNewsletterSignup encodes and decodes via WASM", async () => {
    (window as any).encodeNewsletterSignupRequestWasm = jest.fn().mockResolvedValue(new Uint8Array([1, 2, 3]));
    (window as any).decodeNewsletterSignupResponseWasm = jest.fn().mockResolvedValue({ success: true, message: "ok" });
    global.fetch = jest.fn().mockResolvedValue({
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
    }) as any;
    const result = await submitNewsletterSignup("test@example.com");
    expect(result).toEqual({ success: true, message: "ok" });
  });
});
