// Frontend bridge for obligations Protobuf3 using as-proto/AssemblyScript WASM
// Handles fetch/decode for obligations data
export async function fetchObligations() {
    const resp = await fetch(window.OBLIGATIONS_API_URL + "?format=pb");
    if (!resp.ok)
        throw new Error(`HTTP error! status: ${resp.status}`);
    const buffer = new Uint8Array(await resp.arrayBuffer());
    const decoded = await window.decodeObligationProtoWasm(buffer);
    return decoded.obligations || [];
}
export async function decodeObligationProto(buffer) {
    return window.decodeObligationProtoWasm(buffer);
}
