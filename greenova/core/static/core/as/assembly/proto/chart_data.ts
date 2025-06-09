// AssemblyScript Protobuf stubs for chart_data.proto
import { Protobuf } from "../as-proto/Protobuf";
import { Writer } from "../as-proto/Writer";
import { Reader } from "../as-proto/Reader";

export class AxisConfig {
  label = "";
  data_type = "";
  min_value: f64 = 0;
  max_value: f64 = 0;
  show_ticks: bool = false;
  static encode(message: AxisConfig): Uint8Array {
    return Protobuf.encode<AxisConfig>(message, (m, w) => {
      if (m.label.length > 0) w.string(1, m.label);
      if (m.data_type.length > 0) w.string(2, m.data_type);
      if (m.min_value != 0) w.double(3, m.min_value);
      if (m.max_value != 0) w.double(4, m.max_value);
      if (m.show_ticks) w.bool(5, m.show_ticks);
    });
  }
  static decode(buffer: Uint8Array): AxisConfig {
    return Protobuf.decode<AxisConfig>(buffer, (r, l) => {
      const m = new AxisConfig();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.label = r.string(); break;
          case 2: m.data_type = r.string(); break;
          case 3: m.min_value = r.double(); break;
          case 4: m.max_value = r.double(); break;
          case 5: m.show_ticks = r.bool(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChartConfig {
  width: i32 = 0;
  height: i32 = 0;
  color_scheme = "";
  show_legend: bool = false;
  show_grid: bool = false;
  x_axis: AxisConfig = new AxisConfig();
  y_axis: AxisConfig = new AxisConfig();
  static encode(message: ChartConfig): Uint8Array {
    return Protobuf.encode<ChartConfig>(message, (m, w) => {
      if (m.width != 0) w.int32(1, m.width);
      if (m.height != 0) w.int32(2, m.height);
      if (m.color_scheme.length > 0) w.string(3, m.color_scheme);
      if (m.show_legend) w.bool(4, m.show_legend);
      if (m.show_grid) w.bool(5, m.show_grid);
      w.bytes(6, AxisConfig.encode(m.x_axis));
      w.bytes(7, AxisConfig.encode(m.y_axis));
    });
  }
  static decode(buffer: Uint8Array): ChartConfig {
    return Protobuf.decode<ChartConfig>(buffer, (r, l) => {
      const m = new ChartConfig();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.width = r.int32(); break;
          case 2: m.height = r.int32(); break;
          case 3: m.color_scheme = r.string(); break;
          case 4: m.show_legend = r.bool(); break;
          case 5: m.show_grid = r.bool(); break;
          case 6: m.x_axis = AxisConfig.decode(r.bytes()); break;
          case 7: m.y_axis = AxisConfig.decode(r.bytes()); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class DataPoint {
  string_x = "";
  numeric_x: f64 = 0;
  timestamp_x: i64 = 0;
  y_value: f64 = 0;
  label = "";
  static encode(message: DataPoint): Uint8Array {
    return Protobuf.encode<DataPoint>(message, (m, w) => {
      if (m.string_x.length > 0) w.string(1, m.string_x);
      if (m.numeric_x != 0) w.double(2, m.numeric_x);
      if (m.timestamp_x != 0) w.int64(3, m.timestamp_x);
      if (m.y_value != 0) w.double(4, m.y_value);
      if (m.label.length > 0) w.string(5, m.label);
    });
  }
  static decode(buffer: Uint8Array): DataPoint {
    return Protobuf.decode<DataPoint>(buffer, (r, l) => {
      const m = new DataPoint();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.string_x = r.string(); break;
          case 2: m.numeric_x = r.double(); break;
          case 3: m.timestamp_x = r.int64(); break;
          case 4: m.y_value = r.double(); break;
          case 5: m.label = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class DataSeries {
  series_name = "";
  data_points: Array<DataPoint> = new Array<DataPoint>();
  color = "";
  line_style = "";
  static encode(message: DataSeries): Uint8Array {
    return Protobuf.encode<DataSeries>(message, (m, w) => {
      if (m.series_name.length > 0) w.string(1, m.series_name);
      for (let i = 0; i < m.data_points.length; i++) w.bytes(2, DataPoint.encode(m.data_points[i]));
      if (m.color.length > 0) w.string(3, m.color);
      if (m.line_style.length > 0) w.string(4, m.line_style);
    });
  }
  static decode(buffer: Uint8Array): DataSeries {
    return Protobuf.decode<DataSeries>(buffer, (r, l) => {
      const m = new DataSeries();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.series_name = r.string(); break;
          case 2: m.data_points.push(DataPoint.decode(r.bytes())); break;
          case 3: m.color = r.string(); break;
          case 4: m.line_style = r.string(); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChartMetadata {
  data_source = "";
  generated_at: i64 = 0;
  generated_by = "";
  tags: Array<string> = new Array<string>();
  static encode(message: ChartMetadata): Uint8Array {
    return Protobuf.encode<ChartMetadata>(message, (m, w) => {
      if (m.data_source.length > 0) w.string(1, m.data_source);
      if (m.generated_at != 0) w.int64(2, m.generated_at);
      if (m.generated_by.length > 0) w.string(3, m.generated_by);
      for (let i = 0; i < m.tags.length; i++) w.string(4, m.tags[i]);
    });
  }
  static decode(buffer: Uint8Array): ChartMetadata {
    return Protobuf.decode<ChartMetadata>(buffer, (r, l) => {
      const m = new ChartMetadata();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.data_source = r.string(); break;
          case 2: m.generated_at = r.int64(); break;
          case 3: m.generated_by = r.string(); break;
          case 4: m.tags.push(r.string()); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}

export class ChartData {
  chart_id = "";
  chart_type = "";
  title = "";
  config: ChartConfig = new ChartConfig();
  data_series: Array<DataSeries> = new Array<DataSeries>();
  metadata: ChartMetadata = new ChartMetadata();
  static encode(message: ChartData): Uint8Array {
    return Protobuf.encode<ChartData>(message, (m, w) => {
      if (m.chart_id.length > 0) w.string(1, m.chart_id);
      if (m.chart_type.length > 0) w.string(2, m.chart_type);
      if (m.title.length > 0) w.string(3, m.title);
      w.bytes(4, ChartConfig.encode(m.config));
      for (let i = 0; i < m.data_series.length; i++) w.bytes(5, DataSeries.encode(m.data_series[i]));
      w.bytes(6, ChartMetadata.encode(m.metadata));
    });
  }
  static decode(buffer: Uint8Array): ChartData {
    return Protobuf.decode<ChartData>(buffer, (r, l) => {
      const m = new ChartData();
      const end = l < 0 ? r.ptr + r.uint32() : r.ptr + l;
      while (r.ptr < end) {
        const tag = r.uint32();
        switch (tag >>> 3) {
          case 1: m.chart_id = r.string(); break;
          case 2: m.chart_type = r.string(); break;
          case 3: m.title = r.string(); break;
          case 4: m.config = ChartConfig.decode(r.bytes()); break;
          case 5: m.data_series.push(DataSeries.decode(r.bytes())); break;
          case 6: m.metadata = ChartMetadata.decode(r.bytes()); break;
          default: r.skipType(tag & 7); break;
        }
      }
      return m;
    });
  }
}
