import { fetchAuditLogs, fetchCoreData } from "./proto";
describe("Core Protobuf Bridge", () => {
    it("fetchAuditLogs calls WASM decode", async () => {
        const mockLogs = [{ id: "1" }, { id: "2" }];
        window.decodeAuditLogCollectionWasm = jest.fn().mockResolvedValue({ audit_logs: mockLogs });
        global.fetch = jest.fn().mockResolvedValue({
            arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
        });
        const result = await fetchAuditLogs();
        expect(result).toEqual(mockLogs);
    });
    it("fetchCoreData calls WASM decode", async () => {
        const mockCore = { key: "value" };
        window.decodeCoreProtoWasm = jest.fn().mockResolvedValue(mockCore);
        global.fetch = jest.fn().mockResolvedValue({
            arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
        });
        const result = await fetchCoreData();
        expect(result).toEqual(mockCore);
    });
});
