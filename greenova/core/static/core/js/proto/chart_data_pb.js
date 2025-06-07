export const encodeComplianceStatus = {
  COMPLIANT: 0,
  WARNING: 1,
  NON_COMPLIANT: 2,
  UNKNOWN: 3
}

export const decodeComplianceStatus = {
  0: 'COMPLIANT',
  1: 'WARNING',
  2: 'NON_COMPLIANT',
  3: 'UNKNOWN'
}

export function encodeChartData (message) {
  const bb = popByteBuffer()
  _encodeChartData(message, bb)
  return toUint8Array(bb)
}

function _encodeChartData (message, bb) {
  // optional string chart_id = 1;
  const $chart_id = message.chart_id
  if ($chart_id !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $chart_id)
  }

  // optional string chart_type = 2;
  const $chart_type = message.chart_type
  if ($chart_type !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $chart_type)
  }

  // optional string title = 3;
  const $title = message.title
  if ($title !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $title)
  }

  // optional ChartConfig config = 4;
  const $config = message.config
  if ($config !== undefined) {
    writeVarint32(bb, 34)
    const nested = popByteBuffer()
    _encodeChartConfig($config, nested)
    writeVarint32(bb, nested.limit)
    writeByteBuffer(bb, nested)
    pushByteBuffer(nested)
  }

  // repeated DataSeries data_series = 5;
  const array$data_series = message.data_series
  if (array$data_series !== undefined) {
    for (const value of array$data_series) {
      writeVarint32(bb, 42)
      const nested = popByteBuffer()
      _encodeDataSeries(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }

  // optional ChartMetadata metadata = 6;
  const $metadata = message.metadata
  if ($metadata !== undefined) {
    writeVarint32(bb, 50)
    const nested = popByteBuffer()
    _encodeChartMetadata($metadata, nested)
    writeVarint32(bb, nested.limit)
    writeByteBuffer(bb, nested)
    pushByteBuffer(nested)
  }
}

export function decodeChartData (binary) {
  return _decodeChartData(wrapByteBuffer(binary))
}

function _decodeChartData (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string chart_id = 1;
      case 1: {
        message.chart_id = readString(bb, readVarint32(bb))
        break
      }

      // optional string chart_type = 2;
      case 2: {
        message.chart_type = readString(bb, readVarint32(bb))
        break
      }

      // optional string title = 3;
      case 3: {
        message.title = readString(bb, readVarint32(bb))
        break
      }

      // optional ChartConfig config = 4;
      case 4: {
        const limit = pushTemporaryLength(bb)
        message.config = _decodeChartConfig(bb)
        bb.limit = limit
        break
      }

      // repeated DataSeries data_series = 5;
      case 5: {
        const limit = pushTemporaryLength(bb)
        const values = message.data_series || (message.data_series = [])
        values.push(_decodeDataSeries(bb))
        bb.limit = limit
        break
      }

      // optional ChartMetadata metadata = 6;
      case 6: {
        const limit = pushTemporaryLength(bb)
        message.metadata = _decodeChartMetadata(bb)
        bb.limit = limit
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeChartConfig (message) {
  const bb = popByteBuffer()
  _encodeChartConfig(message, bb)
  return toUint8Array(bb)
}

function _encodeChartConfig (message, bb) {
  // optional int32 width = 1;
  const $width = message.width
  if ($width !== undefined) {
    writeVarint32(bb, 8)
    writeVarint64(bb, intToLong($width))
  }

  // optional int32 height = 2;
  const $height = message.height
  if ($height !== undefined) {
    writeVarint32(bb, 16)
    writeVarint64(bb, intToLong($height))
  }

  // optional string color_scheme = 3;
  const $color_scheme = message.color_scheme
  if ($color_scheme !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $color_scheme)
  }

  // optional bool show_legend = 4;
  const $show_legend = message.show_legend
  if ($show_legend !== undefined) {
    writeVarint32(bb, 32)
    writeByte(bb, $show_legend ? 1 : 0)
  }

  // optional bool show_grid = 5;
  const $show_grid = message.show_grid
  if ($show_grid !== undefined) {
    writeVarint32(bb, 40)
    writeByte(bb, $show_grid ? 1 : 0)
  }

  // optional AxisConfig x_axis = 6;
  const $x_axis = message.x_axis
  if ($x_axis !== undefined) {
    writeVarint32(bb, 50)
    const nested = popByteBuffer()
    _encodeAxisConfig($x_axis, nested)
    writeVarint32(bb, nested.limit)
    writeByteBuffer(bb, nested)
    pushByteBuffer(nested)
  }

  // optional AxisConfig y_axis = 7;
  const $y_axis = message.y_axis
  if ($y_axis !== undefined) {
    writeVarint32(bb, 58)
    const nested = popByteBuffer()
    _encodeAxisConfig($y_axis, nested)
    writeVarint32(bb, nested.limit)
    writeByteBuffer(bb, nested)
    pushByteBuffer(nested)
  }
}

export function decodeChartConfig (binary) {
  return _decodeChartConfig(wrapByteBuffer(binary))
}

function _decodeChartConfig (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional int32 width = 1;
      case 1: {
        message.width = readVarint32(bb)
        break
      }

      // optional int32 height = 2;
      case 2: {
        message.height = readVarint32(bb)
        break
      }

      // optional string color_scheme = 3;
      case 3: {
        message.color_scheme = readString(bb, readVarint32(bb))
        break
      }

      // optional bool show_legend = 4;
      case 4: {
        message.show_legend = !!readByte(bb)
        break
      }

      // optional bool show_grid = 5;
      case 5: {
        message.show_grid = !!readByte(bb)
        break
      }

      // optional AxisConfig x_axis = 6;
      case 6: {
        const limit = pushTemporaryLength(bb)
        message.x_axis = _decodeAxisConfig(bb)
        bb.limit = limit
        break
      }

      // optional AxisConfig y_axis = 7;
      case 7: {
        const limit = pushTemporaryLength(bb)
        message.y_axis = _decodeAxisConfig(bb)
        bb.limit = limit
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeAxisConfig (message) {
  const bb = popByteBuffer()
  _encodeAxisConfig(message, bb)
  return toUint8Array(bb)
}

function _encodeAxisConfig (message, bb) {
  // optional string label = 1;
  const $label = message.label
  if ($label !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $label)
  }

  // optional string data_type = 2;
  const $data_type = message.data_type
  if ($data_type !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $data_type)
  }

  // optional double min_value = 3;
  const $min_value = message.min_value
  if ($min_value !== undefined) {
    writeVarint32(bb, 25)
    writeDouble(bb, $min_value)
  }

  // optional double max_value = 4;
  const $max_value = message.max_value
  if ($max_value !== undefined) {
    writeVarint32(bb, 33)
    writeDouble(bb, $max_value)
  }

  // optional bool show_ticks = 5;
  const $show_ticks = message.show_ticks
  if ($show_ticks !== undefined) {
    writeVarint32(bb, 40)
    writeByte(bb, $show_ticks ? 1 : 0)
  }
}

export function decodeAxisConfig (binary) {
  return _decodeAxisConfig(wrapByteBuffer(binary))
}

function _decodeAxisConfig (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string label = 1;
      case 1: {
        message.label = readString(bb, readVarint32(bb))
        break
      }

      // optional string data_type = 2;
      case 2: {
        message.data_type = readString(bb, readVarint32(bb))
        break
      }

      // optional double min_value = 3;
      case 3: {
        message.min_value = readDouble(bb)
        break
      }

      // optional double max_value = 4;
      case 4: {
        message.max_value = readDouble(bb)
        break
      }

      // optional bool show_ticks = 5;
      case 5: {
        message.show_ticks = !!readByte(bb)
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeDataSeries (message) {
  const bb = popByteBuffer()
  _encodeDataSeries(message, bb)
  return toUint8Array(bb)
}

function _encodeDataSeries (message, bb) {
  // optional string series_name = 1;
  const $series_name = message.series_name
  if ($series_name !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $series_name)
  }

  // repeated DataPoint data_points = 2;
  const array$data_points = message.data_points
  if (array$data_points !== undefined) {
    for (const value of array$data_points) {
      writeVarint32(bb, 18)
      const nested = popByteBuffer()
      _encodeDataPoint(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }

  // optional string color = 3;
  const $color = message.color
  if ($color !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $color)
  }

  // optional string line_style = 4;
  const $line_style = message.line_style
  if ($line_style !== undefined) {
    writeVarint32(bb, 34)
    writeString(bb, $line_style)
  }
}

export function decodeDataSeries (binary) {
  return _decodeDataSeries(wrapByteBuffer(binary))
}

function _decodeDataSeries (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string series_name = 1;
      case 1: {
        message.series_name = readString(bb, readVarint32(bb))
        break
      }

      // repeated DataPoint data_points = 2;
      case 2: {
        const limit = pushTemporaryLength(bb)
        const values = message.data_points || (message.data_points = [])
        values.push(_decodeDataPoint(bb))
        bb.limit = limit
        break
      }

      // optional string color = 3;
      case 3: {
        message.color = readString(bb, readVarint32(bb))
        break
      }

      // optional string line_style = 4;
      case 4: {
        message.line_style = readString(bb, readVarint32(bb))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeDataPoint (message) {
  const bb = popByteBuffer()
  _encodeDataPoint(message, bb)
  return toUint8Array(bb)
}

function _encodeDataPoint (message, bb) {
  // optional string string_x = 1;
  const $string_x = message.string_x
  if ($string_x !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $string_x)
  }

  // optional double numeric_x = 2;
  const $numeric_x = message.numeric_x
  if ($numeric_x !== undefined) {
    writeVarint32(bb, 17)
    writeDouble(bb, $numeric_x)
  }

  // optional int64 timestamp_x = 3;
  const $timestamp_x = message.timestamp_x
  if ($timestamp_x !== undefined) {
    writeVarint32(bb, 24)
    writeVarint64(bb, $timestamp_x)
  }

  // optional double y_value = 4;
  const $y_value = message.y_value
  if ($y_value !== undefined) {
    writeVarint32(bb, 33)
    writeDouble(bb, $y_value)
  }

  // optional string label = 5;
  const $label = message.label
  if ($label !== undefined) {
    writeVarint32(bb, 42)
    writeString(bb, $label)
  }

  // optional map<string, string> metadata = 6;
  const map$metadata = message.metadata
  if (map$metadata !== undefined) {
    for (const key in map$metadata) {
      const nested = popByteBuffer()
      const value = map$metadata[key]
      writeVarint32(nested, 10)
      writeString(nested, key)
      writeVarint32(nested, 18)
      writeString(nested, value)
      writeVarint32(bb, 50)
      writeVarint32(bb, nested.offset)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }
}

export function decodeDataPoint (binary) {
  return _decodeDataPoint(wrapByteBuffer(binary))
}

function _decodeDataPoint (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string string_x = 1;
      case 1: {
        message.string_x = readString(bb, readVarint32(bb))
        break
      }

      // optional double numeric_x = 2;
      case 2: {
        message.numeric_x = readDouble(bb)
        break
      }

      // optional int64 timestamp_x = 3;
      case 3: {
        message.timestamp_x = readVarint64(bb, /* unsigned */ false)
        break
      }

      // optional double y_value = 4;
      case 4: {
        message.y_value = readDouble(bb)
        break
      }

      // optional string label = 5;
      case 5: {
        message.label = readString(bb, readVarint32(bb))
        break
      }

      // optional map<string, string> metadata = 6;
      case 6: {
        const values = message.metadata || (message.metadata = {})
        const outerLimit = pushTemporaryLength(bb)
        let key
        let value
        end_of_entry: while (!isAtEnd(bb)) {
          const tag = readVarint32(bb)
          switch (tag >>> 3) {
            case 0:
              break end_of_entry
            case 1: {
              key = readString(bb, readVarint32(bb))
              break
            }
            case 2: {
              value = readString(bb, readVarint32(bb))
              break
            }
            default:
              skipUnknownField(bb, tag & 7)
          }
        }
        if (key === undefined || value === undefined) {
          throw new Error('Invalid data for map: metadata')
        }
        values[key] = value
        bb.limit = outerLimit
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeChartMetadata (message) {
  const bb = popByteBuffer()
  _encodeChartMetadata(message, bb)
  return toUint8Array(bb)
}

function _encodeChartMetadata (message, bb) {
  // optional string data_source = 1;
  const $data_source = message.data_source
  if ($data_source !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $data_source)
  }

  // optional int64 generated_at = 2;
  const $generated_at = message.generated_at
  if ($generated_at !== undefined) {
    writeVarint32(bb, 16)
    writeVarint64(bb, $generated_at)
  }

  // optional string generated_by = 3;
  const $generated_by = message.generated_by
  if ($generated_by !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $generated_by)
  }

  // repeated string tags = 4;
  const array$tags = message.tags
  if (array$tags !== undefined) {
    for (const value of array$tags) {
      writeVarint32(bb, 34)
      writeString(bb, value)
    }
  }
}

export function decodeChartMetadata (binary) {
  return _decodeChartMetadata(wrapByteBuffer(binary))
}

function _decodeChartMetadata (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string data_source = 1;
      case 1: {
        message.data_source = readString(bb, readVarint32(bb))
        break
      }

      // optional int64 generated_at = 2;
      case 2: {
        message.generated_at = readVarint64(bb, /* unsigned */ false)
        break
      }

      // optional string generated_by = 3;
      case 3: {
        message.generated_by = readString(bb, readVarint32(bb))
        break
      }

      // repeated string tags = 4;
      case 4: {
        const values = message.tags || (message.tags = [])
        values.push(readString(bb, readVarint32(bb)))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeEnvironmentalMetricsChart (message) {
  const bb = popByteBuffer()
  _encodeEnvironmentalMetricsChart(message, bb)
  return toUint8Array(bb)
}

function _encodeEnvironmentalMetricsChart (message, bb) {
  // optional string metric_type = 1;
  const $metric_type = message.metric_type
  if ($metric_type !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $metric_type)
  }

  // optional string measurement_unit = 2;
  const $measurement_unit = message.measurement_unit
  if ($measurement_unit !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $measurement_unit)
  }

  // repeated MetricDataPoint metric_points = 3;
  const array$metric_points = message.metric_points
  if (array$metric_points !== undefined) {
    for (const value of array$metric_points) {
      writeVarint32(bb, 26)
      const nested = popByteBuffer()
      _encodeMetricDataPoint(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }

  // optional MetricThresholds thresholds = 4;
  const $thresholds = message.thresholds
  if ($thresholds !== undefined) {
    writeVarint32(bb, 34)
    const nested = popByteBuffer()
    _encodeMetricThresholds($thresholds, nested)
    writeVarint32(bb, nested.limit)
    writeByteBuffer(bb, nested)
    pushByteBuffer(nested)
  }
}

export function decodeEnvironmentalMetricsChart (binary) {
  return _decodeEnvironmentalMetricsChart(wrapByteBuffer(binary))
}

function _decodeEnvironmentalMetricsChart (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string metric_type = 1;
      case 1: {
        message.metric_type = readString(bb, readVarint32(bb))
        break
      }

      // optional string measurement_unit = 2;
      case 2: {
        message.measurement_unit = readString(bb, readVarint32(bb))
        break
      }

      // repeated MetricDataPoint metric_points = 3;
      case 3: {
        const limit = pushTemporaryLength(bb)
        const values = message.metric_points || (message.metric_points = [])
        values.push(_decodeMetricDataPoint(bb))
        bb.limit = limit
        break
      }

      // optional MetricThresholds thresholds = 4;
      case 4: {
        const limit = pushTemporaryLength(bb)
        message.thresholds = _decodeMetricThresholds(bb)
        bb.limit = limit
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeMetricDataPoint (message) {
  const bb = popByteBuffer()
  _encodeMetricDataPoint(message, bb)
  return toUint8Array(bb)
}

function _encodeMetricDataPoint (message, bb) {
  // optional int64 timestamp = 1;
  const $timestamp = message.timestamp
  if ($timestamp !== undefined) {
    writeVarint32(bb, 8)
    writeVarint64(bb, $timestamp)
  }

  // optional double value = 2;
  const $value = message.value
  if ($value !== undefined) {
    writeVarint32(bb, 17)
    writeDouble(bb, $value)
  }

  // optional string location = 3;
  const $location = message.location
  if ($location !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $location)
  }

  // optional string measurement_method = 4;
  const $measurement_method = message.measurement_method
  if ($measurement_method !== undefined) {
    writeVarint32(bb, 34)
    writeString(bb, $measurement_method)
  }

  // optional ComplianceStatus compliance_status = 5;
  const $compliance_status = message.compliance_status
  if ($compliance_status !== undefined) {
    writeVarint32(bb, 40)
    writeVarint32(bb, encodeComplianceStatus[$compliance_status])
  }
}

export function decodeMetricDataPoint (binary) {
  return _decodeMetricDataPoint(wrapByteBuffer(binary))
}

function _decodeMetricDataPoint (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional int64 timestamp = 1;
      case 1: {
        message.timestamp = readVarint64(bb, /* unsigned */ false)
        break
      }

      // optional double value = 2;
      case 2: {
        message.value = readDouble(bb)
        break
      }

      // optional string location = 3;
      case 3: {
        message.location = readString(bb, readVarint32(bb))
        break
      }

      // optional string measurement_method = 4;
      case 4: {
        message.measurement_method = readString(bb, readVarint32(bb))
        break
      }

      // optional ComplianceStatus compliance_status = 5;
      case 5: {
        message.compliance_status = decodeComplianceStatus[readVarint32(bb)]
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeMetricThresholds (message) {
  const bb = popByteBuffer()
  _encodeMetricThresholds(message, bb)
  return toUint8Array(bb)
}

function _encodeMetricThresholds (message, bb) {
  // optional double warning_threshold = 1;
  const $warning_threshold = message.warning_threshold
  if ($warning_threshold !== undefined) {
    writeVarint32(bb, 9)
    writeDouble(bb, $warning_threshold)
  }

  // optional double critical_threshold = 2;
  const $critical_threshold = message.critical_threshold
  if ($critical_threshold !== undefined) {
    writeVarint32(bb, 17)
    writeDouble(bb, $critical_threshold)
  }

  // optional double target_value = 3;
  const $target_value = message.target_value
  if ($target_value !== undefined) {
    writeVarint32(bb, 25)
    writeDouble(bb, $target_value)
  }
}

export function decodeMetricThresholds (binary) {
  return _decodeMetricThresholds(wrapByteBuffer(binary))
}

function _decodeMetricThresholds (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional double warning_threshold = 1;
      case 1: {
        message.warning_threshold = readDouble(bb)
        break
      }

      // optional double critical_threshold = 2;
      case 2: {
        message.critical_threshold = readDouble(bb)
        break
      }

      // optional double target_value = 3;
      case 3: {
        message.target_value = readDouble(bb)
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

function pushTemporaryLength (bb) {
  const length = readVarint32(bb)
  const limit = bb.limit
  bb.limit = bb.offset + length
  return limit
}

function skipUnknownField (bb, type) {
  switch (type) {
    case 0:
      while (readByte(bb) & 0x80) {}
      break
    case 2:
      skip(bb, readVarint32(bb))
      break
    case 5:
      skip(bb, 4)
      break
    case 1:
      skip(bb, 8)
      break
    default:
      throw new Error('Unimplemented type: ' + type)
  }
}

function stringToLong (value) {
  return {
    low: value.charCodeAt(0) | (value.charCodeAt(1) << 16),
    high: value.charCodeAt(2) | (value.charCodeAt(3) << 16),
    unsigned: false
  }
}

function longToString (value) {
  const low = value.low
  const high = value.high
  return String.fromCharCode(
    low & 0xffff,
    low >>> 16,
    high & 0xffff,
    high >>> 16
  )
}

// The code below was modified from https://github.com/protobufjs/bytebuffer.js
// which is under the Apache License 2.0.

const f32 = new Float32Array(1)
const f32_u8 = new Uint8Array(f32.buffer)

const f64 = new Float64Array(1)
const f64_u8 = new Uint8Array(f64.buffer)

function intToLong (value) {
  value |= 0
  return {
    low: value,
    high: value >> 31,
    unsigned: value >= 0
  }
}

const bbStack = []

function popByteBuffer () {
  const bb = bbStack.pop()
  if (!bb) {
    return { bytes: new Uint8Array(64), offset: 0, limit: 0 }
  }
  bb.offset = bb.limit = 0
  return bb
}

function pushByteBuffer (bb) {
  bbStack.push(bb)
}

function wrapByteBuffer (bytes) {
  return { bytes, offset: 0, limit: bytes.length }
}

function toUint8Array (bb) {
  const bytes = bb.bytes
  const limit = bb.limit
  return bytes.length === limit ? bytes : bytes.subarray(0, limit)
}

function skip (bb, offset) {
  if (bb.offset + offset > bb.limit) {
    throw new Error('Skip past limit')
  }
  bb.offset += offset
}

function isAtEnd (bb) {
  return bb.offset >= bb.limit
}

function grow (bb, count) {
  const bytes = bb.bytes
  const offset = bb.offset
  const limit = bb.limit
  const finalOffset = offset + count
  if (finalOffset > bytes.length) {
    const newBytes = new Uint8Array(finalOffset * 2)
    newBytes.set(bytes)
    bb.bytes = newBytes
  }
  bb.offset = finalOffset
  if (finalOffset > limit) {
    bb.limit = finalOffset
  }
  return offset
}

function advance (bb, count) {
  const offset = bb.offset
  if (offset + count > bb.limit) {
    throw new Error('Read past limit')
  }
  bb.offset += count
  return offset
}

function readBytes (bb, count) {
  const offset = advance(bb, count)
  return bb.bytes.subarray(offset, offset + count)
}

function writeBytes (bb, buffer) {
  const offset = grow(bb, buffer.length)
  bb.bytes.set(buffer, offset)
}

function readString (bb, count) {
  // Sadly a hand-coded UTF8 decoder is much faster than subarray+TextDecoder in V8
  const offset = advance(bb, count)
  const fromCharCode = String.fromCharCode
  const bytes = bb.bytes
  const invalid = '\uFFFD'
  let text = ''

  for (let i = 0; i < count; i += 1) {
    const c1 = bytes[i + offset]
    let c2
    let c3
    let c4
    let c

    // 1 byte
    if ((c1 & 0x80) === 0) {
      text += fromCharCode(c1)
    }

    // 2 bytes
    else if ((c1 & 0xe0) === 0xc0) {
      if (i + 1 >= count) {
        text += invalid
      } else {
        c2 = bytes[i + offset + 1]
        if ((c2 & 0xc0) !== 0x80) {
          text += invalid
        } else {
          c = ((c1 & 0x1f) << 6) | (c2 & 0x3f)
          if (c < 0x80) {
            text += invalid
          } else {
            text += fromCharCode(c)
            i += 1
          }
        }
      }
    }

    // 3 bytes
    else if ((c1 & 0xf0) == 0xe0) {
      if (i + 2 >= count) {
        text += invalid
      } else {
        c2 = bytes[i + offset + 1]
        c3 = bytes[i + offset + 2]
        if (((c2 | (c3 << 8)) & 0xc0c0) !== 0x8080) {
          text += invalid
        } else {
          c = ((c1 & 0x0f) << 12) | ((c2 & 0x3f) << 6) | (c3 & 0x3f)
          if (c < 0x0800 || (c >= 0xd800 && c <= 0xdfff)) {
            text += invalid
          } else {
            text += fromCharCode(c)
            i += 2
          }
        }
      }
    }

    // 4 bytes
    else if ((c1 & 0xf8) == 0xf0) {
      if (i + 3 >= count) {
        text += invalid
      } else {
        c2 = bytes[i + offset + 1]
        c3 = bytes[i + offset + 2]
        c4 = bytes[i + offset + 3]
        if (((c2 | (c3 << 8) | (c4 << 16)) & 0xc0c0c0) !== 0x808080) {
          text += invalid
        } else {
          c =
            ((c1 & 0x07) << 0x12) |
            ((c2 & 0x3f) << 0x0c) |
            ((c3 & 0x3f) << 0x06) |
            (c4 & 0x3f)
          if (c < 0x10000 || c > 0x10ffff) {
            text += invalid
          } else {
            c -= 0x10000
            text += fromCharCode((c >> 10) + 0xd800, (c & 0x3ff) + 0xdc00)
            i += 3
          }
        }
      }
    } else {
      text += invalid
    }
  }

  return text
}

function writeString (bb, text) {
  // Sadly a hand-coded UTF8 encoder is much faster than TextEncoder+set in V8
  const n = text.length
  let byteCount = 0

  // Write the byte count first
  for (let i = 0; i < n; i += 1) {
    let c = text.charCodeAt(i)
    if (c >= 0xd800 && c <= 0xdbff && i + 1 < n) {
      c = (c << 10) + text.charCodeAt((i += 1)) - 0x35fdc00
    }
    byteCount += c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4
  }
  writeVarint32(bb, byteCount)

  let offset = grow(bb, byteCount)
  const bytes = bb.bytes

  // Then write the bytes
  for (let i = 0; i < n; i += 1) {
    let c = text.charCodeAt(i)
    if (c >= 0xd800 && c <= 0xdbff && i + 1 < n) {
      c = (c << 10) + text.charCodeAt((i += 1)) - 0x35fdc00
    }
    if (c < 0x80) {
      bytes[(offset += 1)] = c
    } else {
      if (c < 0x800) {
        bytes[(offset += 1)] = ((c >> 6) & 0x1f) | 0xc0
      } else {
        if (c < 0x10000) {
          bytes[(offset += 1)] = ((c >> 12) & 0x0f) | 0xe0
        } else {
          bytes[(offset += 1)] = ((c >> 18) & 0x07) | 0xf0
          bytes[(offset += 1)] = ((c >> 12) & 0x3f) | 0x80
        }
        bytes[(offset += 1)] = ((c >> 6) & 0x3f) | 0x80
      }
      bytes[(offset += 1)] = (c & 0x3f) | 0x80
    }
  }
}

function writeByteBuffer (bb, buffer) {
  const offset = grow(bb, buffer.limit)
  const from = bb.bytes
  const to = buffer.bytes

  // This for loop is much faster than subarray+set on V8
  for (let i = 0, n = buffer.limit; i < n; i += 1) {
    from[i + offset] = to[i]
  }
}

function readByte (bb) {
  return bb.bytes[advance(bb, 1)]
}

function writeByte (bb, value) {
  const offset = grow(bb, 1)
  bb.bytes[offset] = value
}

function readFloat (bb) {
  let offset = advance(bb, 4)
  const bytes = bb.bytes

  // Manual copying is much faster than subarray+set in V8
  f32_u8[0] = bytes[(offset += 1)]
  f32_u8[1] = bytes[(offset += 1)]
  f32_u8[2] = bytes[(offset += 1)]
  f32_u8[3] = bytes[(offset += 1)]
  return f32[0]
}

function writeFloat (bb, value) {
  let offset = grow(bb, 4)
  const bytes = bb.bytes
  f32[0] = value

  // Manual copying is much faster than subarray+set in V8
  bytes[(offset += 1)] = f32_u8[0]
  bytes[(offset += 1)] = f32_u8[1]
  bytes[(offset += 1)] = f32_u8[2]
  bytes[(offset += 1)] = f32_u8[3]
}

function readDouble (bb) {
  let offset = advance(bb, 8)
  const bytes = bb.bytes

  // Manual copying is much faster than subarray+set in V8
  f64_u8[0] = bytes[(offset += 1)]
  f64_u8[1] = bytes[(offset += 1)]
  f64_u8[2] = bytes[(offset += 1)]
  f64_u8[3] = bytes[(offset += 1)]
  f64_u8[4] = bytes[(offset += 1)]
  f64_u8[5] = bytes[(offset += 1)]
  f64_u8[6] = bytes[(offset += 1)]
  f64_u8[7] = bytes[(offset += 1)]
  return f64[0]
}

function writeDouble (bb, value) {
  let offset = grow(bb, 8)
  const bytes = bb.bytes
  f64[0] = value

  // Manual copying is much faster than subarray+set in V8
  bytes[(offset += 1)] = f64_u8[0]
  bytes[(offset += 1)] = f64_u8[1]
  bytes[(offset += 1)] = f64_u8[2]
  bytes[(offset += 1)] = f64_u8[3]
  bytes[(offset += 1)] = f64_u8[4]
  bytes[(offset += 1)] = f64_u8[5]
  bytes[(offset += 1)] = f64_u8[6]
  bytes[(offset += 1)] = f64_u8[7]
}

function readInt32 (bb) {
  const offset = advance(bb, 4)
  const bytes = bb.bytes
  return (
    bytes[offset] |
    (bytes[offset + 1] << 8) |
    (bytes[offset + 2] << 16) |
    (bytes[offset + 3] << 24)
  )
}

function writeInt32 (bb, value) {
  const offset = grow(bb, 4)
  const bytes = bb.bytes
  bytes[offset] = value
  bytes[offset + 1] = value >> 8
  bytes[offset + 2] = value >> 16
  bytes[offset + 3] = value >> 24
}

function readInt64 (bb, unsigned) {
  return {
    low: readInt32(bb),
    high: readInt32(bb),
    unsigned
  }
}

function writeInt64 (bb, value) {
  writeInt32(bb, value.low)
  writeInt32(bb, value.high)
}

function readVarint32 (bb) {
  let c = 0
  let value = 0
  let b
  do {
    b = readByte(bb)
    if (c < 32) {
      value |= (b & 0x7f) << c
    }
    c += 7
  } while (b & 0x80)
  return value
}

function writeVarint32 (bb, value) {
  value >>>= 0
  while (value >= 0x80) {
    writeByte(bb, (value & 0x7f) | 0x80)
    value >>>= 7
  }
  writeByte(bb, value)
}

function readVarint64 (bb, unsigned) {
  let part0 = 0
  let part1 = 0
  let part2 = 0
  let b

  b = readByte(bb)
  part0 = b & 0x7f
  if (b & 0x80) {
    b = readByte(bb)
    part0 |= (b & 0x7f) << 7
    if (b & 0x80) {
      b = readByte(bb)
      part0 |= (b & 0x7f) << 14
      if (b & 0x80) {
        b = readByte(bb)
        part0 |= (b & 0x7f) << 21
        if (b & 0x80) {
          b = readByte(bb)
          part1 = b & 0x7f
          if (b & 0x80) {
            b = readByte(bb)
            part1 |= (b & 0x7f) << 7
            if (b & 0x80) {
              b = readByte(bb)
              part1 |= (b & 0x7f) << 14
              if (b & 0x80) {
                b = readByte(bb)
                part1 |= (b & 0x7f) << 21
                if (b & 0x80) {
                  b = readByte(bb)
                  part2 = b & 0x7f
                  if (b & 0x80) {
                    b = readByte(bb)
                    part2 |= (b & 0x7f) << 7
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
    unsigned
  }
}

function writeVarint64 (bb, value) {
  const part0 = value.low >>> 0
  const part1 = ((value.low >>> 28) | (value.high << 4)) >>> 0
  const part2 = value.high >>> 24

  // ref: src/google/protobuf/io/coded_stream.cc
  const size =
    part2 === 0
      ? part1 === 0
        ? part0 < 1 << 14
          ? part0 < 1 << 7
            ? 1
            : 2
          : part0 < 1 << 21
            ? 3
            : 4
        : part1 < 1 << 14
          ? part1 < 1 << 7
            ? 5
            : 6
          : part1 < 1 << 21
            ? 7
            : 8
      : part2 < 1 << 7
        ? 9
        : 10

  const offset = grow(bb, size)
  const bytes = bb.bytes

  switch (size) {
    case 10:
      bytes[offset + 9] = (part2 >>> 7) & 0x01
    case 9:
      bytes[offset + 8] = size !== 9 ? part2 | 0x80 : part2 & 0x7f
    case 8:
      bytes[offset + 7] =
        size !== 8 ? (part1 >>> 21) | 0x80 : (part1 >>> 21) & 0x7f
    case 7:
      bytes[offset + 6] =
        size !== 7 ? (part1 >>> 14) | 0x80 : (part1 >>> 14) & 0x7f
    case 6:
      bytes[offset + 5] =
        size !== 6 ? (part1 >>> 7) | 0x80 : (part1 >>> 7) & 0x7f
    case 5:
      bytes[offset + 4] = size !== 5 ? part1 | 0x80 : part1 & 0x7f
    case 4:
      bytes[offset + 3] =
        size !== 4 ? (part0 >>> 21) | 0x80 : (part0 >>> 21) & 0x7f
    case 3:
      bytes[offset + 2] =
        size !== 3 ? (part0 >>> 14) | 0x80 : (part0 >>> 14) & 0x7f
    case 2:
      bytes[offset + 1] =
        size !== 2 ? (part0 >>> 7) | 0x80 : (part0 >>> 7) & 0x7f
    case 1:
      bytes[offset] = size !== 1 ? part0 | 0x80 : part0 & 0x7f
  }
}

function readVarint32ZigZag (bb) {
  const value = readVarint32(bb)

  // ref: src/google/protobuf/wire_format_lite.h
  return (value >>> 1) ^ -(value & 1)
}

function writeVarint32ZigZag (bb, value) {
  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint32(bb, (value << 1) ^ (value >> 31))
}

function readVarint64ZigZag (bb) {
  const value = readVarint64(bb, /* unsigned */ false)
  const low = value.low
  const high = value.high
  const flip = -(low & 1)

  // ref: src/google/protobuf/wire_format_lite.h
  return {
    low: ((low >>> 1) | (high << 31)) ^ flip,
    high: (high >>> 1) ^ flip,
    unsigned: false
  }
}

function writeVarint64ZigZag (bb, value) {
  const low = value.low
  const high = value.high
  const flip = high >> 31

  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint64(bb, {
    low: (low << 1) ^ flip,
    high: ((high << 1) | (low >>> 31)) ^ flip,
    unsigned: false
  })
}
