// Frontend bridge for Greenova landing page Protobuf3 using as-proto/AssemblyScript WASM
// Handles fetch/decode for landing page content and newsletter signup
export async function fetchLandingPageContent() {
    const resp = await fetch("/landing/api/content.protobuf", {
        headers: { Accept: "application/x-protobuf" },
    });
    const buffer = new Uint8Array(await resp.arrayBuffer());
    return window.decodeLandingPageContentWasm(buffer);
}
export async function submitNewsletterSignup(email) {
    const encoded = await window.encodeNewsletterSignupRequestWasm({ email });
    const resp = await fetch("/landing/newsletter_signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-protobuf",
            Accept: "application/x-protobuf",
        },
        body: encoded,
    });
    const buffer = new Uint8Array(await resp.arrayBuffer());
    return window.decodeNewsletterSignupResponseWasm(buffer);
}
