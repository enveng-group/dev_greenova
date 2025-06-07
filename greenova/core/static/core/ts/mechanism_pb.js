/* eslint-disable no-prototype-builtins */
'use strict'

const $protobuf = require('protobufjs/minimal')

// Common aliases
const $Reader = $protobuf.Reader
const $Writer = $protobuf.Writer
const $util = $protobuf.util

// Exported root namespace
const $root = $protobuf.roots.default || ($protobuf.roots.default = {})

$root.greenova = (function () {
  /**
   * Namespace greenova.
   * @exports greenova
   * @namespace
   */
  const greenova = {}

  greenova.mechanisms = (function () {
    /**
     * Namespace mechanisms.
     * @memberof greenova
     * @namespace
     */
    const mechanisms = {}

    /**
     * ObligationStatus enum.
     * @name greenova.mechanisms.ObligationStatus
     * @enum {number}
     * @property {number} STATUS_UNKNOWN=0 STATUS_UNKNOWN value
     * @property {number} STATUS_NOT_STARTED=1 STATUS_NOT_STARTED value
     * @property {number} STATUS_IN_PROGRESS=2 STATUS_IN_PROGRESS value
     * @property {number} STATUS_COMPLETED=3 STATUS_COMPLETED value
     * @property {number} STATUS_OVERDUE=4 STATUS_OVERDUE value
     */
    mechanisms.ObligationStatus = (function () {
      const valuesById = {}
      const values = Object.create(valuesById)
      values[(valuesById[0] = 'STATUS_UNKNOWN')] = 0
      values[(valuesById[1] = 'STATUS_NOT_STARTED')] = 1
      values[(valuesById[2] = 'STATUS_IN_PROGRESS')] = 2
      values[(valuesById[3] = 'STATUS_COMPLETED')] = 3
      values[(valuesById[4] = 'STATUS_OVERDUE')] = 4
      return values
    })()

    mechanisms.ObligationInsight = (function () {
      /**
       * Properties of an ObligationInsight.
       * @memberof greenova.mechanisms
       * @interface IObligationInsight
       * @property {string|null} [obligationNumber] ObligationInsight obligationNumber
       * @property {string|null} [dueDate] ObligationInsight dueDate
       * @property {string|null} [closeOutDate] ObligationInsight closeOutDate
       */

      /**
       * Constructs a new ObligationInsight.
       * @memberof greenova.mechanisms
       * @classdesc Represents an ObligationInsight.
       * @implements IObligationInsight
       * @constructor
       * @param {greenova.mechanisms.IObligationInsight=} [properties] Properties to set
       */
      function ObligationInsight (properties) {
        if (properties) {
          for (
            let keys = Object.keys(properties), i = 0;
            i < keys.length;
            i += 1
          ) {
            if (properties[keys[i]] != null) {
              this[keys[i]] = properties[keys[i]]
            }
          }
        }
      }

      /**
       * ObligationInsight obligationNumber.
       * @member {string} obligationNumber
       * @memberof greenova.mechanisms.ObligationInsight
       * @instance
       */
      ObligationInsight.prototype.obligationNumber = ''

      /**
       * ObligationInsight dueDate.
       * @member {string} dueDate
       * @memberof greenova.mechanisms.ObligationInsight
       * @instance
       */
      ObligationInsight.prototype.dueDate = ''

      /**
       * ObligationInsight closeOutDate.
       * @member {string} closeOutDate
       * @memberof greenova.mechanisms.ObligationInsight
       * @instance
       */
      ObligationInsight.prototype.closeOutDate = ''

      /**
       * Creates a new ObligationInsight instance using the specified properties.
       * @function create
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {greenova.mechanisms.IObligationInsight=} [properties] Properties to set
       * @returns {greenova.mechanisms.ObligationInsight} ObligationInsight instance
       */
      ObligationInsight.create = function create (properties) {
        return new ObligationInsight(properties)
      }

      /**
       * Encodes the specified ObligationInsight message. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
       * @function encode
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {greenova.mechanisms.IObligationInsight} message ObligationInsight message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ObligationInsight.encode = function encode (message, writer) {
        if (!writer) {
          writer = $Writer.create()
        }
        if (
          message.obligationNumber != null &&
          Object.hasOwnProperty.call(message, 'obligationNumber')
        ) {
          writer
            .uint32(/* id 1, wireType 2 = */ 10)
            .string(message.obligationNumber)
        }
        if (
          message.dueDate != null &&
          Object.hasOwnProperty.call(message, 'dueDate')
        ) {
          writer.uint32(/* id 2, wireType 2 = */ 18).string(message.dueDate)
        }
        if (
          message.closeOutDate != null &&
          Object.hasOwnProperty.call(message, 'closeOutDate')
        ) {
          writer
            .uint32(/* id 3, wireType 2 = */ 26)
            .string(message.closeOutDate)
        }
        return writer
      }

      /**
       * Encodes the specified ObligationInsight message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
       * @function encodeDelimited
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {greenova.mechanisms.IObligationInsight} message ObligationInsight message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ObligationInsight.encodeDelimited = function encodeDelimited (
        message,
        writer
      ) {
        return this.encode(message, writer).ldelim()
      }

      /**
       * Decodes an ObligationInsight message from the specified reader or buffer.
       * @function decode
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @param {number} [length] Message length if known beforehand
       * @returns {greenova.mechanisms.ObligationInsight} ObligationInsight
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ObligationInsight.decode = function decode (reader, length, error) {
        if (!(reader instanceof $Reader)) {
          reader = $Reader.create(reader)
        }
        const end = length === undefined ? reader.len : reader.pos + length
        const message = new $root.greenova.mechanisms.ObligationInsight()
        while (reader.pos < end) {
          const tag = reader.uint32()
          if (tag === error) {
            break
          }
          switch (tag >>> 3) {
            case 1: {
              message.obligationNumber = reader.string()
              break
            }
            case 2: {
              message.dueDate = reader.string()
              break
            }
            case 3: {
              message.closeOutDate = reader.string()
              break
            }
            default:
              reader.skipType(tag & 7)
              break
          }
        }
        return message
      }

      /**
       * Decodes an ObligationInsight message from the specified reader or buffer, length delimited.
       * @function decodeDelimited
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @returns {greenova.mechanisms.ObligationInsight} ObligationInsight
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ObligationInsight.decodeDelimited = function decodeDelimited (reader) {
        if (!(reader instanceof $Reader)) {
          reader = new $Reader(reader)
        }
        return this.decode(reader, reader.uint32())
      }

      /**
       * Verifies an ObligationInsight message.
       * @function verify
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {Object.<string,*>} message Plain object to verify
       * @returns {string|null} `null` if valid, otherwise the reason why it is not
       */
      ObligationInsight.verify = function verify (message) {
        if (typeof message !== 'object' || message === null) {
          return 'object expected'
        }
        if (
          message.obligationNumber != null &&
          message.hasOwnProperty('obligationNumber')
        ) {
          if (!$util.isString(message.obligationNumber)) {
            return 'obligationNumber: string expected'
          }
        }
        if (message.dueDate != null && message.hasOwnProperty('dueDate')) {
          if (!$util.isString(message.dueDate)) {
            return 'dueDate: string expected'
          }
        }
        if (
          message.closeOutDate != null &&
          message.hasOwnProperty('closeOutDate')
        ) {
          if (!$util.isString(message.closeOutDate)) {
            return 'closeOutDate: string expected'
          }
        }
        return null
      }

      /**
       * Creates an ObligationInsight message from a plain object. Also converts values to their respective internal types.
       * @function fromObject
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {Object.<string,*>} object Plain object
       * @returns {greenova.mechanisms.ObligationInsight} ObligationInsight
       */
      ObligationInsight.fromObject = function fromObject (object) {
        if (object instanceof $root.greenova.mechanisms.ObligationInsight) {
          return object
        }
        const message = new $root.greenova.mechanisms.ObligationInsight()
        if (object.obligationNumber != null) {
          message.obligationNumber = String(object.obligationNumber)
        }
        if (object.dueDate != null) {
          message.dueDate = String(object.dueDate)
        }
        if (object.closeOutDate != null) {
          message.closeOutDate = String(object.closeOutDate)
        }
        return message
      }

      /**
       * Creates a plain object from an ObligationInsight message. Also converts values to other types if specified.
       * @function toObject
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {greenova.mechanisms.ObligationInsight} message ObligationInsight
       * @param {$protobuf.IConversionOptions} [options] Conversion options
       * @returns {Object.<string,*>} Plain object
       */
      ObligationInsight.toObject = function toObject (message, options) {
        if (!options) {
          options = {}
        }
        const object = {}
        if (options.defaults) {
          object.obligationNumber = ''
          object.dueDate = ''
          object.closeOutDate = ''
        }
        if (
          message.obligationNumber != null &&
          message.hasOwnProperty('obligationNumber')
        ) {
          object.obligationNumber = message.obligationNumber
        }
        if (message.dueDate != null && message.hasOwnProperty('dueDate')) {
          object.dueDate = message.dueDate
        }
        if (
          message.closeOutDate != null &&
          message.hasOwnProperty('closeOutDate')
        ) {
          object.closeOutDate = message.closeOutDate
        }
        return object
      }

      /**
       * Converts this ObligationInsight to JSON.
       * @function toJSON
       * @memberof greenova.mechanisms.ObligationInsight
       * @instance
       * @returns {Object.<string,*>} JSON object
       */
      ObligationInsight.prototype.toJSON = function toJSON () {
        return this.constructor.toObject(this, $protobuf.util.toJSONOptions)
      }

      /**
       * Gets the default type url for ObligationInsight
       * @function getTypeUrl
       * @memberof greenova.mechanisms.ObligationInsight
       * @static
       * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
       * @returns {string} The default type url
       */
      ObligationInsight.getTypeUrl = function getTypeUrl (typeUrlPrefix) {
        if (typeUrlPrefix === undefined) {
          typeUrlPrefix = 'type.googleapis.com'
        }
        return typeUrlPrefix + '/greenova.mechanisms.ObligationInsight'
      }

      return ObligationInsight
    })()

    mechanisms.ObligationInsightResponse = (function () {
      /**
       * Properties of an ObligationInsightResponse.
       * @memberof greenova.mechanisms
       * @interface IObligationInsightResponse
       * @property {number|null} [mechanismId] ObligationInsightResponse mechanismId
       * @property {string|null} [status] ObligationInsightResponse status
       * @property {string|null} [statusKey] ObligationInsightResponse statusKey
       * @property {number|null} [count] ObligationInsightResponse count
       * @property {number|null} [totalCount] ObligationInsightResponse totalCount
       * @property {Array.<greenova.mechanisms.IObligationInsight>|null} [obligations] ObligationInsightResponse obligations
       * @property {string|null} [error] ObligationInsightResponse error
       */

      /**
       * Constructs a new ObligationInsightResponse.
       * @memberof greenova.mechanisms
       * @classdesc Represents an ObligationInsightResponse.
       * @implements IObligationInsightResponse
       * @constructor
       * @param {greenova.mechanisms.IObligationInsightResponse=} [properties] Properties to set
       */
      function ObligationInsightResponse (properties) {
        this.obligations = []
        if (properties) {
          for (
            let keys = Object.keys(properties), i = 0;
            i < keys.length;
            i += 1
          ) {
            if (properties[keys[i]] != null) {
              this[keys[i]] = properties[keys[i]]
            }
          }
        }
      }

      /**
       * ObligationInsightResponse mechanismId.
       * @member {number} mechanismId
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.mechanismId = 0

      /**
       * ObligationInsightResponse status.
       * @member {string} status
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.status = ''

      /**
       * ObligationInsightResponse statusKey.
       * @member {string} statusKey
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.statusKey = ''

      /**
       * ObligationInsightResponse count.
       * @member {number} count
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.count = 0

      /**
       * ObligationInsightResponse totalCount.
       * @member {number} totalCount
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.totalCount = 0

      /**
       * ObligationInsightResponse obligations.
       * @member {Array.<greenova.mechanisms.IObligationInsight>} obligations
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.obligations = $util.emptyArray

      /**
       * ObligationInsightResponse error.
       * @member {string} error
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       */
      ObligationInsightResponse.prototype.error = ''

      /**
       * Creates a new ObligationInsightResponse instance using the specified properties.
       * @function create
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {greenova.mechanisms.IObligationInsightResponse=} [properties] Properties to set
       * @returns {greenova.mechanisms.ObligationInsightResponse} ObligationInsightResponse instance
       */
      ObligationInsightResponse.create = function create (properties) {
        return new ObligationInsightResponse(properties)
      }

      /**
       * Encodes the specified ObligationInsightResponse message. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
       * @function encode
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {greenova.mechanisms.IObligationInsightResponse} message ObligationInsightResponse message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ObligationInsightResponse.encode = function encode (message, writer) {
        if (!writer) {
          writer = $Writer.create()
        }
        if (
          message.mechanismId != null &&
          Object.hasOwnProperty.call(message, 'mechanismId')
        ) {
          writer.uint32(/* id 1, wireType 0 = */ 8).int32(message.mechanismId)
        }
        if (
          message.status != null &&
          Object.hasOwnProperty.call(message, 'status')
        ) {
          writer.uint32(/* id 2, wireType 2 = */ 18).string(message.status)
        }
        if (
          message.statusKey != null &&
          Object.hasOwnProperty.call(message, 'statusKey')
        ) {
          writer.uint32(/* id 3, wireType 2 = */ 26).string(message.statusKey)
        }
        if (
          message.count != null &&
          Object.hasOwnProperty.call(message, 'count')
        ) {
          writer.uint32(/* id 4, wireType 0 = */ 32).int32(message.count)
        }
        if (
          message.totalCount != null &&
          Object.hasOwnProperty.call(message, 'totalCount')
        ) {
          writer.uint32(/* id 5, wireType 0 = */ 40).int32(message.totalCount)
        }
        if (message.obligations != null && message.obligations.length) {
          for (let i = 0; i < message.obligations.length; i += 1) {
            $root.greenova.mechanisms.ObligationInsight.encode(
              message.obligations[i],
              writer.uint32(/* id 6, wireType 2 = */ 50).fork()
            ).ldelim()
          }
        }
        if (
          message.error != null &&
          Object.hasOwnProperty.call(message, 'error')
        ) {
          writer.uint32(/* id 7, wireType 2 = */ 58).string(message.error)
        }
        return writer
      }

      /**
       * Encodes the specified ObligationInsightResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
       * @function encodeDelimited
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {greenova.mechanisms.IObligationInsightResponse} message ObligationInsightResponse message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ObligationInsightResponse.encodeDelimited = function encodeDelimited (
        message,
        writer
      ) {
        return this.encode(message, writer).ldelim()
      }

      /**
       * Decodes an ObligationInsightResponse message from the specified reader or buffer.
       * @function decode
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @param {number} [length] Message length if known beforehand
       * @returns {greenova.mechanisms.ObligationInsightResponse} ObligationInsightResponse
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ObligationInsightResponse.decode = function decode (
        reader,
        length,
        error
      ) {
        if (!(reader instanceof $Reader)) {
          reader = $Reader.create(reader)
        }
        const end = length === undefined ? reader.len : reader.pos + length
        const message =
          new $root.greenova.mechanisms.ObligationInsightResponse()
        while (reader.pos < end) {
          const tag = reader.uint32()
          if (tag === error) {
            break
          }
          switch (tag >>> 3) {
            case 1: {
              message.mechanismId = reader.int32()
              break
            }
            case 2: {
              message.status = reader.string()
              break
            }
            case 3: {
              message.statusKey = reader.string()
              break
            }
            case 4: {
              message.count = reader.int32()
              break
            }
            case 5: {
              message.totalCount = reader.int32()
              break
            }
            case 6: {
              if (!(message.obligations && message.obligations.length)) {
                message.obligations = []
              }
              message.obligations.push(
                $root.greenova.mechanisms.ObligationInsight.decode(
                  reader,
                  reader.uint32()
                )
              )
              break
            }
            case 7: {
              message.error = reader.string()
              break
            }
            default:
              reader.skipType(tag & 7)
              break
          }
        }
        return message
      }

      /**
       * Decodes an ObligationInsightResponse message from the specified reader or buffer, length delimited.
       * @function decodeDelimited
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @returns {greenova.mechanisms.ObligationInsightResponse} ObligationInsightResponse
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ObligationInsightResponse.decodeDelimited = function decodeDelimited (
        reader
      ) {
        if (!(reader instanceof $Reader)) {
          reader = new $Reader(reader)
        }
        return this.decode(reader, reader.uint32())
      }

      /**
       * Verifies an ObligationInsightResponse message.
       * @function verify
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {Object.<string,*>} message Plain object to verify
       * @returns {string|null} `null` if valid, otherwise the reason why it is not
       */
      ObligationInsightResponse.verify = function verify (message) {
        if (typeof message !== 'object' || message === null) {
          return 'object expected'
        }
        if (
          message.mechanismId != null &&
          message.hasOwnProperty('mechanismId')
        ) {
          if (!$util.isInteger(message.mechanismId)) {
            return 'mechanismId: integer expected'
          }
        }
        if (message.status != null && message.hasOwnProperty('status')) {
          if (!$util.isString(message.status)) {
            return 'status: string expected'
          }
        }
        if (message.statusKey != null && message.hasOwnProperty('statusKey')) {
          if (!$util.isString(message.statusKey)) {
            return 'statusKey: string expected'
          }
        }
        if (message.count != null && message.hasOwnProperty('count')) {
          if (!$util.isInteger(message.count)) {
            return 'count: integer expected'
          }
        }
        if (
          message.totalCount != null &&
          message.hasOwnProperty('totalCount')
        ) {
          if (!$util.isInteger(message.totalCount)) {
            return 'totalCount: integer expected'
          }
        }
        if (
          message.obligations != null &&
          message.hasOwnProperty('obligations')
        ) {
          if (!Array.isArray(message.obligations)) {
            return 'obligations: array expected'
          }
          for (let i = 0; i < message.obligations.length; i += 1) {
            const error = $root.greenova.mechanisms.ObligationInsight.verify(
              message.obligations[i]
            )
            if (error) {
              return 'obligations.' + error
            }
          }
        }
        if (message.error != null && message.hasOwnProperty('error')) {
          if (!$util.isString(message.error)) {
            return 'error: string expected'
          }
        }
        return null
      }

      /**
       * Creates an ObligationInsightResponse message from a plain object. Also converts values to their respective internal types.
       * @function fromObject
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {Object.<string,*>} object Plain object
       * @returns {greenova.mechanisms.ObligationInsightResponse} ObligationInsightResponse
       */
      ObligationInsightResponse.fromObject = function fromObject (object) {
        if (
          object instanceof $root.greenova.mechanisms.ObligationInsightResponse
        ) {
          return object
        }
        const message =
          new $root.greenova.mechanisms.ObligationInsightResponse()
        if (object.mechanismId != null) {
          message.mechanismId = object.mechanismId | 0
        }
        if (object.status != null) {
          message.status = String(object.status)
        }
        if (object.statusKey != null) {
          message.statusKey = String(object.statusKey)
        }
        if (object.count != null) {
          message.count = object.count | 0
        }
        if (object.totalCount != null) {
          message.totalCount = object.totalCount | 0
        }
        if (object.obligations) {
          if (!Array.isArray(object.obligations)) {
            throw TypeError(
              '.greenova.mechanisms.ObligationInsightResponse.obligations: array expected'
            )
          }
          message.obligations = []
          for (let i = 0; i < object.obligations.length; i += 1) {
            if (typeof object.obligations[i] !== 'object') {
              throw TypeError(
                '.greenova.mechanisms.ObligationInsightResponse.obligations: object expected'
              )
            }
            message.obligations[i] =
              $root.greenova.mechanisms.ObligationInsight.fromObject(
                object.obligations[i]
              )
          }
        }
        if (object.error != null) {
          message.error = String(object.error)
        }
        return message
      }

      /**
       * Creates a plain object from an ObligationInsightResponse message. Also converts values to other types if specified.
       * @function toObject
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {greenova.mechanisms.ObligationInsightResponse} message ObligationInsightResponse
       * @param {$protobuf.IConversionOptions} [options] Conversion options
       * @returns {Object.<string,*>} Plain object
       */
      ObligationInsightResponse.toObject = function toObject (message, options) {
        if (!options) {
          options = {}
        }
        const object = {}
        if (options.arrays || options.defaults) {
          object.obligations = []
        }
        if (options.defaults) {
          object.mechanismId = 0
          object.status = ''
          object.statusKey = ''
          object.count = 0
          object.totalCount = 0
          object.error = ''
        }
        if (
          message.mechanismId != null &&
          message.hasOwnProperty('mechanismId')
        ) {
          object.mechanismId = message.mechanismId
        }
        if (message.status != null && message.hasOwnProperty('status')) {
          object.status = message.status
        }
        if (message.statusKey != null && message.hasOwnProperty('statusKey')) {
          object.statusKey = message.statusKey
        }
        if (message.count != null && message.hasOwnProperty('count')) {
          object.count = message.count
        }
        if (
          message.totalCount != null &&
          message.hasOwnProperty('totalCount')
        ) {
          object.totalCount = message.totalCount
        }
        if (message.obligations && message.obligations.length) {
          object.obligations = []
          for (let j = 0; j < message.obligations.length; j += 1) {
            object.obligations[j] =
              $root.greenova.mechanisms.ObligationInsight.toObject(
                message.obligations[j],
                options
              )
          }
        }
        if (message.error != null && message.hasOwnProperty('error')) {
          object.error = message.error
        }
        return object
      }

      /**
       * Converts this ObligationInsightResponse to JSON.
       * @function toJSON
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @instance
       * @returns {Object.<string,*>} JSON object
       */
      ObligationInsightResponse.prototype.toJSON = function toJSON () {
        return this.constructor.toObject(this, $protobuf.util.toJSONOptions)
      }

      /**
       * Gets the default type url for ObligationInsightResponse
       * @function getTypeUrl
       * @memberof greenova.mechanisms.ObligationInsightResponse
       * @static
       * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
       * @returns {string} The default type url
       */
      ObligationInsightResponse.getTypeUrl = function getTypeUrl (
        typeUrlPrefix
      ) {
        if (typeUrlPrefix === undefined) {
          typeUrlPrefix = 'type.googleapis.com'
        }
        return typeUrlPrefix + '/greenova.mechanisms.ObligationInsightResponse'
      }

      return ObligationInsightResponse
    })()

    mechanisms.ChartSegment = (function () {
      /**
       * Properties of a ChartSegment.
       * @memberof greenova.mechanisms
       * @interface IChartSegment
       * @property {string|null} [label] ChartSegment label
       * @property {number|null} [value] ChartSegment value
       * @property {string|null} [color] ChartSegment color
       */

      /**
       * Constructs a new ChartSegment.
       * @memberof greenova.mechanisms
       * @classdesc Represents a ChartSegment.
       * @implements IChartSegment
       * @constructor
       * @param {greenova.mechanisms.IChartSegment=} [properties] Properties to set
       */
      function ChartSegment (properties) {
        if (properties) {
          for (
            let keys = Object.keys(properties), i = 0;
            i < keys.length;
            i += 1
          ) {
            if (properties[keys[i]] != null) {
              this[keys[i]] = properties[keys[i]]
            }
          }
        }
      }

      /**
       * ChartSegment label.
       * @member {string} label
       * @memberof greenova.mechanisms.ChartSegment
       * @instance
       */
      ChartSegment.prototype.label = ''

      /**
       * ChartSegment value.
       * @member {number} value
       * @memberof greenova.mechanisms.ChartSegment
       * @instance
       */
      ChartSegment.prototype.value = 0

      /**
       * ChartSegment color.
       * @member {string} color
       * @memberof greenova.mechanisms.ChartSegment
       * @instance
       */
      ChartSegment.prototype.color = ''

      /**
       * Creates a new ChartSegment instance using the specified properties.
       * @function create
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {greenova.mechanisms.IChartSegment=} [properties] Properties to set
       * @returns {greenova.mechanisms.ChartSegment} ChartSegment instance
       */
      ChartSegment.create = function create (properties) {
        return new ChartSegment(properties)
      }

      /**
       * Encodes the specified ChartSegment message. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
       * @function encode
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {greenova.mechanisms.IChartSegment} message ChartSegment message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ChartSegment.encode = function encode (message, writer) {
        if (!writer) {
          writer = $Writer.create()
        }
        if (
          message.label != null &&
          Object.hasOwnProperty.call(message, 'label')
        ) {
          writer.uint32(/* id 1, wireType 2 = */ 10).string(message.label)
        }
        if (
          message.value != null &&
          Object.hasOwnProperty.call(message, 'value')
        ) {
          writer.uint32(/* id 2, wireType 0 = */ 16).int32(message.value)
        }
        if (
          message.color != null &&
          Object.hasOwnProperty.call(message, 'color')
        ) {
          writer.uint32(/* id 3, wireType 2 = */ 26).string(message.color)
        }
        return writer
      }

      /**
       * Encodes the specified ChartSegment message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
       * @function encodeDelimited
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {greenova.mechanisms.IChartSegment} message ChartSegment message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ChartSegment.encodeDelimited = function encodeDelimited (message, writer) {
        return this.encode(message, writer).ldelim()
      }

      /**
       * Decodes a ChartSegment message from the specified reader or buffer.
       * @function decode
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @param {number} [length] Message length if known beforehand
       * @returns {greenova.mechanisms.ChartSegment} ChartSegment
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ChartSegment.decode = function decode (reader, length, error) {
        if (!(reader instanceof $Reader)) {
          reader = $Reader.create(reader)
        }
        const end = length === undefined ? reader.len : reader.pos + length
        const message = new $root.greenova.mechanisms.ChartSegment()
        while (reader.pos < end) {
          const tag = reader.uint32()
          if (tag === error) {
            break
          }
          switch (tag >>> 3) {
            case 1: {
              message.label = reader.string()
              break
            }
            case 2: {
              message.value = reader.int32()
              break
            }
            case 3: {
              message.color = reader.string()
              break
            }
            default:
              reader.skipType(tag & 7)
              break
          }
        }
        return message
      }

      /**
       * Decodes a ChartSegment message from the specified reader or buffer, length delimited.
       * @function decodeDelimited
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @returns {greenova.mechanisms.ChartSegment} ChartSegment
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ChartSegment.decodeDelimited = function decodeDelimited (reader) {
        if (!(reader instanceof $Reader)) {
          reader = new $Reader(reader)
        }
        return this.decode(reader, reader.uint32())
      }

      /**
       * Verifies a ChartSegment message.
       * @function verify
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {Object.<string,*>} message Plain object to verify
       * @returns {string|null} `null` if valid, otherwise the reason why it is not
       */
      ChartSegment.verify = function verify (message) {
        if (typeof message !== 'object' || message === null) {
          return 'object expected'
        }
        if (message.label != null && message.hasOwnProperty('label')) {
          if (!$util.isString(message.label)) {
            return 'label: string expected'
          }
        }
        if (message.value != null && message.hasOwnProperty('value')) {
          if (!$util.isInteger(message.value)) {
            return 'value: integer expected'
          }
        }
        if (message.color != null && message.hasOwnProperty('color')) {
          if (!$util.isString(message.color)) {
            return 'color: string expected'
          }
        }
        return null
      }

      /**
       * Creates a ChartSegment message from a plain object. Also converts values to their respective internal types.
       * @function fromObject
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {Object.<string,*>} object Plain object
       * @returns {greenova.mechanisms.ChartSegment} ChartSegment
       */
      ChartSegment.fromObject = function fromObject (object) {
        if (object instanceof $root.greenova.mechanisms.ChartSegment) {
          return object
        }
        const message = new $root.greenova.mechanisms.ChartSegment()
        if (object.label != null) {
          message.label = String(object.label)
        }
        if (object.value != null) {
          message.value = object.value | 0
        }
        if (object.color != null) {
          message.color = String(object.color)
        }
        return message
      }

      /**
       * Creates a plain object from a ChartSegment message. Also converts values to other types if specified.
       * @function toObject
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {greenova.mechanisms.ChartSegment} message ChartSegment
       * @param {$protobuf.IConversionOptions} [options] Conversion options
       * @returns {Object.<string,*>} Plain object
       */
      ChartSegment.toObject = function toObject (message, options) {
        if (!options) {
          options = {}
        }
        const object = {}
        if (options.defaults) {
          object.label = ''
          object.value = 0
          object.color = ''
        }
        if (message.label != null && message.hasOwnProperty('label')) {
          object.label = message.label
        }
        if (message.value != null && message.hasOwnProperty('value')) {
          object.value = message.value
        }
        if (message.color != null && message.hasOwnProperty('color')) {
          object.color = message.color
        }
        return object
      }

      /**
       * Converts this ChartSegment to JSON.
       * @function toJSON
       * @memberof greenova.mechanisms.ChartSegment
       * @instance
       * @returns {Object.<string,*>} JSON object
       */
      ChartSegment.prototype.toJSON = function toJSON () {
        return this.constructor.toObject(this, $protobuf.util.toJSONOptions)
      }

      /**
       * Gets the default type url for ChartSegment
       * @function getTypeUrl
       * @memberof greenova.mechanisms.ChartSegment
       * @static
       * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
       * @returns {string} The default type url
       */
      ChartSegment.getTypeUrl = function getTypeUrl (typeUrlPrefix) {
        if (typeUrlPrefix === undefined) {
          typeUrlPrefix = 'type.googleapis.com'
        }
        return typeUrlPrefix + '/greenova.mechanisms.ChartSegment'
      }

      return ChartSegment
    })()

    mechanisms.ChartData = (function () {
      /**
       * Properties of a ChartData.
       * @memberof greenova.mechanisms
       * @interface IChartData
       * @property {Array.<greenova.mechanisms.IChartSegment>|null} [segments] ChartData segments
       * @property {number|null} [mechanismId] ChartData mechanismId
       * @property {string|null} [mechanismName] ChartData mechanismName
       */

      /**
       * Constructs a new ChartData.
       * @memberof greenova.mechanisms
       * @classdesc Represents a ChartData.
       * @implements IChartData
       * @constructor
       * @param {greenova.mechanisms.IChartData=} [properties] Properties to set
       */
      function ChartData (properties) {
        this.segments = []
        if (properties) {
          for (
            let keys = Object.keys(properties), i = 0;
            i < keys.length;
            i += 1
          ) {
            if (properties[keys[i]] != null) {
              this[keys[i]] = properties[keys[i]]
            }
          }
        }
      }

      /**
       * ChartData segments.
       * @member {Array.<greenova.mechanisms.IChartSegment>} segments
       * @memberof greenova.mechanisms.ChartData
       * @instance
       */
      ChartData.prototype.segments = $util.emptyArray

      /**
       * ChartData mechanismId.
       * @member {number} mechanismId
       * @memberof greenova.mechanisms.ChartData
       * @instance
       */
      ChartData.prototype.mechanismId = 0

      /**
       * ChartData mechanismName.
       * @member {string} mechanismName
       * @memberof greenova.mechanisms.ChartData
       * @instance
       */
      ChartData.prototype.mechanismName = ''

      /**
       * Creates a new ChartData instance using the specified properties.
       * @function create
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {greenova.mechanisms.IChartData=} [properties] Properties to set
       * @returns {greenova.mechanisms.ChartData} ChartData instance
       */
      ChartData.create = function create (properties) {
        return new ChartData(properties)
      }

      /**
       * Encodes the specified ChartData message. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
       * @function encode
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {greenova.mechanisms.IChartData} message ChartData message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ChartData.encode = function encode (message, writer) {
        if (!writer) {
          writer = $Writer.create()
        }
        if (message.segments != null && message.segments.length) {
          for (let i = 0; i < message.segments.length; i += 1) {
            $root.greenova.mechanisms.ChartSegment.encode(
              message.segments[i],
              writer.uint32(/* id 1, wireType 2 = */ 10).fork()
            ).ldelim()
          }
        }
        if (
          message.mechanismId != null &&
          Object.hasOwnProperty.call(message, 'mechanismId')
        ) {
          writer.uint32(/* id 2, wireType 0 = */ 16).int32(message.mechanismId)
        }
        if (
          message.mechanismName != null &&
          Object.hasOwnProperty.call(message, 'mechanismName')
        ) {
          writer
            .uint32(/* id 3, wireType 2 = */ 26)
            .string(message.mechanismName)
        }
        return writer
      }

      /**
       * Encodes the specified ChartData message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
       * @function encodeDelimited
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {greenova.mechanisms.IChartData} message ChartData message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ChartData.encodeDelimited = function encodeDelimited (message, writer) {
        return this.encode(message, writer).ldelim()
      }

      /**
       * Decodes a ChartData message from the specified reader or buffer.
       * @function decode
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @param {number} [length] Message length if known beforehand
       * @returns {greenova.mechanisms.ChartData} ChartData
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ChartData.decode = function decode (reader, length, error) {
        if (!(reader instanceof $Reader)) {
          reader = $Reader.create(reader)
        }
        const end = length === undefined ? reader.len : reader.pos + length
        const message = new $root.greenova.mechanisms.ChartData()
        while (reader.pos < end) {
          const tag = reader.uint32()
          if (tag === error) {
            break
          }
          switch (tag >>> 3) {
            case 1: {
              if (!(message.segments && message.segments.length)) {
                message.segments = []
              }
              message.segments.push(
                $root.greenova.mechanisms.ChartSegment.decode(
                  reader,
                  reader.uint32()
                )
              )
              break
            }
            case 2: {
              message.mechanismId = reader.int32()
              break
            }
            case 3: {
              message.mechanismName = reader.string()
              break
            }
            default:
              reader.skipType(tag & 7)
              break
          }
        }
        return message
      }

      /**
       * Decodes a ChartData message from the specified reader or buffer, length delimited.
       * @function decodeDelimited
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @returns {greenova.mechanisms.ChartData} ChartData
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ChartData.decodeDelimited = function decodeDelimited (reader) {
        if (!(reader instanceof $Reader)) {
          reader = new $Reader(reader)
        }
        return this.decode(reader, reader.uint32())
      }

      /**
       * Verifies a ChartData message.
       * @function verify
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {Object.<string,*>} message Plain object to verify
       * @returns {string|null} `null` if valid, otherwise the reason why it is not
       */
      ChartData.verify = function verify (message) {
        if (typeof message !== 'object' || message === null) {
          return 'object expected'
        }
        if (message.segments != null && message.hasOwnProperty('segments')) {
          if (!Array.isArray(message.segments)) {
            return 'segments: array expected'
          }
          for (let i = 0; i < message.segments.length; i += 1) {
            const error = $root.greenova.mechanisms.ChartSegment.verify(
              message.segments[i]
            )
            if (error) {
              return 'segments.' + error
            }
          }
        }
        if (
          message.mechanismId != null &&
          message.hasOwnProperty('mechanismId')
        ) {
          if (!$util.isInteger(message.mechanismId)) {
            return 'mechanismId: integer expected'
          }
        }
        if (
          message.mechanismName != null &&
          message.hasOwnProperty('mechanismName')
        ) {
          if (!$util.isString(message.mechanismName)) {
            return 'mechanismName: string expected'
          }
        }
        return null
      }

      /**
       * Creates a ChartData message from a plain object. Also converts values to their respective internal types.
       * @function fromObject
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {Object.<string,*>} object Plain object
       * @returns {greenova.mechanisms.ChartData} ChartData
       */
      ChartData.fromObject = function fromObject (object) {
        if (object instanceof $root.greenova.mechanisms.ChartData) {
          return object
        }
        const message = new $root.greenova.mechanisms.ChartData()
        if (object.segments) {
          if (!Array.isArray(object.segments)) {
            throw TypeError(
              '.greenova.mechanisms.ChartData.segments: array expected'
            )
          }
          message.segments = []
          for (let i = 0; i < object.segments.length; i += 1) {
            if (typeof object.segments[i] !== 'object') {
              throw TypeError(
                '.greenova.mechanisms.ChartData.segments: object expected'
              )
            }
            message.segments[i] =
              $root.greenova.mechanisms.ChartSegment.fromObject(
                object.segments[i]
              )
          }
        }
        if (object.mechanismId != null) {
          message.mechanismId = object.mechanismId | 0
        }
        if (object.mechanismName != null) {
          message.mechanismName = String(object.mechanismName)
        }
        return message
      }

      /**
       * Creates a plain object from a ChartData message. Also converts values to other types if specified.
       * @function toObject
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {greenova.mechanisms.ChartData} message ChartData
       * @param {$protobuf.IConversionOptions} [options] Conversion options
       * @returns {Object.<string,*>} Plain object
       */
      ChartData.toObject = function toObject (message, options) {
        if (!options) {
          options = {}
        }
        const object = {}
        if (options.arrays || options.defaults) {
          object.segments = []
        }
        if (options.defaults) {
          object.mechanismId = 0
          object.mechanismName = ''
        }
        if (message.segments && message.segments.length) {
          object.segments = []
          for (let j = 0; j < message.segments.length; j += 1) {
            object.segments[j] =
              $root.greenova.mechanisms.ChartSegment.toObject(
                message.segments[j],
                options
              )
          }
        }
        if (
          message.mechanismId != null &&
          message.hasOwnProperty('mechanismId')
        ) {
          object.mechanismId = message.mechanismId
        }
        if (
          message.mechanismName != null &&
          message.hasOwnProperty('mechanismName')
        ) {
          object.mechanismName = message.mechanismName
        }
        return object
      }

      /**
       * Converts this ChartData to JSON.
       * @function toJSON
       * @memberof greenova.mechanisms.ChartData
       * @instance
       * @returns {Object.<string,*>} JSON object
       */
      ChartData.prototype.toJSON = function toJSON () {
        return this.constructor.toObject(this, $protobuf.util.toJSONOptions)
      }

      /**
       * Gets the default type url for ChartData
       * @function getTypeUrl
       * @memberof greenova.mechanisms.ChartData
       * @static
       * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
       * @returns {string} The default type url
       */
      ChartData.getTypeUrl = function getTypeUrl (typeUrlPrefix) {
        if (typeUrlPrefix === undefined) {
          typeUrlPrefix = 'type.googleapis.com'
        }
        return typeUrlPrefix + '/greenova.mechanisms.ChartData'
      }

      return ChartData
    })()

    mechanisms.ChartResponse = (function () {
      /**
       * Properties of a ChartResponse.
       * @memberof greenova.mechanisms
       * @interface IChartResponse
       * @property {Array.<greenova.mechanisms.IChartData>|null} [charts] ChartResponse charts
       * @property {string|null} [error] ChartResponse error
       */

      /**
       * Constructs a new ChartResponse.
       * @memberof greenova.mechanisms
       * @classdesc Represents a ChartResponse.
       * @implements IChartResponse
       * @constructor
       * @param {greenova.mechanisms.IChartResponse=} [properties] Properties to set
       */
      function ChartResponse (properties) {
        this.charts = []
        if (properties) {
          for (
            let keys = Object.keys(properties), i = 0;
            i < keys.length;
            i += 1
          ) {
            if (properties[keys[i]] != null) {
              this[keys[i]] = properties[keys[i]]
            }
          }
        }
      }

      /**
       * ChartResponse charts.
       * @member {Array.<greenova.mechanisms.IChartData>} charts
       * @memberof greenova.mechanisms.ChartResponse
       * @instance
       */
      ChartResponse.prototype.charts = $util.emptyArray

      /**
       * ChartResponse error.
       * @member {string} error
       * @memberof greenova.mechanisms.ChartResponse
       * @instance
       */
      ChartResponse.prototype.error = ''

      /**
       * Creates a new ChartResponse instance using the specified properties.
       * @function create
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {greenova.mechanisms.IChartResponse=} [properties] Properties to set
       * @returns {greenova.mechanisms.ChartResponse} ChartResponse instance
       */
      ChartResponse.create = function create (properties) {
        return new ChartResponse(properties)
      }

      /**
       * Encodes the specified ChartResponse message. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
       * @function encode
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {greenova.mechanisms.IChartResponse} message ChartResponse message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ChartResponse.encode = function encode (message, writer) {
        if (!writer) {
          writer = $Writer.create()
        }
        if (message.charts != null && message.charts.length) {
          for (let i = 0; i < message.charts.length; i += 1) {
            $root.greenova.mechanisms.ChartData.encode(
              message.charts[i],
              writer.uint32(/* id 1, wireType 2 = */ 10).fork()
            ).ldelim()
          }
        }
        if (
          message.error != null &&
          Object.hasOwnProperty.call(message, 'error')
        ) {
          writer.uint32(/* id 2, wireType 2 = */ 18).string(message.error)
        }
        return writer
      }

      /**
       * Encodes the specified ChartResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
       * @function encodeDelimited
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {greenova.mechanisms.IChartResponse} message ChartResponse message or plain object to encode
       * @param {$protobuf.Writer} [writer] Writer to encode to
       * @returns {$protobuf.Writer} Writer
       */
      ChartResponse.encodeDelimited = function encodeDelimited (
        message,
        writer
      ) {
        return this.encode(message, writer).ldelim()
      }

      /**
       * Decodes a ChartResponse message from the specified reader or buffer.
       * @function decode
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @param {number} [length] Message length if known beforehand
       * @returns {greenova.mechanisms.ChartResponse} ChartResponse
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ChartResponse.decode = function decode (reader, length, error) {
        if (!(reader instanceof $Reader)) {
          reader = $Reader.create(reader)
        }
        const end = length === undefined ? reader.len : reader.pos + length
        const message = new $root.greenova.mechanisms.ChartResponse()
        while (reader.pos < end) {
          const tag = reader.uint32()
          if (tag === error) {
            break
          }
          switch (tag >>> 3) {
            case 1: {
              if (!(message.charts && message.charts.length)) {
                message.charts = []
              }
              message.charts.push(
                $root.greenova.mechanisms.ChartData.decode(
                  reader,
                  reader.uint32()
                )
              )
              break
            }
            case 2: {
              message.error = reader.string()
              break
            }
            default:
              reader.skipType(tag & 7)
              break
          }
        }
        return message
      }

      /**
       * Decodes a ChartResponse message from the specified reader or buffer, length delimited.
       * @function decodeDelimited
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
       * @returns {greenova.mechanisms.ChartResponse} ChartResponse
       * @throws {Error} If the payload is not a reader or valid buffer
       * @throws {$protobuf.util.ProtocolError} If required fields are missing
       */
      ChartResponse.decodeDelimited = function decodeDelimited (reader) {
        if (!(reader instanceof $Reader)) {
          reader = new $Reader(reader)
        }
        return this.decode(reader, reader.uint32())
      }

      /**
       * Verifies a ChartResponse message.
       * @function verify
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {Object.<string,*>} message Plain object to verify
       * @returns {string|null} `null` if valid, otherwise the reason why it is not
       */
      ChartResponse.verify = function verify (message) {
        if (typeof message !== 'object' || message === null) {
          return 'object expected'
        }
        if (message.charts != null && message.hasOwnProperty('charts')) {
          if (!Array.isArray(message.charts)) {
            return 'charts: array expected'
          }
          for (let i = 0; i < message.charts.length; i += 1) {
            const error = $root.greenova.mechanisms.ChartData.verify(
              message.charts[i]
            )
            if (error) {
              return 'charts.' + error
            }
          }
        }
        if (message.error != null && message.hasOwnProperty('error')) {
          if (!$util.isString(message.error)) {
            return 'error: string expected'
          }
        }
        return null
      }

      /**
       * Creates a ChartResponse message from a plain object. Also converts values to their respective internal types.
       * @function fromObject
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {Object.<string,*>} object Plain object
       * @returns {greenova.mechanisms.ChartResponse} ChartResponse
       */
      ChartResponse.fromObject = function fromObject (object) {
        if (object instanceof $root.greenova.mechanisms.ChartResponse) {
          return object
        }
        const message = new $root.greenova.mechanisms.ChartResponse()
        if (object.charts) {
          if (!Array.isArray(object.charts)) {
            throw TypeError(
              '.greenova.mechanisms.ChartResponse.charts: array expected'
            )
          }
          message.charts = []
          for (let i = 0; i < object.charts.length; i += 1) {
            if (typeof object.charts[i] !== 'object') {
              throw TypeError(
                '.greenova.mechanisms.ChartResponse.charts: object expected'
              )
            }
            message.charts[i] = $root.greenova.mechanisms.ChartData.fromObject(
              object.charts[i]
            )
          }
        }
        if (object.error != null) {
          message.error = String(object.error)
        }
        return message
      }

      /**
       * Creates a plain object from a ChartResponse message. Also converts values to other types if specified.
       * @function toObject
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {greenova.mechanisms.ChartResponse} message ChartResponse
       * @param {$protobuf.IConversionOptions} [options] Conversion options
       * @returns {Object.<string,*>} Plain object
       */
      ChartResponse.toObject = function toObject (message, options) {
        if (!options) {
          options = {}
        }
        const object = {}
        if (options.arrays || options.defaults) {
          object.charts = []
        }
        if (options.defaults) {
          object.error = ''
        }
        if (message.charts && message.charts.length) {
          object.charts = []
          for (let j = 0; j < message.charts.length; j += 1) {
            object.charts[j] = $root.greenova.mechanisms.ChartData.toObject(
              message.charts[j],
              options
            )
          }
        }
        if (message.error != null && message.hasOwnProperty('error')) {
          object.error = message.error
        }
        return object
      }

      /**
       * Converts this ChartResponse to JSON.
       * @function toJSON
       * @memberof greenova.mechanisms.ChartResponse
       * @instance
       * @returns {Object.<string,*>} JSON object
       */
      ChartResponse.prototype.toJSON = function toJSON () {
        return this.constructor.toObject(this, $protobuf.util.toJSONOptions)
      }

      /**
       * Gets the default type url for ChartResponse
       * @function getTypeUrl
       * @memberof greenova.mechanisms.ChartResponse
       * @static
       * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
       * @returns {string} The default type url
       */
      ChartResponse.getTypeUrl = function getTypeUrl (typeUrlPrefix) {
        if (typeUrlPrefix === undefined) {
          typeUrlPrefix = 'type.googleapis.com'
        }
        return typeUrlPrefix + '/greenova.mechanisms.ChartResponse'
      }

      return ChartResponse
    })()

    return mechanisms
  })()

  return greenova
})()

module.exports = $root
