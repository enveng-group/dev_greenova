export const encodeObligationStatus = {
  STATUS_UNKNOWN: 0,
  STATUS_NOT_STARTED: 1,
  STATUS_IN_PROGRESS: 2,
  STATUS_COMPLETED: 3,
  STATUS_OVERDUE: 4
}

export const decodeObligationStatus = {
  0: 'STATUS_UNKNOWN',
  1: 'STATUS_NOT_STARTED',
  2: 'STATUS_IN_PROGRESS',
  3: 'STATUS_COMPLETED',
  4: 'STATUS_OVERDUE'
}

export function encodeObligationInsight (message) {
  const bb = popByteBuffer()
  _encodeObligationInsight(message, bb)
  return toUint8Array(bb)
}

function _encodeObligationInsight (message, bb) {
  // optional string obligation_number = 1;
  const $obligation_number = message.obligation_number
  if ($obligation_number !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $obligation_number)
  }

  // optional string due_date = 2;
  const $due_date = message.due_date
  if ($due_date !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $due_date)
  }

  // optional string close_out_date = 3;
  const $close_out_date = message.close_out_date
  if ($close_out_date !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $close_out_date)
  }
}

export function decodeObligationInsight (binary) {
  return _decodeObligationInsight(wrapByteBuffer(binary))
}

function _decodeObligationInsight (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional string obligation_number = 1;
      case 1: {
        message.obligation_number = readString(bb, readVarint32(bb))
        break
      }

      // optional string due_date = 2;
      case 2: {
        message.due_date = readString(bb, readVarint32(bb))
        break
      }

      // optional string close_out_date = 3;
      case 3: {
        message.close_out_date = readString(bb, readVarint32(bb))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeObligationInsightResponse (message) {
  const bb = popByteBuffer()
  _encodeObligationInsightResponse(message, bb)
  return toUint8Array(bb)
}

function _encodeObligationInsightResponse (message, bb) {
  // optional int32 mechanism_id = 1;
  const $mechanism_id = message.mechanism_id
  if ($mechanism_id !== undefined) {
    writeVarint32(bb, 8)
    writeVarint64(bb, intToLong($mechanism_id))
  }

  // optional string status = 2;
  const $status = message.status
  if ($status !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $status)
  }

  // optional string status_key = 3;
  const $status_key = message.status_key
  if ($status_key !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $status_key)
  }

  // optional int32 count = 4;
  const $count = message.count
  if ($count !== undefined) {
    writeVarint32(bb, 32)
    writeVarint64(bb, intToLong($count))
  }

  // optional int32 total_count = 5;
  const $total_count = message.total_count
  if ($total_count !== undefined) {
    writeVarint32(bb, 40)
    writeVarint64(bb, intToLong($total_count))
  }

  // repeated ObligationInsight obligations = 6;
  const array$obligations = message.obligations
  if (array$obligations !== undefined) {
    for (const value of array$obligations) {
      writeVarint32(bb, 50)
      const nested = popByteBuffer()
      _encodeObligationInsight(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }

  // optional string error = 7;
  const $error = message.error
  if ($error !== undefined) {
    writeVarint32(bb, 58)
    writeString(bb, $error)
  }
}

export function decodeObligationInsightResponse (binary) {
  return _decodeObligationInsightResponse(wrapByteBuffer(binary))
}

function _decodeObligationInsightResponse (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // optional int32 mechanism_id = 1;
      case 1: {
        message.mechanism_id = readVarint32(bb)
        break
      }

      // optional string status = 2;
      case 2: {
        message.status = readString(bb, readVarint32(bb))
        break
      }

      // optional string status_key = 3;
      case 3: {
        message.status_key = readString(bb, readVarint32(bb))
        break
      }

      // optional int32 count = 4;
      case 4: {
        message.count = readVarint32(bb)
        break
      }

      // optional int32 total_count = 5;
      case 5: {
        message.total_count = readVarint32(bb)
        break
      }

      // repeated ObligationInsight obligations = 6;
      case 6: {
        const limit = pushTemporaryLength(bb)
        const values = message.obligations || (message.obligations = [])
        values.push(_decodeObligationInsight(bb))
        bb.limit = limit
        break
      }

      // optional string error = 7;
      case 7: {
        message.error = readString(bb, readVarint32(bb))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeChartSegment (message) {
  const bb = popByteBuffer()
  _encodeChartSegment(message, bb)
  return toUint8Array(bb)
}

function _encodeChartSegment (message, bb) {
  // optional string label = 1;
  const $label = message.label
  if ($label !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $label)
  }

  // optional int32 value = 2;
  const $value = message.value
  if ($value !== undefined) {
    writeVarint32(bb, 16)
    writeVarint64(bb, intToLong($value))
  }

  // optional string color = 3;
  const $color = message.color
  if ($color !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $color)
  }
}

export function decodeChartSegment (binary) {
  return _decodeChartSegment(wrapByteBuffer(binary))
}

function _decodeChartSegment (bb) {
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

      // optional int32 value = 2;
      case 2: {
        message.value = readVarint32(bb)
        break
      }

      // optional string color = 3;
      case 3: {
        message.color = readString(bb, readVarint32(bb))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeChartData (message) {
  const bb = popByteBuffer()
  _encodeChartData(message, bb)
  return toUint8Array(bb)
}

function _encodeChartData (message, bb) {
  // repeated ChartSegment segments = 1;
  const array$segments = message.segments
  if (array$segments !== undefined) {
    for (const value of array$segments) {
      writeVarint32(bb, 10)
      const nested = popByteBuffer()
      _encodeChartSegment(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }

  // optional int32 mechanism_id = 2;
  const $mechanism_id = message.mechanism_id
  if ($mechanism_id !== undefined) {
    writeVarint32(bb, 16)
    writeVarint64(bb, intToLong($mechanism_id))
  }

  // optional string mechanism_name = 3;
  const $mechanism_name = message.mechanism_name
  if ($mechanism_name !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $mechanism_name)
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

      // repeated ChartSegment segments = 1;
      case 1: {
        const limit = pushTemporaryLength(bb)
        const values = message.segments || (message.segments = [])
        values.push(_decodeChartSegment(bb))
        bb.limit = limit
        break
      }

      // optional int32 mechanism_id = 2;
      case 2: {
        message.mechanism_id = readVarint32(bb)
        break
      }

      // optional string mechanism_name = 3;
      case 3: {
        message.mechanism_name = readString(bb, readVarint32(bb))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeChartResponse (message) {
  const bb = popByteBuffer()
  _encodeChartResponse(message, bb)
  return toUint8Array(bb)
}

function _encodeChartResponse (message, bb) {
  // repeated ChartData charts = 1;
  const array$charts = message.charts
  if (array$charts !== undefined) {
    for (const value of array$charts) {
      writeVarint32(bb, 10)
      const nested = popByteBuffer()
      _encodeChartData(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }

  // optional string error = 2;
  const $error = message.error
  if ($error !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $error)
  }
}

export function decodeChartResponse (binary) {
  return _decodeChartResponse(wrapByteBuffer(binary))
}

function _decodeChartResponse (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // repeated ChartData charts = 1;
      case 1: {
        const limit = pushTemporaryLength(bb)
        const values = message.charts || (message.charts = [])
        values.push(_decodeChartData(bb))
        bb.limit = limit
        break
      }

      // optional string error = 2;
      case 2: {
        message.error = readString(bb, readVarint32(bb))
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
