// Frontend bridge for core and core_audit Protobuf3 using as-proto/AssemblyScript WASM
// Handles fetch/decode for core audit logs and core data
export async function fetchAuditLogs() {
    const resp = await fetch("/core/api/auditlogs.protobuf", {
        headers: { Accept: "application/x-protobuf" },
    });
    const buffer = new Uint8Array(await resp.arrayBuffer());
    const decoded = await window.decodeAuditLogCollectionWasm(buffer);
    return decoded.audit_logs || [];
}
export async function fetchCoreData() {
    const resp = await fetch("/core/api/coredata.protobuf", {
        headers: { Accept: "application/x-protobuf" },
    });
    const buffer = new Uint8Array(await resp.arrayBuffer());
    return window.decodeCoreProtoWasm(buffer);
}
