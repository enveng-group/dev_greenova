import { fetchObligations, decodeObligationProto } from "./proto";
describe("Obligations Protobuf Bridge", () => {
    it("fetchObligations calls WASM decode", async () => {
        const mockObligations = [{ id: 1 }, { id: 2 }];
        window.decodeObligationProtoWasm = jest.fn().mockResolvedValue({ obligations: mockObligations });
        window.OBLIGATIONS_API_URL = "/api/obligations";
        global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)),
        });
        const result = await fetchObligations();
        expect(result).toEqual(mockObligations);
    });
    it("decodeObligationProto calls WASM", async () => {
        const buffer = new Uint8Array([1, 2, 3]);
        window.decodeObligationProtoWasm = jest.fn().mockResolvedValue({ id: 1 });
        const result = await decodeObligationProto(buffer);
        expect(result).toEqual({ id: 1 });
    });
});
