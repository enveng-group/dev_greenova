// Frontend bridge for obligations Protobuf3 using as-proto/AssemblyScript WASM
// Handles fetch/decode for obligations data

export async function fetchObligations(): Promise<any[]> {
  const resp = await fetch((window as any).OBLIGATIONS_API_URL + "?format=pb");
  if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
  const buffer = new Uint8Array(await resp.arrayBuffer());
  const decoded = await (window as any).decodeObligationProtoWasm(buffer);
  return decoded.obligations || [];
}

export async function decodeObligationProto(buffer: Uint8Array): Promise<any> {
  return (window as any).decodeObligationProtoWasm(buffer);
}
