export function encodeObligationProto (message) {
  const bb = popByteBuffer()
  _encodeObligationProto(message, bb)
  return toUint8Array(bb)
}

function _encodeObligationProto (message, bb) {
  // optional string obligation_number = 1;
  const $obligation_number = message.obligation_number
  if ($obligation_number !== undefined) {
    writeVarint32(bb, 10)
    writeString(bb, $obligation_number)
  }

  // optional string project_id = 2;
  const $project_id = message.project_id
  if ($project_id !== undefined) {
    writeVarint32(bb, 18)
    writeString(bb, $project_id)
  }

  // optional string primary_environmental_mechanism_id = 3;
  const $primary_environmental_mechanism_id =
    message.primary_environmental_mechanism_id
  if ($primary_environmental_mechanism_id !== undefined) {
    writeVarint32(bb, 26)
    writeString(bb, $primary_environmental_mechanism_id)
  }

  // optional string procedure = 4;
  const $procedure = message.procedure
  if ($procedure !== undefined) {
    writeVarint32(bb, 34)
    writeString(bb, $procedure)
  }

  // optional string environmental_aspect = 5;
  const $environmental_aspect = message.environmental_aspect
  if ($environmental_aspect !== undefined) {
    writeVarint32(bb, 42)
    writeString(bb, $environmental_aspect)
  }

  // optional string custom_environmental_aspect = 6;
  const $custom_environmental_aspect = message.custom_environmental_aspect
  if ($custom_environmental_aspect !== undefined) {
    writeVarint32(bb, 50)
    writeString(bb, $custom_environmental_aspect)
  }

  // optional string obligation = 7;
  const $obligation = message.obligation
  if ($obligation !== undefined) {
    writeVarint32(bb, 58)
    writeString(bb, $obligation)
  }

  // optional string accountability = 8;
  const $accountability = message.accountability
  if ($accountability !== undefined) {
    writeVarint32(bb, 66)
    writeString(bb, $accountability)
  }

  // repeated string responsible_user_ids = 9;
  const array$responsible_user_ids = message.responsible_user_ids
  if (array$responsible_user_ids !== undefined) {
    for (const value of array$responsible_user_ids) {
      writeVarint32(bb, 74)
      writeString(bb, value)
    }
  }

  // optional string project_phase = 10;
  const $project_phase = message.project_phase
  if ($project_phase !== undefined) {
    writeVarint32(bb, 82)
    writeString(bb, $project_phase)
  }

  // optional string action_due_date = 11;
  const $action_due_date = message.action_due_date
  if ($action_due_date !== undefined) {
    writeVarint32(bb, 90)
    writeString(bb, $action_due_date)
  }

  // optional string close_out_date = 12;
  const $close_out_date = message.close_out_date
  if ($close_out_date !== undefined) {
    writeVarint32(bb, 98)
    writeString(bb, $close_out_date)
  }

  // optional string status = 13;
  const $status = message.status
  if ($status !== undefined) {
    writeVarint32(bb, 106)
    writeString(bb, $status)
  }

  // optional string supporting_information = 14;
  const $supporting_information = message.supporting_information
  if ($supporting_information !== undefined) {
    writeVarint32(bb, 114)
    writeString(bb, $supporting_information)
  }

  // optional string general_comments = 15;
  const $general_comments = message.general_comments
  if ($general_comments !== undefined) {
    writeVarint32(bb, 122)
    writeString(bb, $general_comments)
  }

  // optional string evidence_notes = 16;
  const $evidence_notes = message.evidence_notes
  if ($evidence_notes !== undefined) {
    writeVarint32(bb, 130)
    writeString(bb, $evidence_notes)
  }

  // optional bool recurring_obligation = 17;
  const $recurring_obligation = message.recurring_obligation
  if ($recurring_obligation !== undefined) {
    writeVarint32(bb, 136)
    writeByte(bb, $recurring_obligation ? 1 : 0)
  }

  // optional string recurring_frequency = 18;
  const $recurring_frequency = message.recurring_frequency
  if ($recurring_frequency !== undefined) {
    writeVarint32(bb, 146)
    writeString(bb, $recurring_frequency)
  }

  // optional string recurring_status = 19;
  const $recurring_status = message.recurring_status
  if ($recurring_status !== undefined) {
    writeVarint32(bb, 154)
    writeString(bb, $recurring_status)
  }

  // optional string recurring_forecasted_date = 20;
  const $recurring_forecasted_date = message.recurring_forecasted_date
  if ($recurring_forecasted_date !== undefined) {
    writeVarint32(bb, 162)
    writeString(bb, $recurring_forecasted_date)
  }

  // optional bool inspection = 21;
  const $inspection = message.inspection
  if ($inspection !== undefined) {
    writeVarint32(bb, 168)
    writeByte(bb, $inspection ? 1 : 0)
  }

  // optional string inspection_frequency = 22;
  const $inspection_frequency = message.inspection_frequency
  if ($inspection_frequency !== undefined) {
    writeVarint32(bb, 178)
    writeString(bb, $inspection_frequency)
  }

  // optional string site_or_desktop = 23;
  const $site_or_desktop = message.site_or_desktop
  if ($site_or_desktop !== undefined) {
    writeVarint32(bb, 186)
    writeString(bb, $site_or_desktop)
  }

  // optional bool new_control_action_required = 24;
  const $new_control_action_required = message.new_control_action_required
  if ($new_control_action_required !== undefined) {
    writeVarint32(bb, 192)
    writeByte(bb, $new_control_action_required ? 1 : 0)
  }

  // optional string obligation_type = 25;
  const $obligation_type = message.obligation_type
  if ($obligation_type !== undefined) {
    writeVarint32(bb, 202)
    writeString(bb, $obligation_type)
  }

  // optional bool gap_analysis = 26;
  const $gap_analysis = message.gap_analysis
  if ($gap_analysis !== undefined) {
    writeVarint32(bb, 208)
    writeByte(bb, $gap_analysis ? 1 : 0)
  }

  // optional string notes_for_gap_analysis = 27;
  const $notes_for_gap_analysis = message.notes_for_gap_analysis
  if ($notes_for_gap_analysis !== undefined) {
    writeVarint32(bb, 218)
    writeString(bb, $notes_for_gap_analysis)
  }

  // optional string created_at = 28;
  const $created_at = message.created_at
  if ($created_at !== undefined) {
    writeVarint32(bb, 226)
    writeString(bb, $created_at)
  }

  // optional string updated_at = 29;
  const $updated_at = message.updated_at
  if ($updated_at !== undefined) {
    writeVarint32(bb, 234)
    writeString(bb, $updated_at)
  }
}

