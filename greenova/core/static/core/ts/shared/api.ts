// shared/api.ts
// Common API utilities for Greenova frontend

export async function fetchProtobuf(url: string): Promise<Uint8Array> {
  const resp = await fetch(url, { headers: { Accept: "application/x-protobuf" } });
  if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
  return new Uint8Array(await resp.arrayBuffer());
}

export function handleApiError(error: unknown): void {
  // Optionally log or display error
  // eslint-disable-next-line no-console
  console.error("API error:", error);
}
