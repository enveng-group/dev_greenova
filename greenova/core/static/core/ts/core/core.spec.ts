import { fetchAuditLogs, fetchCoreData } from "./proto";

describe("Core Protobuf Bridge", () => {
  it("fetchAuditLogs calls WASM decode", async () => {
    const mockLogs = [{ id: "1" }, { id: "2" }];
    (window as any).decodeAuditLogCollectionWasm = jest.fn().mockResolvedValue({ audit_logs: mockLogs });
    global.fetch = jest.fn().mockResolvedValue({
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
    }) as any;
    const result = await fetchAuditLogs();
    expect(result).toEqual(mockLogs);
  });

  it("fetchCoreData calls WASM decode", async () => {
    const mockCore = { key: "value" };
    (window as any).decodeCoreProtoWasm = jest.fn().mockResolvedValue(mockCore);
    global.fetch = jest.fn().mockResolvedValue({
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
    }) as any;
    const result = await fetchCoreData();
    expect(result).toEqual(mockCore);
  });
});