export function decodeObligationProto (binary) {
  return _decodeObligationProto(wrapByteBuffer(binary))
}

function _decodeObligationProto (bb) {
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

      // optional string project_id = 2;
      case 2: {
        message.project_id = readString(bb, readVarint32(bb))
        break
      }

      // optional string primary_environmental_mechanism_id = 3;
      case 3: {
        message.primary_environmental_mechanism_id = readString(
          bb,
          readVarint32(bb)
        )
        break
      }

      // optional string procedure = 4;
      case 4: {
        message.procedure = readString(bb, readVarint32(bb))
        break
      }

      // optional string environmental_aspect = 5;
      case 5: {
        message.environmental_aspect = readString(bb, readVarint32(bb))
        break
      }

      // optional string custom_environmental_aspect = 6;
      case 6: {
        message.custom_environmental_aspect = readString(bb, readVarint32(bb))
        break
      }

      // optional string obligation = 7;
      case 7: {
        message.obligation = readString(bb, readVarint32(bb))
        break
      }

      // optional string accountability = 8;
      case 8: {
        message.accountability = readString(bb, readVarint32(bb))
        break
      }

      // repeated string responsible_user_ids = 9;
      case 9: {
        const values =
          message.responsible_user_ids || (message.responsible_user_ids = [])
        values.push(readString(bb, readVarint32(bb)))
        break
      }

      // optional string project_phase = 10;
      case 10: {
        message.project_phase = readString(bb, readVarint32(bb))
        break
      }

      // optional string action_due_date = 11;
      case 11: {
        message.action_due_date = readString(bb, readVarint32(bb))
        break
      }

      // optional string close_out_date = 12;
      case 12: {
        message.close_out_date = readString(bb, readVarint32(bb))
        break
      }

      // optional string status = 13;
      case 13: {
        message.status = readString(bb, readVarint32(bb))
        break
      }

      // optional string supporting_information = 14;
      case 14: {
        message.supporting_information = readString(bb, readVarint32(bb))
        break
      }

      // optional string general_comments = 15;
      case 15: {
        message.general_comments = readString(bb, readVarint32(bb))
        break
      }

      // optional string evidence_notes = 16;
      case 16: {
        message.evidence_notes = readString(bb, readVarint32(bb))
        break
      }

      // optional bool recurring_obligation = 17;
      case 17: {
        message.recurring_obligation = !!readByte(bb)
        break
      }

      // optional string recurring_frequency = 18;
      case 18: {
        message.recurring_frequency = readString(bb, readVarint32(bb))
        break
      }

      // optional string recurring_status = 19;
      case 19: {
        message.recurring_status = readString(bb, readVarint32(bb))
        break
      }

      // optional string recurring_forecasted_date = 20;
      case 20: {
        message.recurring_forecasted_date = readString(bb, readVarint32(bb))
        break
      }

      // optional bool inspection = 21;
      case 21: {
        message.inspection = !!readByte(bb)
        break
      }

      // optional string inspection_frequency = 22;
      case 22: {
        message.inspection_frequency = readString(bb, readVarint32(bb))
        break
      }

      // optional string site_or_desktop = 23;
      case 23: {
        message.site_or_desktop = readString(bb, readVarint32(bb))
        break
      }

      // optional bool new_control_action_required = 24;
      case 24: {
        message.new_control_action_required = !!readByte(bb)
        break
      }

      // optional string obligation_type = 25;
      case 25: {
        message.obligation_type = readString(bb, readVarint32(bb))
        break
      }

      // optional bool gap_analysis = 26;
      case 26: {
        message.gap_analysis = !!readByte(bb)
        break
      }

      // optional string notes_for_gap_analysis = 27;
      case 27: {
        message.notes_for_gap_analysis = readString(bb, readVarint32(bb))
        break
      }

      // optional string created_at = 28;
      case 28: {
        message.created_at = readString(bb, readVarint32(bb))
        break
      }

      // optional string updated_at = 29;
      case 29: {
        message.updated_at = readString(bb, readVarint32(bb))
        break
      }

      default:
        skipUnknownField(bb, tag & 7)
    }
  }

  return message
}

export function encodeObligationCollection (message) {
  const bb = popByteBuffer()
  _encodeObligationCollection(message, bb)
  return toUint8Array(bb)
}

function _encodeObligationCollection (message, bb) {
  // repeated ObligationProto obligations = 1;
  const array$obligations = message.obligations
  if (array$obligations !== undefined) {
    for (const value of array$obligations) {
      writeVarint32(bb, 10)
      const nested = popByteBuffer()
      _encodeObligationProto(value, nested)
      writeVarint32(bb, nested.limit)
      writeByteBuffer(bb, nested)
      pushByteBuffer(nested)
    }
  }
}

export function decodeObligationCollection (binary) {
  return _decodeObligationCollection(wrapByteBuffer(binary))
}

function _decodeObligationCollection (bb) {
  const message = {}

  end_of_message: while (!isAtEnd(bb)) {
    const tag = readVarint32(bb)

    switch (tag >>> 3) {
      case 0:
        break end_of_message

      // repeated ObligationProto obligations = 1;
      case 1: {
        const limit = pushTemporaryLength(bb)
        const values = message.obligations || (message.obligations = [])
        values.push(_decodeObligationProto(bb))
        bb.limit = limit
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
