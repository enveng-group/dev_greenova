export const enum ComplianceStatus {
  COMPLIANT = "COMPLIANT",
  WARNING = "WARNING",
  NON_COMPLIANT = "NON_COMPLIANT",
  UNKNOWN = "UNKNOWN",
}

export const encodeComplianceStatus: { [key: string]: number } = {
  COMPLIANT: 0,
  WARNING: 1,
  NON_COMPLIANT: 2,
  UNKNOWN: 3,
};

export const decodeComplianceStatus: { [key: number]: ComplianceStatus } = {
  0: ComplianceStatus.COMPLIANT,
  1: ComplianceStatus.WARNING,
  2: ComplianceStatus.NON_COMPLIANT,
  3: ComplianceStatus.UNKNOWN,
};

export interface ChartData {
  chart_id?: string;
  chart_type?: string;
  title?: string;
  config?: ChartConfig;
  data_series?: DataSeries[];
  metadata?: ChartMetadata;
}

export function encodeChartData(message: ChartData): Uint8Array {
  let bb = popByteBuffer();
  _encodeChartData(message, bb);
  return toUint8Array(bb);
}

function _encodeChartData(message: ChartData, bb: ByteBuffer): void {
  // optional string chart_id = 1;
  let $chart_id = message.chart_id;
  if ($chart_id !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $chart_id);
  }

  // optional string chart_type = 2;
  let $chart_type = message.chart_type;
  if ($chart_type !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $chart_type);
  }

  // optional string title = 3;
  let $title = message.title;
  if ($title !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $title);
  }

  // optional ChartConfig config = 4;
  let $config = message.config;
  if ($config !== undefined) {
    writeVarint32(bb, 34);
    let nested = popByteBuffer();
    _encodeChartConfig($config, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // repeated DataSeries data_series = 5;
  let array$data_series = message.data_series;
  if (array$data_series !== undefined) {
    for (let value of array$data_series) {
      writeVarint32(bb, 42);
      let nested = popByteBuffer();
      _encodeDataSeries(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional ChartMetadata metadata = 6;
  let $metadata = message.metadata;
  if ($metadata !== undefined) {
    writeVarint32(bb, 50);
    let nested = popByteBuffer();
    _encodeChartMetadata($metadata, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }
}

export function decodeChartData(binary: Uint8Array): ChartData {
  return _decodeChartData(wrapByteBuffer(binary));
}

function _decodeChartData(bb: ByteBuffer): ChartData {
  let message: ChartData = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string chart_id = 1;
      case 1: {
        message.chart_id = readString(bb, readVarint32(bb));
        break;
      }

      // optional string chart_type = 2;
      case 2: {
        message.chart_type = readString(bb, readVarint32(bb));
        break;
      }

      // optional string title = 3;
      case 3: {
        message.title = readString(bb, readVarint32(bb));
        break;
      }

      // optional ChartConfig config = 4;
      case 4: {
        let limit = pushTemporaryLength(bb);
        message.config = _decodeChartConfig(bb);
        bb.limit = limit;
        break;
      }

      // repeated DataSeries data_series = 5;
      case 5: {
        let limit = pushTemporaryLength(bb);
        let values = message.data_series || (message.data_series = []);
        values.push(_decodeDataSeries(bb));
        bb.limit = limit;
        break;
      }

      // optional ChartMetadata metadata = 6;
      case 6: {
        let limit = pushTemporaryLength(bb);
        message.metadata = _decodeChartMetadata(bb);
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ChartConfig {
  width?: number;
  height?: number;
  color_scheme?: string;
  show_legend?: boolean;
  show_grid?: boolean;
  x_axis?: AxisConfig;
  y_axis?: AxisConfig;
}

export function encodeChartConfig(message: ChartConfig): Uint8Array {
  let bb = popByteBuffer();
  _encodeChartConfig(message, bb);
  return toUint8Array(bb);
}

function _encodeChartConfig(message: ChartConfig, bb: ByteBuffer): void {
  // optional int32 width = 1;
  let $width = message.width;
  if ($width !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($width));
  }

  // optional int32 height = 2;
  let $height = message.height;
  if ($height !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($height));
  }

  // optional string color_scheme = 3;
  let $color_scheme = message.color_scheme;
  if ($color_scheme !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $color_scheme);
  }

  // optional bool show_legend = 4;
  let $show_legend = message.show_legend;
  if ($show_legend !== undefined) {
    writeVarint32(bb, 32);
    writeByte(bb, $show_legend ? 1 : 0);
  }

  // optional bool show_grid = 5;
  let $show_grid = message.show_grid;
  if ($show_grid !== undefined) {
    writeVarint32(bb, 40);
    writeByte(bb, $show_grid ? 1 : 0);
  }

  // optional AxisConfig x_axis = 6;
  let $x_axis = message.x_axis;
  if ($x_axis !== undefined) {
    writeVarint32(bb, 50);
    let nested = popByteBuffer();
    _encodeAxisConfig($x_axis, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional AxisConfig y_axis = 7;
  let $y_axis = message.y_axis;
  if ($y_axis !== undefined) {
    writeVarint32(bb, 58);
    let nested = popByteBuffer();
    _encodeAxisConfig($y_axis, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }
}

export function decodeChartConfig(binary: Uint8Array): ChartConfig {
  return _decodeChartConfig(wrapByteBuffer(binary));
}

function _decodeChartConfig(bb: ByteBuffer): ChartConfig {
  let message: ChartConfig = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 width = 1;
      case 1: {
        message.width = readVarint32(bb);
        break;
      }

      // optional int32 height = 2;
      case 2: {
        message.height = readVarint32(bb);
        break;
      }

      // optional string color_scheme = 3;
      case 3: {
        message.color_scheme = readString(bb, readVarint32(bb));
        break;
      }

      // optional bool show_legend = 4;
      case 4: {
        message.show_legend = !!readByte(bb);
        break;
      }

      // optional bool show_grid = 5;
      case 5: {
        message.show_grid = !!readByte(bb);
        break;
      }

      // optional AxisConfig x_axis = 6;
      case 6: {
        let limit = pushTemporaryLength(bb);
        message.x_axis = _decodeAxisConfig(bb);
        bb.limit = limit;
        break;
      }

      // optional AxisConfig y_axis = 7;
      case 7: {
        let limit = pushTemporaryLength(bb);
        message.y_axis = _decodeAxisConfig(bb);
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface AxisConfig {
  label?: string;
  data_type?: string;
  min_value?: number;
  max_value?: number;
  show_ticks?: boolean;
}

export function encodeAxisConfig(message: AxisConfig): Uint8Array {
  let bb = popByteBuffer();
  _encodeAxisConfig(message, bb);
  return toUint8Array(bb);
}

function _encodeAxisConfig(message: AxisConfig, bb: ByteBuffer): void {
  // optional string label = 1;
  let $label = message.label;
  if ($label !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $label);
  }

  // optional string data_type = 2;
  let $data_type = message.data_type;
  if ($data_type !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $data_type);
  }

  // optional double min_value = 3;
  let $min_value = message.min_value;
  if ($min_value !== undefined) {
    writeVarint32(bb, 25);
    writeDouble(bb, $min_value);
  }

  // optional double max_value = 4;
  let $max_value = message.max_value;
  if ($max_value !== undefined) {
    writeVarint32(bb, 33);
    writeDouble(bb, $max_value);
  }

  // optional bool show_ticks = 5;
  let $show_ticks = message.show_ticks;
  if ($show_ticks !== undefined) {
    writeVarint32(bb, 40);
    writeByte(bb, $show_ticks ? 1 : 0);
  }
}

export function decodeAxisConfig(binary: Uint8Array): AxisConfig {
  return _decodeAxisConfig(wrapByteBuffer(binary));
}

function _decodeAxisConfig(bb: ByteBuffer): AxisConfig {
  let message: AxisConfig = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string label = 1;
      case 1: {
        message.label = readString(bb, readVarint32(bb));
        break;
      }

      // optional string data_type = 2;
      case 2: {
        message.data_type = readString(bb, readVarint32(bb));
        break;
      }

      // optional double min_value = 3;
      case 3: {
        message.min_value = readDouble(bb);
        break;
      }

      // optional double max_value = 4;
      case 4: {
        message.max_value = readDouble(bb);
        break;
      }

      // optional bool show_ticks = 5;
      case 5: {
        message.show_ticks = !!readByte(bb);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface DataSeries {
  series_name?: string;
  data_points?: DataPoint[];
  color?: string;
  line_style?: string;
}

export function encodeDataSeries(message: DataSeries): Uint8Array {
  let bb = popByteBuffer();
  _encodeDataSeries(message, bb);
  return toUint8Array(bb);
}

function _encodeDataSeries(message: DataSeries, bb: ByteBuffer): void {
  // optional string series_name = 1;
  let $series_name = message.series_name;
  if ($series_name !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $series_name);
  }

  // repeated DataPoint data_points = 2;
  let array$data_points = message.data_points;
  if (array$data_points !== undefined) {
    for (let value of array$data_points) {
      writeVarint32(bb, 18);
      let nested = popByteBuffer();
      _encodeDataPoint(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional string color = 3;
  let $color = message.color;
  if ($color !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $color);
  }

  // optional string line_style = 4;
  let $line_style = message.line_style;
  if ($line_style !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $line_style);
  }
}

export function decodeDataSeries(binary: Uint8Array): DataSeries {
  return _decodeDataSeries(wrapByteBuffer(binary));
}

function _decodeDataSeries(bb: ByteBuffer): DataSeries {
  let message: DataSeries = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string series_name = 1;
      case 1: {
        message.series_name = readString(bb, readVarint32(bb));
        break;
      }

      // repeated DataPoint data_points = 2;
      case 2: {
        let limit = pushTemporaryLength(bb);
        let values = message.data_points || (message.data_points = []);
        values.push(_decodeDataPoint(bb));
        bb.limit = limit;
        break;
      }

      // optional string color = 3;
      case 3: {
        message.color = readString(bb, readVarint32(bb));
        break;
      }

      // optional string line_style = 4;
      case 4: {
        message.line_style = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface DataPoint {
  string_x?: string;
  numeric_x?: number;
  timestamp_x?: Long;
  y_value?: number;
  label?: string;
  metadata?: { [key: string]: string };
}

export function encodeDataPoint(message: DataPoint): Uint8Array {
  let bb = popByteBuffer();
  _encodeDataPoint(message, bb);
  return toUint8Array(bb);
}

function _encodeDataPoint(message: DataPoint, bb: ByteBuffer): void {
  // optional string string_x = 1;
  let $string_x = message.string_x;
  if ($string_x !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $string_x);
  }

  // optional double numeric_x = 2;
  let $numeric_x = message.numeric_x;
  if ($numeric_x !== undefined) {
    writeVarint32(bb, 17);
    writeDouble(bb, $numeric_x);
  }

  // optional int64 timestamp_x = 3;
  let $timestamp_x = message.timestamp_x;
  if ($timestamp_x !== undefined) {
    writeVarint32(bb, 24);
    writeVarint64(bb, $timestamp_x);
  }

  // optional double y_value = 4;
  let $y_value = message.y_value;
  if ($y_value !== undefined) {
    writeVarint32(bb, 33);
    writeDouble(bb, $y_value);
  }

  // optional string label = 5;
  let $label = message.label;
  if ($label !== undefined) {
    writeVarint32(bb, 42);
    writeString(bb, $label);
  }

  // optional map<string, string> metadata = 6;
  let map$metadata = message.metadata;
  if (map$metadata !== undefined) {
    for (let key in map$metadata) {
      let nested = popByteBuffer();
      let value = map$metadata[key];
      writeVarint32(nested, 10);
      writeString(nested, key);
      writeVarint32(nested, 18);
      writeString(nested, value);
      writeVarint32(bb, 50);
      writeVarint32(bb, nested.offset);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }
}

export function decodeDataPoint(binary: Uint8Array): DataPoint {
  return _decodeDataPoint(wrapByteBuffer(binary));
}

function _decodeDataPoint(bb: ByteBuffer): DataPoint {
  let message: DataPoint = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string string_x = 1;
      case 1: {
        message.string_x = readString(bb, readVarint32(bb));
        break;
      }

      // optional double numeric_x = 2;
      case 2: {
        message.numeric_x = readDouble(bb);
        break;
      }

      // optional int64 timestamp_x = 3;
      case 3: {
        message.timestamp_x = readVarint64(bb, /* unsigned */ false);
        break;
      }

      // optional double y_value = 4;
      case 4: {
        message.y_value = readDouble(bb);
        break;
      }

      // optional string label = 5;
      case 5: {
        message.label = readString(bb, readVarint32(bb));
        break;
      }

      // optional map<string, string> metadata = 6;
      case 6: {
        let values = message.metadata || (message.metadata = {});
        let outerLimit = pushTemporaryLength(bb);
        let key: string | undefined;
        let value: string | undefined;
        end_of_entry: while (!isAtEnd(bb)) {
          let tag = readVarint32(bb);
          switch (tag >>> 3) {
            case 0:
              break end_of_entry;
            case 1: {
              key = readString(bb, readVarint32(bb));
              break;
            }
            case 2: {
              value = readString(bb, readVarint32(bb));
              break;
            }
            default:
              skipUnknownField(bb, tag & 7);
          }
        }
        if (key === undefined || value === undefined)
          throw new Error("Invalid data for map: metadata");
        values[key] = value;
        bb.limit = outerLimit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface ChartMetadata {
  data_source?: string;
  generated_at?: Long;
  generated_by?: string;
  tags?: string[];
}

export function encodeChartMetadata(message: ChartMetadata): Uint8Array {
  let bb = popByteBuffer();
  _encodeChartMetadata(message, bb);
  return toUint8Array(bb);
}

function _encodeChartMetadata(message: ChartMetadata, bb: ByteBuffer): void {
  // optional string data_source = 1;
  let $data_source = message.data_source;
  if ($data_source !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $data_source);
  }

  // optional int64 generated_at = 2;
  let $generated_at = message.generated_at;
  if ($generated_at !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, $generated_at);
  }

  // optional string generated_by = 3;
  let $generated_by = message.generated_by;
  if ($generated_by !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $generated_by);
  }

  // repeated string tags = 4;
  let array$tags = message.tags;
  if (array$tags !== undefined) {
    for (let value of array$tags) {
      writeVarint32(bb, 34);
      writeString(bb, value);
    }
  }
}

export function decodeChartMetadata(binary: Uint8Array): ChartMetadata {
  return _decodeChartMetadata(wrapByteBuffer(binary));
}

function _decodeChartMetadata(bb: ByteBuffer): ChartMetadata {
  let message: ChartMetadata = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string data_source = 1;
      case 1: {
        message.data_source = readString(bb, readVarint32(bb));
        break;
      }

      // optional int64 generated_at = 2;
      case 2: {
        message.generated_at = readVarint64(bb, /* unsigned */ false);
        break;
      }

      // optional string generated_by = 3;
      case 3: {
        message.generated_by = readString(bb, readVarint32(bb));
        break;
      }

      // repeated string tags = 4;
      case 4: {
        let values = message.tags || (message.tags = []);
        values.push(readString(bb, readVarint32(bb)));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface EnvironmentalMetricsChart {
  metric_type?: string;
  measurement_unit?: string;
  metric_points?: MetricDataPoint[];
  thresholds?: MetricThresholds;
}

export function encodeEnvironmentalMetricsChart(message: EnvironmentalMetricsChart): Uint8Array {
  let bb = popByteBuffer();
  _encodeEnvironmentalMetricsChart(message, bb);
  return toUint8Array(bb);
}

function _encodeEnvironmentalMetricsChart(message: EnvironmentalMetricsChart, bb: ByteBuffer): void {
  // optional string metric_type = 1;
  let $metric_type = message.metric_type;
  if ($metric_type !== undefined) {
    writeVarint32(bb, 10);
    writeString(bb, $metric_type);
  }

  // optional string measurement_unit = 2;
  let $measurement_unit = message.measurement_unit;
  if ($measurement_unit !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $measurement_unit);
  }

  // repeated MetricDataPoint metric_points = 3;
  let array$metric_points = message.metric_points;
  if (array$metric_points !== undefined) {
    for (let value of array$metric_points) {
      writeVarint32(bb, 26);
      let nested = popByteBuffer();
      _encodeMetricDataPoint(value, nested);
      writeVarint32(bb, nested.limit);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional MetricThresholds thresholds = 4;
  let $thresholds = message.thresholds;
  if ($thresholds !== undefined) {
    writeVarint32(bb, 34);
    let nested = popByteBuffer();
    _encodeMetricThresholds($thresholds, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }
}

export function decodeEnvironmentalMetricsChart(binary: Uint8Array): EnvironmentalMetricsChart {
  return _decodeEnvironmentalMetricsChart(wrapByteBuffer(binary));
}

function _decodeEnvironmentalMetricsChart(bb: ByteBuffer): EnvironmentalMetricsChart {
  let message: EnvironmentalMetricsChart = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional string metric_type = 1;
      case 1: {
        message.metric_type = readString(bb, readVarint32(bb));
        break;
      }

      // optional string measurement_unit = 2;
      case 2: {
        message.measurement_unit = readString(bb, readVarint32(bb));
        break;
      }

      // repeated MetricDataPoint metric_points = 3;
      case 3: {
        let limit = pushTemporaryLength(bb);
        let values = message.metric_points || (message.metric_points = []);
        values.push(_decodeMetricDataPoint(bb));
        bb.limit = limit;
        break;
      }

      // optional MetricThresholds thresholds = 4;
      case 4: {
        let limit = pushTemporaryLength(bb);
        message.thresholds = _decodeMetricThresholds(bb);
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface MetricDataPoint {
  timestamp?: Long;
  value?: number;
  location?: string;
  measurement_method?: string;
  compliance_status?: ComplianceStatus;
}

export function encodeMetricDataPoint(message: MetricDataPoint): Uint8Array {
  let bb = popByteBuffer();
  _encodeMetricDataPoint(message, bb);
  return toUint8Array(bb);
}

function _encodeMetricDataPoint(message: MetricDataPoint, bb: ByteBuffer): void {
  // optional int64 timestamp = 1;
  let $timestamp = message.timestamp;
  if ($timestamp !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, $timestamp);
  }

  // optional double value = 2;
  let $value = message.value;
  if ($value !== undefined) {
    writeVarint32(bb, 17);
    writeDouble(bb, $value);
  }

  // optional string location = 3;
  let $location = message.location;
  if ($location !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $location);
  }

  // optional string measurement_method = 4;
  let $measurement_method = message.measurement_method;
  if ($measurement_method !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $measurement_method);
  }

  // optional ComplianceStatus compliance_status = 5;
  let $compliance_status = message.compliance_status;
  if ($compliance_status !== undefined) {
    writeVarint32(bb, 40);
    writeVarint32(bb, encodeComplianceStatus[$compliance_status]);
  }
}

export function decodeMetricDataPoint(binary: Uint8Array): MetricDataPoint {
  return _decodeMetricDataPoint(wrapByteBuffer(binary));
}

function _decodeMetricDataPoint(bb: ByteBuffer): MetricDataPoint {
  let message: MetricDataPoint = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int64 timestamp = 1;
      case 1: {
        message.timestamp = readVarint64(bb, /* unsigned */ false);
        break;
      }

      // optional double value = 2;
      case 2: {
        message.value = readDouble(bb);
        break;
      }

      // optional string location = 3;
      case 3: {
        message.location = readString(bb, readVarint32(bb));
        break;
      }

      // optional string measurement_method = 4;
      case 4: {
        message.measurement_method = readString(bb, readVarint32(bb));
        break;
      }

      // optional ComplianceStatus compliance_status = 5;
      case 5: {
        message.compliance_status = decodeComplianceStatus[readVarint32(bb)];
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface MetricThresholds {
  warning_threshold?: number;
  critical_threshold?: number;
  target_value?: number;
}

export function encodeMetricThresholds(message: MetricThresholds): Uint8Array {
  let bb = popByteBuffer();
  _encodeMetricThresholds(message, bb);
  return toUint8Array(bb);
}

function _encodeMetricThresholds(message: MetricThresholds, bb: ByteBuffer): void {
  // optional double warning_threshold = 1;
  let $warning_threshold = message.warning_threshold;
  if ($warning_threshold !== undefined) {
    writeVarint32(bb, 9);
    writeDouble(bb, $warning_threshold);
  }

  // optional double critical_threshold = 2;
  let $critical_threshold = message.critical_threshold;
  if ($critical_threshold !== undefined) {
    writeVarint32(bb, 17);
    writeDouble(bb, $critical_threshold);
  }

  // optional double target_value = 3;
  let $target_value = message.target_value;
  if ($target_value !== undefined) {
    writeVarint32(bb, 25);
    writeDouble(bb, $target_value);
  }
}

export function decodeMetricThresholds(binary: Uint8Array): MetricThresholds {
  return _decodeMetricThresholds(wrapByteBuffer(binary));
}

function _decodeMetricThresholds(bb: ByteBuffer): MetricThresholds {
  let message: MetricThresholds = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional double warning_threshold = 1;
      case 1: {
        message.warning_threshold = readDouble(bb);
        break;
      }

      // optional double critical_threshold = 2;
      case 2: {
        message.critical_threshold = readDouble(bb);
        break;
      }

      // optional double target_value = 3;
      case 3: {
        message.target_value = readDouble(bb);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface Long {
  low: number;
  high: number;
  unsigned: boolean;
}

interface ByteBuffer {
  bytes: Uint8Array;
  offset: number;
  limit: number;
}

function pushTemporaryLength(bb: ByteBuffer): number {
  let length = readVarint32(bb);
  let limit = bb.limit;
  bb.limit = bb.offset + length;
  return limit;
}

function skipUnknownField(bb: ByteBuffer, type: number): void {
  switch (type) {
    case 0: while (readByte(bb) & 0x80) { } break;
    case 2: skip(bb, readVarint32(bb)); break;
    case 5: skip(bb, 4); break;
    case 1: skip(bb, 8); break;
    default: throw new Error("Unimplemented type: " + type);
  }
}

function stringToLong(value: string): Long {
  return {
    low: value.charCodeAt(0) | (value.charCodeAt(1) << 16),
    high: value.charCodeAt(2) | (value.charCodeAt(3) << 16),
    unsigned: false,
  };
}

function longToString(value: Long): string {
  let low = value.low;
  let high = value.high;
  return String.fromCharCode(
    low & 0xFFFF,
    low >>> 16,
    high & 0xFFFF,
    high >>> 16);
}

// The code below was modified from https://github.com/protobufjs/bytebuffer.js
// which is under the Apache License 2.0.

let f32 = new Float32Array(1);
let f32_u8 = new Uint8Array(f32.buffer);

let f64 = new Float64Array(1);
let f64_u8 = new Uint8Array(f64.buffer);

function intToLong(value: number): Long {
  value |= 0;
  return {
    low: value,
    high: value >> 31,
    unsigned: value >= 0,
  };
}

let bbStack: ByteBuffer[] = [];

function popByteBuffer(): ByteBuffer {
  const bb = bbStack.pop();
  if (!bb) return { bytes: new Uint8Array(64), offset: 0, limit: 0 };
  bb.offset = bb.limit = 0;
  return bb;
}

function pushByteBuffer(bb: ByteBuffer): void {
  bbStack.push(bb);
}

function wrapByteBuffer(bytes: Uint8Array): ByteBuffer {
  return { bytes, offset: 0, limit: bytes.length };
}

function toUint8Array(bb: ByteBuffer): Uint8Array {
  let bytes = bb.bytes;
  let limit = bb.limit;
  return bytes.length === limit ? bytes : bytes.subarray(0, limit);
}

function skip(bb: ByteBuffer, offset: number): void {
  if (bb.offset + offset > bb.limit) {
    throw new Error('Skip past limit');
  }
  bb.offset += offset;
}

function isAtEnd(bb: ByteBuffer): boolean {
  return bb.offset >= bb.limit;
}

function grow(bb: ByteBuffer, count: number): number {
  let bytes = bb.bytes;
  let offset = bb.offset;
  let limit = bb.limit;
  let finalOffset = offset + count;
  if (finalOffset > bytes.length) {
    let newBytes = new Uint8Array(finalOffset * 2);
    newBytes.set(bytes);
    bb.bytes = newBytes;
  }
  bb.offset = finalOffset;
  if (finalOffset > limit) {
    bb.limit = finalOffset;
  }
  return offset;
}

function advance(bb: ByteBuffer, count: number): number {
  let offset = bb.offset;
  if (offset + count > bb.limit) {
    throw new Error('Read past limit');
  }
  bb.offset += count;
  return offset;
}

function readBytes(bb: ByteBuffer, count: number): Uint8Array {
  let offset = advance(bb, count);
  return bb.bytes.subarray(offset, offset + count);
}

function writeBytes(bb: ByteBuffer, buffer: Uint8Array): void {
  let offset = grow(bb, buffer.length);
  bb.bytes.set(buffer, offset);
}

function readString(bb: ByteBuffer, count: number): string {
  // Sadly a hand-coded UTF8 decoder is much faster than subarray+TextDecoder in V8
  let offset = advance(bb, count);
  let fromCharCode = String.fromCharCode;
  let bytes = bb.bytes;
  let invalid = '\uFFFD';
  let text = '';

  for (let i = 0; i < count; i++) {
    let c1 = bytes[i + offset], c2: number, c3: number, c4: number, c: number;

    // 1 byte
    if ((c1 & 0x80) === 0) {
      text += fromCharCode(c1);
    }

    // 2 bytes
    else if ((c1 & 0xE0) === 0xC0) {
      if (i + 1 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        if ((c2 & 0xC0) !== 0x80) text += invalid;
        else {
          c = ((c1 & 0x1F) << 6) | (c2 & 0x3F);
          if (c < 0x80) text += invalid;
          else {
            text += fromCharCode(c);
            i++;
          }
        }
      }
    }

    // 3 bytes
    else if ((c1 & 0xF0) == 0xE0) {
      if (i + 2 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        c3 = bytes[i + offset + 2];
        if (((c2 | (c3 << 8)) & 0xC0C0) !== 0x8080) text += invalid;
        else {
          c = ((c1 & 0x0F) << 12) | ((c2 & 0x3F) << 6) | (c3 & 0x3F);
          if (c < 0x0800 || (c >= 0xD800 && c <= 0xDFFF)) text += invalid;
          else {
            text += fromCharCode(c);
            i += 2;
          }
        }
      }
    }

    // 4 bytes
    else if ((c1 & 0xF8) == 0xF0) {
      if (i + 3 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        c3 = bytes[i + offset + 2];
        c4 = bytes[i + offset + 3];
        if (((c2 | (c3 << 8) | (c4 << 16)) & 0xC0C0C0) !== 0x808080) text += invalid;
        else {
          c = ((c1 & 0x07) << 0x12) | ((c2 & 0x3F) << 0x0C) | ((c3 & 0x3F) << 0x06) | (c4 & 0x3F);
          if (c < 0x10000 || c > 0x10FFFF) text += invalid;
          else {
            c -= 0x10000;
            text += fromCharCode((c >> 10) + 0xD800, (c & 0x3FF) + 0xDC00);
            i += 3;
          }
        }
      }
    }

    else text += invalid;
  }

  return text;
}

function writeString(bb: ByteBuffer, text: string): void {
  // Sadly a hand-coded UTF8 encoder is much faster than TextEncoder+set in V8
  let n = text.length;
  let byteCount = 0;

  // Write the byte count first
  for (let i = 0; i < n; i++) {
    let c = text.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF && i + 1 < n) {
      c = (c << 10) + text.charCodeAt(++i) - 0x35FDC00;
    }
    byteCount += c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4;
  }
  writeVarint32(bb, byteCount);

  let offset = grow(bb, byteCount);
  let bytes = bb.bytes;

  // Then write the bytes
  for (let i = 0; i < n; i++) {
    let c = text.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF && i + 1 < n) {
      c = (c << 10) + text.charCodeAt(++i) - 0x35FDC00;
    }
    if (c < 0x80) {
      bytes[offset++] = c;
    } else {
      if (c < 0x800) {
        bytes[offset++] = ((c >> 6) & 0x1F) | 0xC0;
      } else {
        if (c < 0x10000) {
          bytes[offset++] = ((c >> 12) & 0x0F) | 0xE0;
        } else {
          bytes[offset++] = ((c >> 18) & 0x07) | 0xF0;
          bytes[offset++] = ((c >> 12) & 0x3F) | 0x80;
        }
        bytes[offset++] = ((c >> 6) & 0x3F) | 0x80;
      }
      bytes[offset++] = (c & 0x3F) | 0x80;
    }
  }
}

function writeByteBuffer(bb: ByteBuffer, buffer: ByteBuffer): void {
  let offset = grow(bb, buffer.limit);
  let from = bb.bytes;
  let to = buffer.bytes;

  // This for loop is much faster than subarray+set on V8
  for (let i = 0, n = buffer.limit; i < n; i++) {
    from[i + offset] = to[i];
  }
}

function readByte(bb: ByteBuffer): number {
  return bb.bytes[advance(bb, 1)];
}

function writeByte(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 1);
  bb.bytes[offset] = value;
}

function readFloat(bb: ByteBuffer): number {
  let offset = advance(bb, 4);
  let bytes = bb.bytes;

  // Manual copying is much faster than subarray+set in V8
  f32_u8[0] = bytes[offset++];
  f32_u8[1] = bytes[offset++];
  f32_u8[2] = bytes[offset++];
  f32_u8[3] = bytes[offset++];
  return f32[0];
}

function writeFloat(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 4);
  let bytes = bb.bytes;
  f32[0] = value;

  // Manual copying is much faster than subarray+set in V8
  bytes[offset++] = f32_u8[0];
  bytes[offset++] = f32_u8[1];
  bytes[offset++] = f32_u8[2];
  bytes[offset++] = f32_u8[3];
}

function readDouble(bb: ByteBuffer): number {
  let offset = advance(bb, 8);
  let bytes = bb.bytes;

  // Manual copying is much faster than subarray+set in V8
  f64_u8[0] = bytes[offset++];
  f64_u8[1] = bytes[offset++];
  f64_u8[2] = bytes[offset++];
  f64_u8[3] = bytes[offset++];
  f64_u8[4] = bytes[offset++];
  f64_u8[5] = bytes[offset++];
  f64_u8[6] = bytes[offset++];
  f64_u8[7] = bytes[offset++];
  return f64[0];
}

function writeDouble(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 8);
  let bytes = bb.bytes;
  f64[0] = value;

  // Manual copying is much faster than subarray+set in V8
  bytes[offset++] = f64_u8[0];
  bytes[offset++] = f64_u8[1];
  bytes[offset++] = f64_u8[2];
  bytes[offset++] = f64_u8[3];
  bytes[offset++] = f64_u8[4];
  bytes[offset++] = f64_u8[5];
  bytes[offset++] = f64_u8[6];
  bytes[offset++] = f64_u8[7];
}

function readInt32(bb: ByteBuffer): number {
  let offset = advance(bb, 4);
  let bytes = bb.bytes;
  return (
    bytes[offset] |
    (bytes[offset + 1] << 8) |
    (bytes[offset + 2] << 16) |
    (bytes[offset + 3] << 24)
  );
}

function writeInt32(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 4);
  let bytes = bb.bytes;
  bytes[offset] = value;
  bytes[offset + 1] = value >> 8;
  bytes[offset + 2] = value >> 16;
  bytes[offset + 3] = value >> 24;
}

function readInt64(bb: ByteBuffer, unsigned: boolean): Long {
  return {
    low: readInt32(bb),
    high: readInt32(bb),
    unsigned,
  };
}

function writeInt64(bb: ByteBuffer, value: Long): void {
  writeInt32(bb, value.low);
  writeInt32(bb, value.high);
}

function readVarint32(bb: ByteBuffer): number {
  let c = 0;
  let value = 0;
  let b: number;
  do {
    b = readByte(bb);
    if (c < 32) value |= (b & 0x7F) << c;
    c += 7;
  } while (b & 0x80);
  return value;
}

function writeVarint32(bb: ByteBuffer, value: number): void {
  value >>>= 0;
  while (value >= 0x80) {
    writeByte(bb, (value & 0x7f) | 0x80);
    value >>>= 7;
  }
  writeByte(bb, value);
}

function readVarint64(bb: ByteBuffer, unsigned: boolean): Long {
  let part0 = 0;
  let part1 = 0;
  let part2 = 0;
  let b: number;

  b = readByte(bb); part0 = (b & 0x7F); if (b & 0x80) {
    b = readByte(bb); part0 |= (b & 0x7F) << 7; if (b & 0x80) {
      b = readByte(bb); part0 |= (b & 0x7F) << 14; if (b & 0x80) {
        b = readByte(bb); part0 |= (b & 0x7F) << 21; if (b & 0x80) {

          b = readByte(bb); part1 = (b & 0x7F); if (b & 0x80) {
            b = readByte(bb); part1 |= (b & 0x7F) << 7; if (b & 0x80) {
              b = readByte(bb); part1 |= (b & 0x7F) << 14; if (b & 0x80) {
                b = readByte(bb); part1 |= (b & 0x7F) << 21; if (b & 0x80) {

                  b = readByte(bb); part2 = (b & 0x7F); if (b & 0x80) {
                    b = readByte(bb); part2 |= (b & 0x7F) << 7;
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  return {
    low: part0 | (part1 << 28),
    high: (part1 >>> 4) | (part2 << 24),
    unsigned,
  };
}

function writeVarint64(bb: ByteBuffer, value: Long): void {
  let part0 = value.low >>> 0;
  let part1 = ((value.low >>> 28) | (value.high << 4)) >>> 0;
  let part2 = value.high >>> 24;

  // ref: src/google/protobuf/io/coded_stream.cc
  let size =
    part2 === 0 ?
      part1 === 0 ?
        part0 < 1 << 14 ?
          part0 < 1 << 7 ? 1 : 2 :
          part0 < 1 << 21 ? 3 : 4 :
        part1 < 1 << 14 ?
          part1 < 1 << 7 ? 5 : 6 :
          part1 < 1 << 21 ? 7 : 8 :
      part2 < 1 << 7 ? 9 : 10;

  let offset = grow(bb, size);
  let bytes = bb.bytes;

  switch (size) {
    case 10: bytes[offset + 9] = (part2 >>> 7) & 0x01;
    case 9: bytes[offset + 8] = size !== 9 ? part2 | 0x80 : part2 & 0x7F;
    case 8: bytes[offset + 7] = size !== 8 ? (part1 >>> 21) | 0x80 : (part1 >>> 21) & 0x7F;
    case 7: bytes[offset + 6] = size !== 7 ? (part1 >>> 14) | 0x80 : (part1 >>> 14) & 0x7F;
    case 6: bytes[offset + 5] = size !== 6 ? (part1 >>> 7) | 0x80 : (part1 >>> 7) & 0x7F;
    case 5: bytes[offset + 4] = size !== 5 ? part1 | 0x80 : part1 & 0x7F;
    case 4: bytes[offset + 3] = size !== 4 ? (part0 >>> 21) | 0x80 : (part0 >>> 21) & 0x7F;
    case 3: bytes[offset + 2] = size !== 3 ? (part0 >>> 14) | 0x80 : (part0 >>> 14) & 0x7F;
    case 2: bytes[offset + 1] = size !== 2 ? (part0 >>> 7) | 0x80 : (part0 >>> 7) & 0x7F;
    case 1: bytes[offset] = size !== 1 ? part0 | 0x80 : part0 & 0x7F;
  }
}

function readVarint32ZigZag(bb: ByteBuffer): number {
  let value = readVarint32(bb);

  // ref: src/google/protobuf/wire_format_lite.h
  return (value >>> 1) ^ -(value & 1);
}

function writeVarint32ZigZag(bb: ByteBuffer, value: number): void {
  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint32(bb, (value << 1) ^ (value >> 31));
}

function readVarint64ZigZag(bb: ByteBuffer): Long {
  let value = readVarint64(bb, /* unsigned */ false);
  let low = value.low;
  let high = value.high;
  let flip = -(low & 1);

  // ref: src/google/protobuf/wire_format_lite.h
  return {
    low: ((low >>> 1) | (high << 31)) ^ flip,
    high: (high >>> 1) ^ flip,
    unsigned: false,
  };
}

function writeVarint64ZigZag(bb: ByteBuffer, value: Long): void {
  let low = value.low;
  let high = value.high;
  let flip = high >> 31;

  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint64(bb, {
    low: (low << 1) ^ flip,
    high: ((high << 1) | (low >>> 31)) ^ flip,
    unsigned: false,
  });
}
