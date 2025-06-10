// Frontend bridge for Greenova landing page Protobuf3 using as-proto/AssemblyScript WASM
// Handles fetch/decode for landing page content and newsletter signup

export async function fetchLandingPageContent(): Promise<any> {
  const resp = await fetch("/landing/api/content.protobuf", {
    headers: { Accept: "application/x-protobuf" },
  });
  const buffer = new Uint8Array(await resp.arrayBuffer());
  return (window as any).decodeLandingPageContentWasm(buffer);
}

export async function submitNewsletterSignup(email: string): Promise<any> {
  const encoded = await (window as any).encodeNewsletterSignupRequestWasm({ email });
  const resp = await fetch("/landing/newsletter_signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-protobuf",
      Accept: "application/x-protobuf",
    },
    body: encoded,
  });
  const buffer = new Uint8Array(await resp.arrayBuffer());
  return (window as any).decodeNewsletterSignupResponseWasm(buffer);
}
