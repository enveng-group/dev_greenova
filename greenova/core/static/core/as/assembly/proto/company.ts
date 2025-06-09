// AssemblyScript Protobuf stubs for company.proto
// Generated for as-proto runtime
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class Company {
  id = "";
  name = "";
  address = "";
  email = "";

  static encode(message: Company): Uint8Array {
    return Protobuf.encode<Company>(message, (m, w) => {
      if (m.id.length > 0) w.string(1, m.id);
      if (m.name.length > 0) w.string(2, m.name);
      if (m.address.length > 0) w.string(3, m.address);
      if (m.email.length > 0) w.string(4, m.email);
    });
  }
  static decode(buffer: Uint8Array): Company {
    return Protobuf.decode<Company>(buffer, (r, l) => {
      const m = new Company();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.id = r.string(); break;
          case 2: m.name = r.string(); break;
          case 3: m.address = r.string(); break;
          case 4: m.email = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class CompanyList {
  companies: Array<Company> = new Array<Company>();
  error = "";

  static encode(message: CompanyList): Uint8Array {
    return Protobuf.encode<CompanyList>(message, (m, w) => {
      for (let i = 0; i < m.companies.length; i++) w.bytes(1, Company.encode(m.companies[i]));
      if (m.error.length > 0) w.string(2, m.error);
    });
  }
  static decode(buffer: Uint8Array): CompanyList {
    return Protobuf.decode<CompanyList>(buffer, (r, l) => {
      const m = new CompanyList();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.companies.push(Company.decode(r.bytes())); break;
          case 2: m.error = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
