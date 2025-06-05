// SPDX-License-Identifier: AGPL-3.0-or-later
// Unified JS/TS glue code for AssemblyScript WASM and protobuf3 endpoints
// and generated protobuf message classes (using protobufjs).
// Example assumes BugReportProto is generated and available in JS/TS
// import { BugReportProto } from './generated/greenova_pb';
export async function sendProtobuf(url, binary) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/octet-stream",
            "X-Requested-With": "XMLHttpRequest",
        },
        body: binary,
        credentials: "same-origin",
    });
    return response.status;
}
export async function fetchProtobuf(url) {
    const response = await fetch(url, {
        method: "GET",
        headers: {
            Accept: "application/octet-stream",
            "X-Requested-With": "XMLHttpRequest",
        },
        credentials: "same-origin",
    });
    if (!response.ok)
        throw new Error("Failed to fetch protobuf data");
    return await response.arrayBuffer();
}
// Example usage:
// import { BugReportProto } from './generated/greenova_pb';
// async function uploadBugReport(report: BugReportProto) {
//   const binary = BugReportProto.encode(report).finish();
//   const status = await sendProtobuf('/feedback/import/', binary);
//   // handle status
// }
// async function downloadBugReport(id: number) {
//   const binary = await fetchProtobuf(`/feedback/export/${id}/`);
//   const report = BugReportProto.decode(new Uint8Array(binary));
//   // use report
// }
