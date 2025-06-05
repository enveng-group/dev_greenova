/*eslint-disable block-scoped-var, id-length, no-control-regex, no-magic-numbers, no-prototype-builtins, no-redeclare, no-shadow, no-var, sort-vars*/
"use strict";

var $protobuf = require("protobufjs/minimal");

// Common aliases
var $Reader = $protobuf.Reader, $Writer = $protobuf.Writer, $util = $protobuf.util;

// Exported root namespace
var $root = $protobuf.roots["default"] || ($protobuf.roots["default"] = {});

$root.company = (function() {

    /**
     * Namespace company.
     * @exports company
     * @namespace
     */
    var company = {};

    company.CompanyProto = (function() {

        /**
         * Properties of a CompanyProto.
         * @memberof company
         * @interface ICompanyProto
         * @property {string|null} [id] CompanyProto id
         * @property {string|null} [name] CompanyProto name
         * @property {string|null} [logoUrl] CompanyProto logoUrl
         * @property {string|null} [description] CompanyProto description
         * @property {string|null} [website] CompanyProto website
         * @property {string|null} [address] CompanyProto address
         * @property {string|null} [phone] CompanyProto phone
         * @property {string|null} [email] CompanyProto email
         * @property {string|null} [companyType] CompanyProto companyType
         * @property {string|null} [size] CompanyProto size
         * @property {string|null} [industry] CompanyProto industry
         * @property {boolean|null} [isActive] CompanyProto isActive
         * @property {Array.<string>|null} [memberUserIds] CompanyProto memberUserIds
         * @property {string|null} [createdAt] CompanyProto createdAt
         * @property {string|null} [updatedAt] CompanyProto updatedAt
         */

        /**
         * Constructs a new CompanyProto.
         * @memberof company
         * @classdesc Represents a CompanyProto.
         * @implements ICompanyProto
         * @constructor
         * @param {company.ICompanyProto=} [properties] Properties to set
         */
        function CompanyProto(properties) {
            this.memberUserIds = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CompanyProto id.
         * @member {string} id
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.id = "";

        /**
         * CompanyProto name.
         * @member {string} name
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.name = "";

        /**
         * CompanyProto logoUrl.
         * @member {string} logoUrl
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.logoUrl = "";

        /**
         * CompanyProto description.
         * @member {string} description
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.description = "";

        /**
         * CompanyProto website.
         * @member {string} website
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.website = "";

        /**
         * CompanyProto address.
         * @member {string} address
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.address = "";

        /**
         * CompanyProto phone.
         * @member {string} phone
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.phone = "";

        /**
         * CompanyProto email.
         * @member {string} email
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.email = "";

        /**
         * CompanyProto companyType.
         * @member {string} companyType
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.companyType = "";

        /**
         * CompanyProto size.
         * @member {string} size
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.size = "";

        /**
         * CompanyProto industry.
         * @member {string} industry
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.industry = "";

        /**
         * CompanyProto isActive.
         * @member {boolean} isActive
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.isActive = false;

        /**
         * CompanyProto memberUserIds.
         * @member {Array.<string>} memberUserIds
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.memberUserIds = $util.emptyArray;

        /**
         * CompanyProto createdAt.
         * @member {string} createdAt
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.createdAt = "";

        /**
         * CompanyProto updatedAt.
         * @member {string} updatedAt
         * @memberof company.CompanyProto
         * @instance
         */
        CompanyProto.prototype.updatedAt = "";

        /**
         * Creates a new CompanyProto instance using the specified properties.
         * @function create
         * @memberof company.CompanyProto
         * @static
         * @param {company.ICompanyProto=} [properties] Properties to set
         * @returns {company.CompanyProto} CompanyProto instance
         */
        CompanyProto.create = function create(properties) {
            return new CompanyProto(properties);
        };

        /**
         * Encodes the specified CompanyProto message. Does not implicitly {@link company.CompanyProto.verify|verify} messages.
         * @function encode
         * @memberof company.CompanyProto
         * @static
         * @param {company.ICompanyProto} message CompanyProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.logoUrl != null && Object.hasOwnProperty.call(message, "logoUrl"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.logoUrl);
            if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.description);
            if (message.website != null && Object.hasOwnProperty.call(message, "website"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.website);
            if (message.address != null && Object.hasOwnProperty.call(message, "address"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.address);
            if (message.phone != null && Object.hasOwnProperty.call(message, "phone"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.phone);
            if (message.email != null && Object.hasOwnProperty.call(message, "email"))
                writer.uint32(/* id 8, wireType 2 =*/66).string(message.email);
            if (message.companyType != null && Object.hasOwnProperty.call(message, "companyType"))
                writer.uint32(/* id 9, wireType 2 =*/74).string(message.companyType);
            if (message.size != null && Object.hasOwnProperty.call(message, "size"))
                writer.uint32(/* id 10, wireType 2 =*/82).string(message.size);
            if (message.industry != null && Object.hasOwnProperty.call(message, "industry"))
                writer.uint32(/* id 11, wireType 2 =*/90).string(message.industry);
            if (message.isActive != null && Object.hasOwnProperty.call(message, "isActive"))
                writer.uint32(/* id 12, wireType 0 =*/96).bool(message.isActive);
            if (message.memberUserIds != null && message.memberUserIds.length)
                for (var i = 0; i < message.memberUserIds.length; ++i)
                    writer.uint32(/* id 13, wireType 2 =*/106).string(message.memberUserIds[i]);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 14, wireType 2 =*/114).string(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 15, wireType 2 =*/122).string(message.updatedAt);
            return writer;
        };

        /**
         * Encodes the specified CompanyProto message, length delimited. Does not implicitly {@link company.CompanyProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof company.CompanyProto
         * @static
         * @param {company.ICompanyProto} message CompanyProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CompanyProto message from the specified reader or buffer.
         * @function decode
         * @memberof company.CompanyProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {company.CompanyProto} CompanyProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.company.CompanyProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.logoUrl = reader.string();
                        break;
                    }
                case 4: {
                        message.description = reader.string();
                        break;
                    }
                case 5: {
                        message.website = reader.string();
                        break;
                    }
                case 6: {
                        message.address = reader.string();
                        break;
                    }
                case 7: {
                        message.phone = reader.string();
                        break;
                    }
                case 8: {
                        message.email = reader.string();
                        break;
                    }
                case 9: {
                        message.companyType = reader.string();
                        break;
                    }
                case 10: {
                        message.size = reader.string();
                        break;
                    }
                case 11: {
                        message.industry = reader.string();
                        break;
                    }
                case 12: {
                        message.isActive = reader.bool();
                        break;
                    }
                case 13: {
                        if (!(message.memberUserIds && message.memberUserIds.length))
                            message.memberUserIds = [];
                        message.memberUserIds.push(reader.string());
                        break;
                    }
                case 14: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 15: {
                        message.updatedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CompanyProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof company.CompanyProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {company.CompanyProto} CompanyProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CompanyProto message.
         * @function verify
         * @memberof company.CompanyProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CompanyProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.logoUrl != null && message.hasOwnProperty("logoUrl"))
                if (!$util.isString(message.logoUrl))
                    return "logoUrl: string expected";
            if (message.description != null && message.hasOwnProperty("description"))
                if (!$util.isString(message.description))
                    return "description: string expected";
            if (message.website != null && message.hasOwnProperty("website"))
                if (!$util.isString(message.website))
                    return "website: string expected";
            if (message.address != null && message.hasOwnProperty("address"))
                if (!$util.isString(message.address))
                    return "address: string expected";
            if (message.phone != null && message.hasOwnProperty("phone"))
                if (!$util.isString(message.phone))
                    return "phone: string expected";
            if (message.email != null && message.hasOwnProperty("email"))
                if (!$util.isString(message.email))
                    return "email: string expected";
            if (message.companyType != null && message.hasOwnProperty("companyType"))
                if (!$util.isString(message.companyType))
                    return "companyType: string expected";
            if (message.size != null && message.hasOwnProperty("size"))
                if (!$util.isString(message.size))
                    return "size: string expected";
            if (message.industry != null && message.hasOwnProperty("industry"))
                if (!$util.isString(message.industry))
                    return "industry: string expected";
            if (message.isActive != null && message.hasOwnProperty("isActive"))
                if (typeof message.isActive !== "boolean")
                    return "isActive: boolean expected";
            if (message.memberUserIds != null && message.hasOwnProperty("memberUserIds")) {
                if (!Array.isArray(message.memberUserIds))
                    return "memberUserIds: array expected";
                for (var i = 0; i < message.memberUserIds.length; ++i)
                    if (!$util.isString(message.memberUserIds[i]))
                        return "memberUserIds: string[] expected";
            }
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isString(message.updatedAt))
                    return "updatedAt: string expected";
            return null;
        };

        /**
         * Creates a CompanyProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof company.CompanyProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {company.CompanyProto} CompanyProto
         */
        CompanyProto.fromObject = function fromObject(object) {
            if (object instanceof $root.company.CompanyProto)
                return object;
            var message = new $root.company.CompanyProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.name != null)
                message.name = String(object.name);
            if (object.logoUrl != null)
                message.logoUrl = String(object.logoUrl);
            if (object.description != null)
                message.description = String(object.description);
            if (object.website != null)
                message.website = String(object.website);
            if (object.address != null)
                message.address = String(object.address);
            if (object.phone != null)
                message.phone = String(object.phone);
            if (object.email != null)
                message.email = String(object.email);
            if (object.companyType != null)
                message.companyType = String(object.companyType);
            if (object.size != null)
                message.size = String(object.size);
            if (object.industry != null)
                message.industry = String(object.industry);
            if (object.isActive != null)
                message.isActive = Boolean(object.isActive);
            if (object.memberUserIds) {
                if (!Array.isArray(object.memberUserIds))
                    throw TypeError(".company.CompanyProto.memberUserIds: array expected");
                message.memberUserIds = [];
                for (var i = 0; i < object.memberUserIds.length; ++i)
                    message.memberUserIds[i] = String(object.memberUserIds[i]);
            }
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.updatedAt != null)
                message.updatedAt = String(object.updatedAt);
            return message;
        };

        /**
         * Creates a plain object from a CompanyProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof company.CompanyProto
         * @static
         * @param {company.CompanyProto} message CompanyProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CompanyProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.memberUserIds = [];
            if (options.defaults) {
                object.id = "";
                object.name = "";
                object.logoUrl = "";
                object.description = "";
                object.website = "";
                object.address = "";
                object.phone = "";
                object.email = "";
                object.companyType = "";
                object.size = "";
                object.industry = "";
                object.isActive = false;
                object.createdAt = "";
                object.updatedAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.logoUrl != null && message.hasOwnProperty("logoUrl"))
                object.logoUrl = message.logoUrl;
            if (message.description != null && message.hasOwnProperty("description"))
                object.description = message.description;
            if (message.website != null && message.hasOwnProperty("website"))
                object.website = message.website;
            if (message.address != null && message.hasOwnProperty("address"))
                object.address = message.address;
            if (message.phone != null && message.hasOwnProperty("phone"))
                object.phone = message.phone;
            if (message.email != null && message.hasOwnProperty("email"))
                object.email = message.email;
            if (message.companyType != null && message.hasOwnProperty("companyType"))
                object.companyType = message.companyType;
            if (message.size != null && message.hasOwnProperty("size"))
                object.size = message.size;
            if (message.industry != null && message.hasOwnProperty("industry"))
                object.industry = message.industry;
            if (message.isActive != null && message.hasOwnProperty("isActive"))
                object.isActive = message.isActive;
            if (message.memberUserIds && message.memberUserIds.length) {
                object.memberUserIds = [];
                for (var j = 0; j < message.memberUserIds.length; ++j)
                    object.memberUserIds[j] = message.memberUserIds[j];
            }
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                object.updatedAt = message.updatedAt;
            return object;
        };

        /**
         * Converts this CompanyProto to JSON.
         * @function toJSON
         * @memberof company.CompanyProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CompanyProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CompanyProto
         * @function getTypeUrl
         * @memberof company.CompanyProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CompanyProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/company.CompanyProto";
        };

        return CompanyProto;
    })();

    company.CompanyMembershipProto = (function() {

        /**
         * Properties of a CompanyMembershipProto.
         * @memberof company
         * @interface ICompanyMembershipProto
         * @property {string|null} [id] CompanyMembershipProto id
         * @property {string|null} [companyId] CompanyMembershipProto companyId
         * @property {string|null} [userId] CompanyMembershipProto userId
         * @property {string|null} [role] CompanyMembershipProto role
         * @property {string|null} [department] CompanyMembershipProto department
         * @property {string|null} [position] CompanyMembershipProto position
         * @property {string|null} [dateJoined] CompanyMembershipProto dateJoined
         * @property {boolean|null} [isPrimary] CompanyMembershipProto isPrimary
         */

        /**
         * Constructs a new CompanyMembershipProto.
         * @memberof company
         * @classdesc Represents a CompanyMembershipProto.
         * @implements ICompanyMembershipProto
         * @constructor
         * @param {company.ICompanyMembershipProto=} [properties] Properties to set
         */
        function CompanyMembershipProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CompanyMembershipProto id.
         * @member {string} id
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.id = "";

        /**
         * CompanyMembershipProto companyId.
         * @member {string} companyId
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.companyId = "";

        /**
         * CompanyMembershipProto userId.
         * @member {string} userId
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.userId = "";

        /**
         * CompanyMembershipProto role.
         * @member {string} role
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.role = "";

        /**
         * CompanyMembershipProto department.
         * @member {string} department
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.department = "";

        /**
         * CompanyMembershipProto position.
         * @member {string} position
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.position = "";

        /**
         * CompanyMembershipProto dateJoined.
         * @member {string} dateJoined
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.dateJoined = "";

        /**
         * CompanyMembershipProto isPrimary.
         * @member {boolean} isPrimary
         * @memberof company.CompanyMembershipProto
         * @instance
         */
        CompanyMembershipProto.prototype.isPrimary = false;

        /**
         * Creates a new CompanyMembershipProto instance using the specified properties.
         * @function create
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {company.ICompanyMembershipProto=} [properties] Properties to set
         * @returns {company.CompanyMembershipProto} CompanyMembershipProto instance
         */
        CompanyMembershipProto.create = function create(properties) {
            return new CompanyMembershipProto(properties);
        };

        /**
         * Encodes the specified CompanyMembershipProto message. Does not implicitly {@link company.CompanyMembershipProto.verify|verify} messages.
         * @function encode
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {company.ICompanyMembershipProto} message CompanyMembershipProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyMembershipProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.companyId != null && Object.hasOwnProperty.call(message, "companyId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.companyId);
            if (message.userId != null && Object.hasOwnProperty.call(message, "userId"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.userId);
            if (message.role != null && Object.hasOwnProperty.call(message, "role"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.role);
            if (message.department != null && Object.hasOwnProperty.call(message, "department"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.department);
            if (message.position != null && Object.hasOwnProperty.call(message, "position"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.position);
            if (message.dateJoined != null && Object.hasOwnProperty.call(message, "dateJoined"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.dateJoined);
            if (message.isPrimary != null && Object.hasOwnProperty.call(message, "isPrimary"))
                writer.uint32(/* id 8, wireType 0 =*/64).bool(message.isPrimary);
            return writer;
        };

        /**
         * Encodes the specified CompanyMembershipProto message, length delimited. Does not implicitly {@link company.CompanyMembershipProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {company.ICompanyMembershipProto} message CompanyMembershipProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyMembershipProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CompanyMembershipProto message from the specified reader or buffer.
         * @function decode
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {company.CompanyMembershipProto} CompanyMembershipProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyMembershipProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.company.CompanyMembershipProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.companyId = reader.string();
                        break;
                    }
                case 3: {
                        message.userId = reader.string();
                        break;
                    }
                case 4: {
                        message.role = reader.string();
                        break;
                    }
                case 5: {
                        message.department = reader.string();
                        break;
                    }
                case 6: {
                        message.position = reader.string();
                        break;
                    }
                case 7: {
                        message.dateJoined = reader.string();
                        break;
                    }
                case 8: {
                        message.isPrimary = reader.bool();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CompanyMembershipProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {company.CompanyMembershipProto} CompanyMembershipProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyMembershipProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CompanyMembershipProto message.
         * @function verify
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CompanyMembershipProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.companyId != null && message.hasOwnProperty("companyId"))
                if (!$util.isString(message.companyId))
                    return "companyId: string expected";
            if (message.userId != null && message.hasOwnProperty("userId"))
                if (!$util.isString(message.userId))
                    return "userId: string expected";
            if (message.role != null && message.hasOwnProperty("role"))
                if (!$util.isString(message.role))
                    return "role: string expected";
            if (message.department != null && message.hasOwnProperty("department"))
                if (!$util.isString(message.department))
                    return "department: string expected";
            if (message.position != null && message.hasOwnProperty("position"))
                if (!$util.isString(message.position))
                    return "position: string expected";
            if (message.dateJoined != null && message.hasOwnProperty("dateJoined"))
                if (!$util.isString(message.dateJoined))
                    return "dateJoined: string expected";
            if (message.isPrimary != null && message.hasOwnProperty("isPrimary"))
                if (typeof message.isPrimary !== "boolean")
                    return "isPrimary: boolean expected";
            return null;
        };

        /**
         * Creates a CompanyMembershipProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {company.CompanyMembershipProto} CompanyMembershipProto
         */
        CompanyMembershipProto.fromObject = function fromObject(object) {
            if (object instanceof $root.company.CompanyMembershipProto)
                return object;
            var message = new $root.company.CompanyMembershipProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.companyId != null)
                message.companyId = String(object.companyId);
            if (object.userId != null)
                message.userId = String(object.userId);
            if (object.role != null)
                message.role = String(object.role);
            if (object.department != null)
                message.department = String(object.department);
            if (object.position != null)
                message.position = String(object.position);
            if (object.dateJoined != null)
                message.dateJoined = String(object.dateJoined);
            if (object.isPrimary != null)
                message.isPrimary = Boolean(object.isPrimary);
            return message;
        };

        /**
         * Creates a plain object from a CompanyMembershipProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {company.CompanyMembershipProto} message CompanyMembershipProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CompanyMembershipProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.companyId = "";
                object.userId = "";
                object.role = "";
                object.department = "";
                object.position = "";
                object.dateJoined = "";
                object.isPrimary = false;
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.companyId != null && message.hasOwnProperty("companyId"))
                object.companyId = message.companyId;
            if (message.userId != null && message.hasOwnProperty("userId"))
                object.userId = message.userId;
            if (message.role != null && message.hasOwnProperty("role"))
                object.role = message.role;
            if (message.department != null && message.hasOwnProperty("department"))
                object.department = message.department;
            if (message.position != null && message.hasOwnProperty("position"))
                object.position = message.position;
            if (message.dateJoined != null && message.hasOwnProperty("dateJoined"))
                object.dateJoined = message.dateJoined;
            if (message.isPrimary != null && message.hasOwnProperty("isPrimary"))
                object.isPrimary = message.isPrimary;
            return object;
        };

        /**
         * Converts this CompanyMembershipProto to JSON.
         * @function toJSON
         * @memberof company.CompanyMembershipProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CompanyMembershipProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CompanyMembershipProto
         * @function getTypeUrl
         * @memberof company.CompanyMembershipProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CompanyMembershipProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/company.CompanyMembershipProto";
        };

        return CompanyMembershipProto;
    })();

    company.CompanyDocumentProto = (function() {

        /**
         * Properties of a CompanyDocumentProto.
         * @memberof company
         * @interface ICompanyDocumentProto
         * @property {string|null} [id] CompanyDocumentProto id
         * @property {string|null} [companyId] CompanyDocumentProto companyId
         * @property {string|null} [name] CompanyDocumentProto name
         * @property {string|null} [description] CompanyDocumentProto description
         * @property {string|null} [fileUrl] CompanyDocumentProto fileUrl
         * @property {string|null} [documentType] CompanyDocumentProto documentType
         * @property {string|null} [uploadedByUserId] CompanyDocumentProto uploadedByUserId
         * @property {string|null} [uploadedAt] CompanyDocumentProto uploadedAt
         */

        /**
         * Constructs a new CompanyDocumentProto.
         * @memberof company
         * @classdesc Represents a CompanyDocumentProto.
         * @implements ICompanyDocumentProto
         * @constructor
         * @param {company.ICompanyDocumentProto=} [properties] Properties to set
         */
        function CompanyDocumentProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CompanyDocumentProto id.
         * @member {string} id
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.id = "";

        /**
         * CompanyDocumentProto companyId.
         * @member {string} companyId
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.companyId = "";

        /**
         * CompanyDocumentProto name.
         * @member {string} name
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.name = "";

        /**
         * CompanyDocumentProto description.
         * @member {string} description
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.description = "";

        /**
         * CompanyDocumentProto fileUrl.
         * @member {string} fileUrl
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.fileUrl = "";

        /**
         * CompanyDocumentProto documentType.
         * @member {string} documentType
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.documentType = "";

        /**
         * CompanyDocumentProto uploadedByUserId.
         * @member {string} uploadedByUserId
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.uploadedByUserId = "";

        /**
         * CompanyDocumentProto uploadedAt.
         * @member {string} uploadedAt
         * @memberof company.CompanyDocumentProto
         * @instance
         */
        CompanyDocumentProto.prototype.uploadedAt = "";

        /**
         * Creates a new CompanyDocumentProto instance using the specified properties.
         * @function create
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {company.ICompanyDocumentProto=} [properties] Properties to set
         * @returns {company.CompanyDocumentProto} CompanyDocumentProto instance
         */
        CompanyDocumentProto.create = function create(properties) {
            return new CompanyDocumentProto(properties);
        };

        /**
         * Encodes the specified CompanyDocumentProto message. Does not implicitly {@link company.CompanyDocumentProto.verify|verify} messages.
         * @function encode
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {company.ICompanyDocumentProto} message CompanyDocumentProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyDocumentProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.companyId != null && Object.hasOwnProperty.call(message, "companyId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.companyId);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.name);
            if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.description);
            if (message.fileUrl != null && Object.hasOwnProperty.call(message, "fileUrl"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.fileUrl);
            if (message.documentType != null && Object.hasOwnProperty.call(message, "documentType"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.documentType);
            if (message.uploadedByUserId != null && Object.hasOwnProperty.call(message, "uploadedByUserId"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.uploadedByUserId);
            if (message.uploadedAt != null && Object.hasOwnProperty.call(message, "uploadedAt"))
                writer.uint32(/* id 8, wireType 2 =*/66).string(message.uploadedAt);
            return writer;
        };

        /**
         * Encodes the specified CompanyDocumentProto message, length delimited. Does not implicitly {@link company.CompanyDocumentProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {company.ICompanyDocumentProto} message CompanyDocumentProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyDocumentProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CompanyDocumentProto message from the specified reader or buffer.
         * @function decode
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {company.CompanyDocumentProto} CompanyDocumentProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyDocumentProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.company.CompanyDocumentProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.companyId = reader.string();
                        break;
                    }
                case 3: {
                        message.name = reader.string();
                        break;
                    }
                case 4: {
                        message.description = reader.string();
                        break;
                    }
                case 5: {
                        message.fileUrl = reader.string();
                        break;
                    }
                case 6: {
                        message.documentType = reader.string();
                        break;
                    }
                case 7: {
                        message.uploadedByUserId = reader.string();
                        break;
                    }
                case 8: {
                        message.uploadedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CompanyDocumentProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {company.CompanyDocumentProto} CompanyDocumentProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyDocumentProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CompanyDocumentProto message.
         * @function verify
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CompanyDocumentProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.companyId != null && message.hasOwnProperty("companyId"))
                if (!$util.isString(message.companyId))
                    return "companyId: string expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.description != null && message.hasOwnProperty("description"))
                if (!$util.isString(message.description))
                    return "description: string expected";
            if (message.fileUrl != null && message.hasOwnProperty("fileUrl"))
                if (!$util.isString(message.fileUrl))
                    return "fileUrl: string expected";
            if (message.documentType != null && message.hasOwnProperty("documentType"))
                if (!$util.isString(message.documentType))
                    return "documentType: string expected";
            if (message.uploadedByUserId != null && message.hasOwnProperty("uploadedByUserId"))
                if (!$util.isString(message.uploadedByUserId))
                    return "uploadedByUserId: string expected";
            if (message.uploadedAt != null && message.hasOwnProperty("uploadedAt"))
                if (!$util.isString(message.uploadedAt))
                    return "uploadedAt: string expected";
            return null;
        };

        /**
         * Creates a CompanyDocumentProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {company.CompanyDocumentProto} CompanyDocumentProto
         */
        CompanyDocumentProto.fromObject = function fromObject(object) {
            if (object instanceof $root.company.CompanyDocumentProto)
                return object;
            var message = new $root.company.CompanyDocumentProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.companyId != null)
                message.companyId = String(object.companyId);
            if (object.name != null)
                message.name = String(object.name);
            if (object.description != null)
                message.description = String(object.description);
            if (object.fileUrl != null)
                message.fileUrl = String(object.fileUrl);
            if (object.documentType != null)
                message.documentType = String(object.documentType);
            if (object.uploadedByUserId != null)
                message.uploadedByUserId = String(object.uploadedByUserId);
            if (object.uploadedAt != null)
                message.uploadedAt = String(object.uploadedAt);
            return message;
        };

        /**
         * Creates a plain object from a CompanyDocumentProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {company.CompanyDocumentProto} message CompanyDocumentProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CompanyDocumentProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.companyId = "";
                object.name = "";
                object.description = "";
                object.fileUrl = "";
                object.documentType = "";
                object.uploadedByUserId = "";
                object.uploadedAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.companyId != null && message.hasOwnProperty("companyId"))
                object.companyId = message.companyId;
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.description != null && message.hasOwnProperty("description"))
                object.description = message.description;
            if (message.fileUrl != null && message.hasOwnProperty("fileUrl"))
                object.fileUrl = message.fileUrl;
            if (message.documentType != null && message.hasOwnProperty("documentType"))
                object.documentType = message.documentType;
            if (message.uploadedByUserId != null && message.hasOwnProperty("uploadedByUserId"))
                object.uploadedByUserId = message.uploadedByUserId;
            if (message.uploadedAt != null && message.hasOwnProperty("uploadedAt"))
                object.uploadedAt = message.uploadedAt;
            return object;
        };

        /**
         * Converts this CompanyDocumentProto to JSON.
         * @function toJSON
         * @memberof company.CompanyDocumentProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CompanyDocumentProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CompanyDocumentProto
         * @function getTypeUrl
         * @memberof company.CompanyDocumentProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CompanyDocumentProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/company.CompanyDocumentProto";
        };

        return CompanyDocumentProto;
    })();

    company.CompanyCollection = (function() {

        /**
         * Properties of a CompanyCollection.
         * @memberof company
         * @interface ICompanyCollection
         * @property {Array.<company.ICompanyProto>|null} [companies] CompanyCollection companies
         */

        /**
         * Constructs a new CompanyCollection.
         * @memberof company
         * @classdesc Represents a CompanyCollection.
         * @implements ICompanyCollection
         * @constructor
         * @param {company.ICompanyCollection=} [properties] Properties to set
         */
        function CompanyCollection(properties) {
            this.companies = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CompanyCollection companies.
         * @member {Array.<company.ICompanyProto>} companies
         * @memberof company.CompanyCollection
         * @instance
         */
        CompanyCollection.prototype.companies = $util.emptyArray;

        /**
         * Creates a new CompanyCollection instance using the specified properties.
         * @function create
         * @memberof company.CompanyCollection
         * @static
         * @param {company.ICompanyCollection=} [properties] Properties to set
         * @returns {company.CompanyCollection} CompanyCollection instance
         */
        CompanyCollection.create = function create(properties) {
            return new CompanyCollection(properties);
        };

        /**
         * Encodes the specified CompanyCollection message. Does not implicitly {@link company.CompanyCollection.verify|verify} messages.
         * @function encode
         * @memberof company.CompanyCollection
         * @static
         * @param {company.ICompanyCollection} message CompanyCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.companies != null && message.companies.length)
                for (var i = 0; i < message.companies.length; ++i)
                    $root.company.CompanyProto.encode(message.companies[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified CompanyCollection message, length delimited. Does not implicitly {@link company.CompanyCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof company.CompanyCollection
         * @static
         * @param {company.ICompanyCollection} message CompanyCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CompanyCollection message from the specified reader or buffer.
         * @function decode
         * @memberof company.CompanyCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {company.CompanyCollection} CompanyCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.company.CompanyCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.companies && message.companies.length))
                            message.companies = [];
                        message.companies.push($root.company.CompanyProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CompanyCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof company.CompanyCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {company.CompanyCollection} CompanyCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CompanyCollection message.
         * @function verify
         * @memberof company.CompanyCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CompanyCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.companies != null && message.hasOwnProperty("companies")) {
                if (!Array.isArray(message.companies))
                    return "companies: array expected";
                for (var i = 0; i < message.companies.length; ++i) {
                    var error = $root.company.CompanyProto.verify(message.companies[i]);
                    if (error)
                        return "companies." + error;
                }
            }
            return null;
        };

        /**
         * Creates a CompanyCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof company.CompanyCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {company.CompanyCollection} CompanyCollection
         */
        CompanyCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.company.CompanyCollection)
                return object;
            var message = new $root.company.CompanyCollection();
            if (object.companies) {
                if (!Array.isArray(object.companies))
                    throw TypeError(".company.CompanyCollection.companies: array expected");
                message.companies = [];
                for (var i = 0; i < object.companies.length; ++i) {
                    if (typeof object.companies[i] !== "object")
                        throw TypeError(".company.CompanyCollection.companies: object expected");
                    message.companies[i] = $root.company.CompanyProto.fromObject(object.companies[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a CompanyCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof company.CompanyCollection
         * @static
         * @param {company.CompanyCollection} message CompanyCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CompanyCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.companies = [];
            if (message.companies && message.companies.length) {
                object.companies = [];
                for (var j = 0; j < message.companies.length; ++j)
                    object.companies[j] = $root.company.CompanyProto.toObject(message.companies[j], options);
            }
            return object;
        };

        /**
         * Converts this CompanyCollection to JSON.
         * @function toJSON
         * @memberof company.CompanyCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CompanyCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CompanyCollection
         * @function getTypeUrl
         * @memberof company.CompanyCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CompanyCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/company.CompanyCollection";
        };

        return CompanyCollection;
    })();

    company.CompanyMembershipCollection = (function() {

        /**
         * Properties of a CompanyMembershipCollection.
         * @memberof company
         * @interface ICompanyMembershipCollection
         * @property {Array.<company.ICompanyMembershipProto>|null} [memberships] CompanyMembershipCollection memberships
         */

        /**
         * Constructs a new CompanyMembershipCollection.
         * @memberof company
         * @classdesc Represents a CompanyMembershipCollection.
         * @implements ICompanyMembershipCollection
         * @constructor
         * @param {company.ICompanyMembershipCollection=} [properties] Properties to set
         */
        function CompanyMembershipCollection(properties) {
            this.memberships = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CompanyMembershipCollection memberships.
         * @member {Array.<company.ICompanyMembershipProto>} memberships
         * @memberof company.CompanyMembershipCollection
         * @instance
         */
        CompanyMembershipCollection.prototype.memberships = $util.emptyArray;

        /**
         * Creates a new CompanyMembershipCollection instance using the specified properties.
         * @function create
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {company.ICompanyMembershipCollection=} [properties] Properties to set
         * @returns {company.CompanyMembershipCollection} CompanyMembershipCollection instance
         */
        CompanyMembershipCollection.create = function create(properties) {
            return new CompanyMembershipCollection(properties);
        };

        /**
         * Encodes the specified CompanyMembershipCollection message. Does not implicitly {@link company.CompanyMembershipCollection.verify|verify} messages.
         * @function encode
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {company.ICompanyMembershipCollection} message CompanyMembershipCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyMembershipCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.memberships != null && message.memberships.length)
                for (var i = 0; i < message.memberships.length; ++i)
                    $root.company.CompanyMembershipProto.encode(message.memberships[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified CompanyMembershipCollection message, length delimited. Does not implicitly {@link company.CompanyMembershipCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {company.ICompanyMembershipCollection} message CompanyMembershipCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyMembershipCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CompanyMembershipCollection message from the specified reader or buffer.
         * @function decode
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {company.CompanyMembershipCollection} CompanyMembershipCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyMembershipCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.company.CompanyMembershipCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.memberships && message.memberships.length))
                            message.memberships = [];
                        message.memberships.push($root.company.CompanyMembershipProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CompanyMembershipCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {company.CompanyMembershipCollection} CompanyMembershipCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyMembershipCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CompanyMembershipCollection message.
         * @function verify
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CompanyMembershipCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.memberships != null && message.hasOwnProperty("memberships")) {
                if (!Array.isArray(message.memberships))
                    return "memberships: array expected";
                for (var i = 0; i < message.memberships.length; ++i) {
                    var error = $root.company.CompanyMembershipProto.verify(message.memberships[i]);
                    if (error)
                        return "memberships." + error;
                }
            }
            return null;
        };

        /**
         * Creates a CompanyMembershipCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {company.CompanyMembershipCollection} CompanyMembershipCollection
         */
        CompanyMembershipCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.company.CompanyMembershipCollection)
                return object;
            var message = new $root.company.CompanyMembershipCollection();
            if (object.memberships) {
                if (!Array.isArray(object.memberships))
                    throw TypeError(".company.CompanyMembershipCollection.memberships: array expected");
                message.memberships = [];
                for (var i = 0; i < object.memberships.length; ++i) {
                    if (typeof object.memberships[i] !== "object")
                        throw TypeError(".company.CompanyMembershipCollection.memberships: object expected");
                    message.memberships[i] = $root.company.CompanyMembershipProto.fromObject(object.memberships[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a CompanyMembershipCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {company.CompanyMembershipCollection} message CompanyMembershipCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CompanyMembershipCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.memberships = [];
            if (message.memberships && message.memberships.length) {
                object.memberships = [];
                for (var j = 0; j < message.memberships.length; ++j)
                    object.memberships[j] = $root.company.CompanyMembershipProto.toObject(message.memberships[j], options);
            }
            return object;
        };

        /**
         * Converts this CompanyMembershipCollection to JSON.
         * @function toJSON
         * @memberof company.CompanyMembershipCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CompanyMembershipCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CompanyMembershipCollection
         * @function getTypeUrl
         * @memberof company.CompanyMembershipCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CompanyMembershipCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/company.CompanyMembershipCollection";
        };

        return CompanyMembershipCollection;
    })();

    company.CompanyDocumentCollection = (function() {

        /**
         * Properties of a CompanyDocumentCollection.
         * @memberof company
         * @interface ICompanyDocumentCollection
         * @property {Array.<company.ICompanyDocumentProto>|null} [documents] CompanyDocumentCollection documents
         */

        /**
         * Constructs a new CompanyDocumentCollection.
         * @memberof company
         * @classdesc Represents a CompanyDocumentCollection.
         * @implements ICompanyDocumentCollection
         * @constructor
         * @param {company.ICompanyDocumentCollection=} [properties] Properties to set
         */
        function CompanyDocumentCollection(properties) {
            this.documents = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CompanyDocumentCollection documents.
         * @member {Array.<company.ICompanyDocumentProto>} documents
         * @memberof company.CompanyDocumentCollection
         * @instance
         */
        CompanyDocumentCollection.prototype.documents = $util.emptyArray;

        /**
         * Creates a new CompanyDocumentCollection instance using the specified properties.
         * @function create
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {company.ICompanyDocumentCollection=} [properties] Properties to set
         * @returns {company.CompanyDocumentCollection} CompanyDocumentCollection instance
         */
        CompanyDocumentCollection.create = function create(properties) {
            return new CompanyDocumentCollection(properties);
        };

        /**
         * Encodes the specified CompanyDocumentCollection message. Does not implicitly {@link company.CompanyDocumentCollection.verify|verify} messages.
         * @function encode
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {company.ICompanyDocumentCollection} message CompanyDocumentCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyDocumentCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.documents != null && message.documents.length)
                for (var i = 0; i < message.documents.length; ++i)
                    $root.company.CompanyDocumentProto.encode(message.documents[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified CompanyDocumentCollection message, length delimited. Does not implicitly {@link company.CompanyDocumentCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {company.ICompanyDocumentCollection} message CompanyDocumentCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CompanyDocumentCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CompanyDocumentCollection message from the specified reader or buffer.
         * @function decode
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {company.CompanyDocumentCollection} CompanyDocumentCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyDocumentCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.company.CompanyDocumentCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.documents && message.documents.length))
                            message.documents = [];
                        message.documents.push($root.company.CompanyDocumentProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CompanyDocumentCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {company.CompanyDocumentCollection} CompanyDocumentCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CompanyDocumentCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CompanyDocumentCollection message.
         * @function verify
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CompanyDocumentCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.documents != null && message.hasOwnProperty("documents")) {
                if (!Array.isArray(message.documents))
                    return "documents: array expected";
                for (var i = 0; i < message.documents.length; ++i) {
                    var error = $root.company.CompanyDocumentProto.verify(message.documents[i]);
                    if (error)
                        return "documents." + error;
                }
            }
            return null;
        };

        /**
         * Creates a CompanyDocumentCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {company.CompanyDocumentCollection} CompanyDocumentCollection
         */
        CompanyDocumentCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.company.CompanyDocumentCollection)
                return object;
            var message = new $root.company.CompanyDocumentCollection();
            if (object.documents) {
                if (!Array.isArray(object.documents))
                    throw TypeError(".company.CompanyDocumentCollection.documents: array expected");
                message.documents = [];
                for (var i = 0; i < object.documents.length; ++i) {
                    if (typeof object.documents[i] !== "object")
                        throw TypeError(".company.CompanyDocumentCollection.documents: object expected");
                    message.documents[i] = $root.company.CompanyDocumentProto.fromObject(object.documents[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a CompanyDocumentCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {company.CompanyDocumentCollection} message CompanyDocumentCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CompanyDocumentCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.documents = [];
            if (message.documents && message.documents.length) {
                object.documents = [];
                for (var j = 0; j < message.documents.length; ++j)
                    object.documents[j] = $root.company.CompanyDocumentProto.toObject(message.documents[j], options);
            }
            return object;
        };

        /**
         * Converts this CompanyDocumentCollection to JSON.
         * @function toJSON
         * @memberof company.CompanyDocumentCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CompanyDocumentCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CompanyDocumentCollection
         * @function getTypeUrl
         * @memberof company.CompanyDocumentCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CompanyDocumentCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/company.CompanyDocumentCollection";
        };

        return CompanyDocumentCollection;
    })();

    return company;
})();

$root.projects = (function() {

    /**
     * Namespace projects.
     * @exports projects
     * @namespace
     */
    var projects = {};

    projects.ProjectProto = (function() {

        /**
         * Properties of a ProjectProto.
         * @memberof projects
         * @interface IProjectProto
         * @property {string|null} [id] ProjectProto id
         * @property {string|null} [name] ProjectProto name
         * @property {string|null} [description] ProjectProto description
         * @property {Array.<string>|null} [memberUserIds] ProjectProto memberUserIds
         * @property {string|null} [createdAt] ProjectProto createdAt
         * @property {string|null} [updatedAt] ProjectProto updatedAt
         */

        /**
         * Constructs a new ProjectProto.
         * @memberof projects
         * @classdesc Represents a ProjectProto.
         * @implements IProjectProto
         * @constructor
         * @param {projects.IProjectProto=} [properties] Properties to set
         */
        function ProjectProto(properties) {
            this.memberUserIds = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProjectProto id.
         * @member {string} id
         * @memberof projects.ProjectProto
         * @instance
         */
        ProjectProto.prototype.id = "";

        /**
         * ProjectProto name.
         * @member {string} name
         * @memberof projects.ProjectProto
         * @instance
         */
        ProjectProto.prototype.name = "";

        /**
         * ProjectProto description.
         * @member {string} description
         * @memberof projects.ProjectProto
         * @instance
         */
        ProjectProto.prototype.description = "";

        /**
         * ProjectProto memberUserIds.
         * @member {Array.<string>} memberUserIds
         * @memberof projects.ProjectProto
         * @instance
         */
        ProjectProto.prototype.memberUserIds = $util.emptyArray;

        /**
         * ProjectProto createdAt.
         * @member {string} createdAt
         * @memberof projects.ProjectProto
         * @instance
         */
        ProjectProto.prototype.createdAt = "";

        /**
         * ProjectProto updatedAt.
         * @member {string} updatedAt
         * @memberof projects.ProjectProto
         * @instance
         */
        ProjectProto.prototype.updatedAt = "";

        /**
         * Creates a new ProjectProto instance using the specified properties.
         * @function create
         * @memberof projects.ProjectProto
         * @static
         * @param {projects.IProjectProto=} [properties] Properties to set
         * @returns {projects.ProjectProto} ProjectProto instance
         */
        ProjectProto.create = function create(properties) {
            return new ProjectProto(properties);
        };

        /**
         * Encodes the specified ProjectProto message. Does not implicitly {@link projects.ProjectProto.verify|verify} messages.
         * @function encode
         * @memberof projects.ProjectProto
         * @static
         * @param {projects.IProjectProto} message ProjectProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.description);
            if (message.memberUserIds != null && message.memberUserIds.length)
                for (var i = 0; i < message.memberUserIds.length; ++i)
                    writer.uint32(/* id 4, wireType 2 =*/34).string(message.memberUserIds[i]);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.updatedAt);
            return writer;
        };

        /**
         * Encodes the specified ProjectProto message, length delimited. Does not implicitly {@link projects.ProjectProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof projects.ProjectProto
         * @static
         * @param {projects.IProjectProto} message ProjectProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProjectProto message from the specified reader or buffer.
         * @function decode
         * @memberof projects.ProjectProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {projects.ProjectProto} ProjectProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.projects.ProjectProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.description = reader.string();
                        break;
                    }
                case 4: {
                        if (!(message.memberUserIds && message.memberUserIds.length))
                            message.memberUserIds = [];
                        message.memberUserIds.push(reader.string());
                        break;
                    }
                case 5: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 6: {
                        message.updatedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProjectProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof projects.ProjectProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {projects.ProjectProto} ProjectProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProjectProto message.
         * @function verify
         * @memberof projects.ProjectProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProjectProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.description != null && message.hasOwnProperty("description"))
                if (!$util.isString(message.description))
                    return "description: string expected";
            if (message.memberUserIds != null && message.hasOwnProperty("memberUserIds")) {
                if (!Array.isArray(message.memberUserIds))
                    return "memberUserIds: array expected";
                for (var i = 0; i < message.memberUserIds.length; ++i)
                    if (!$util.isString(message.memberUserIds[i]))
                        return "memberUserIds: string[] expected";
            }
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isString(message.updatedAt))
                    return "updatedAt: string expected";
            return null;
        };

        /**
         * Creates a ProjectProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof projects.ProjectProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {projects.ProjectProto} ProjectProto
         */
        ProjectProto.fromObject = function fromObject(object) {
            if (object instanceof $root.projects.ProjectProto)
                return object;
            var message = new $root.projects.ProjectProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.name != null)
                message.name = String(object.name);
            if (object.description != null)
                message.description = String(object.description);
            if (object.memberUserIds) {
                if (!Array.isArray(object.memberUserIds))
                    throw TypeError(".projects.ProjectProto.memberUserIds: array expected");
                message.memberUserIds = [];
                for (var i = 0; i < object.memberUserIds.length; ++i)
                    message.memberUserIds[i] = String(object.memberUserIds[i]);
            }
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.updatedAt != null)
                message.updatedAt = String(object.updatedAt);
            return message;
        };

        /**
         * Creates a plain object from a ProjectProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof projects.ProjectProto
         * @static
         * @param {projects.ProjectProto} message ProjectProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProjectProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.memberUserIds = [];
            if (options.defaults) {
                object.id = "";
                object.name = "";
                object.description = "";
                object.createdAt = "";
                object.updatedAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.description != null && message.hasOwnProperty("description"))
                object.description = message.description;
            if (message.memberUserIds && message.memberUserIds.length) {
                object.memberUserIds = [];
                for (var j = 0; j < message.memberUserIds.length; ++j)
                    object.memberUserIds[j] = message.memberUserIds[j];
            }
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                object.updatedAt = message.updatedAt;
            return object;
        };

        /**
         * Converts this ProjectProto to JSON.
         * @function toJSON
         * @memberof projects.ProjectProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProjectProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProjectProto
         * @function getTypeUrl
         * @memberof projects.ProjectProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProjectProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/projects.ProjectProto";
        };

        return ProjectProto;
    })();

    projects.ProjectMembershipProto = (function() {

        /**
         * Properties of a ProjectMembershipProto.
         * @memberof projects
         * @interface IProjectMembershipProto
         * @property {string|null} [id] ProjectMembershipProto id
         * @property {string|null} [projectId] ProjectMembershipProto projectId
         * @property {string|null} [userId] ProjectMembershipProto userId
         * @property {string|null} [role] ProjectMembershipProto role
         * @property {string|null} [createdAt] ProjectMembershipProto createdAt
         * @property {string|null} [updatedAt] ProjectMembershipProto updatedAt
         */

        /**
         * Constructs a new ProjectMembershipProto.
         * @memberof projects
         * @classdesc Represents a ProjectMembershipProto.
         * @implements IProjectMembershipProto
         * @constructor
         * @param {projects.IProjectMembershipProto=} [properties] Properties to set
         */
        function ProjectMembershipProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProjectMembershipProto id.
         * @member {string} id
         * @memberof projects.ProjectMembershipProto
         * @instance
         */
        ProjectMembershipProto.prototype.id = "";

        /**
         * ProjectMembershipProto projectId.
         * @member {string} projectId
         * @memberof projects.ProjectMembershipProto
         * @instance
         */
        ProjectMembershipProto.prototype.projectId = "";

        /**
         * ProjectMembershipProto userId.
         * @member {string} userId
         * @memberof projects.ProjectMembershipProto
         * @instance
         */
        ProjectMembershipProto.prototype.userId = "";

        /**
         * ProjectMembershipProto role.
         * @member {string} role
         * @memberof projects.ProjectMembershipProto
         * @instance
         */
        ProjectMembershipProto.prototype.role = "";

        /**
         * ProjectMembershipProto createdAt.
         * @member {string} createdAt
         * @memberof projects.ProjectMembershipProto
         * @instance
         */
        ProjectMembershipProto.prototype.createdAt = "";

        /**
         * ProjectMembershipProto updatedAt.
         * @member {string} updatedAt
         * @memberof projects.ProjectMembershipProto
         * @instance
         */
        ProjectMembershipProto.prototype.updatedAt = "";

        /**
         * Creates a new ProjectMembershipProto instance using the specified properties.
         * @function create
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {projects.IProjectMembershipProto=} [properties] Properties to set
         * @returns {projects.ProjectMembershipProto} ProjectMembershipProto instance
         */
        ProjectMembershipProto.create = function create(properties) {
            return new ProjectMembershipProto(properties);
        };

        /**
         * Encodes the specified ProjectMembershipProto message. Does not implicitly {@link projects.ProjectMembershipProto.verify|verify} messages.
         * @function encode
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {projects.IProjectMembershipProto} message ProjectMembershipProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectMembershipProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.projectId != null && Object.hasOwnProperty.call(message, "projectId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.projectId);
            if (message.userId != null && Object.hasOwnProperty.call(message, "userId"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.userId);
            if (message.role != null && Object.hasOwnProperty.call(message, "role"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.role);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.updatedAt);
            return writer;
        };

        /**
         * Encodes the specified ProjectMembershipProto message, length delimited. Does not implicitly {@link projects.ProjectMembershipProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {projects.IProjectMembershipProto} message ProjectMembershipProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectMembershipProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProjectMembershipProto message from the specified reader or buffer.
         * @function decode
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {projects.ProjectMembershipProto} ProjectMembershipProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectMembershipProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.projects.ProjectMembershipProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.projectId = reader.string();
                        break;
                    }
                case 3: {
                        message.userId = reader.string();
                        break;
                    }
                case 4: {
                        message.role = reader.string();
                        break;
                    }
                case 5: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 6: {
                        message.updatedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProjectMembershipProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {projects.ProjectMembershipProto} ProjectMembershipProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectMembershipProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProjectMembershipProto message.
         * @function verify
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProjectMembershipProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.projectId != null && message.hasOwnProperty("projectId"))
                if (!$util.isString(message.projectId))
                    return "projectId: string expected";
            if (message.userId != null && message.hasOwnProperty("userId"))
                if (!$util.isString(message.userId))
                    return "userId: string expected";
            if (message.role != null && message.hasOwnProperty("role"))
                if (!$util.isString(message.role))
                    return "role: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isString(message.updatedAt))
                    return "updatedAt: string expected";
            return null;
        };

        /**
         * Creates a ProjectMembershipProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {projects.ProjectMembershipProto} ProjectMembershipProto
         */
        ProjectMembershipProto.fromObject = function fromObject(object) {
            if (object instanceof $root.projects.ProjectMembershipProto)
                return object;
            var message = new $root.projects.ProjectMembershipProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.projectId != null)
                message.projectId = String(object.projectId);
            if (object.userId != null)
                message.userId = String(object.userId);
            if (object.role != null)
                message.role = String(object.role);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.updatedAt != null)
                message.updatedAt = String(object.updatedAt);
            return message;
        };

        /**
         * Creates a plain object from a ProjectMembershipProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {projects.ProjectMembershipProto} message ProjectMembershipProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProjectMembershipProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.projectId = "";
                object.userId = "";
                object.role = "";
                object.createdAt = "";
                object.updatedAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.projectId != null && message.hasOwnProperty("projectId"))
                object.projectId = message.projectId;
            if (message.userId != null && message.hasOwnProperty("userId"))
                object.userId = message.userId;
            if (message.role != null && message.hasOwnProperty("role"))
                object.role = message.role;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                object.updatedAt = message.updatedAt;
            return object;
        };

        /**
         * Converts this ProjectMembershipProto to JSON.
         * @function toJSON
         * @memberof projects.ProjectMembershipProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProjectMembershipProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProjectMembershipProto
         * @function getTypeUrl
         * @memberof projects.ProjectMembershipProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProjectMembershipProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/projects.ProjectMembershipProto";
        };

        return ProjectMembershipProto;
    })();

    projects.ProjectObligationProto = (function() {

        /**
         * Properties of a ProjectObligationProto.
         * @memberof projects
         * @interface IProjectObligationProto
         * @property {string|null} [id] ProjectObligationProto id
         * @property {string|null} [projectId] ProjectObligationProto projectId
         * @property {string|null} [obligationId] ProjectObligationProto obligationId
         * @property {string|null} [createdAt] ProjectObligationProto createdAt
         * @property {string|null} [updatedAt] ProjectObligationProto updatedAt
         */

        /**
         * Constructs a new ProjectObligationProto.
         * @memberof projects
         * @classdesc Represents a ProjectObligationProto.
         * @implements IProjectObligationProto
         * @constructor
         * @param {projects.IProjectObligationProto=} [properties] Properties to set
         */
        function ProjectObligationProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProjectObligationProto id.
         * @member {string} id
         * @memberof projects.ProjectObligationProto
         * @instance
         */
        ProjectObligationProto.prototype.id = "";

        /**
         * ProjectObligationProto projectId.
         * @member {string} projectId
         * @memberof projects.ProjectObligationProto
         * @instance
         */
        ProjectObligationProto.prototype.projectId = "";

        /**
         * ProjectObligationProto obligationId.
         * @member {string} obligationId
         * @memberof projects.ProjectObligationProto
         * @instance
         */
        ProjectObligationProto.prototype.obligationId = "";

        /**
         * ProjectObligationProto createdAt.
         * @member {string} createdAt
         * @memberof projects.ProjectObligationProto
         * @instance
         */
        ProjectObligationProto.prototype.createdAt = "";

        /**
         * ProjectObligationProto updatedAt.
         * @member {string} updatedAt
         * @memberof projects.ProjectObligationProto
         * @instance
         */
        ProjectObligationProto.prototype.updatedAt = "";

        /**
         * Creates a new ProjectObligationProto instance using the specified properties.
         * @function create
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {projects.IProjectObligationProto=} [properties] Properties to set
         * @returns {projects.ProjectObligationProto} ProjectObligationProto instance
         */
        ProjectObligationProto.create = function create(properties) {
            return new ProjectObligationProto(properties);
        };

        /**
         * Encodes the specified ProjectObligationProto message. Does not implicitly {@link projects.ProjectObligationProto.verify|verify} messages.
         * @function encode
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {projects.IProjectObligationProto} message ProjectObligationProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectObligationProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.projectId != null && Object.hasOwnProperty.call(message, "projectId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.projectId);
            if (message.obligationId != null && Object.hasOwnProperty.call(message, "obligationId"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.obligationId);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.updatedAt);
            return writer;
        };

        /**
         * Encodes the specified ProjectObligationProto message, length delimited. Does not implicitly {@link projects.ProjectObligationProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {projects.IProjectObligationProto} message ProjectObligationProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectObligationProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProjectObligationProto message from the specified reader or buffer.
         * @function decode
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {projects.ProjectObligationProto} ProjectObligationProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectObligationProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.projects.ProjectObligationProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.projectId = reader.string();
                        break;
                    }
                case 3: {
                        message.obligationId = reader.string();
                        break;
                    }
                case 4: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 5: {
                        message.updatedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProjectObligationProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {projects.ProjectObligationProto} ProjectObligationProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectObligationProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProjectObligationProto message.
         * @function verify
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProjectObligationProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.projectId != null && message.hasOwnProperty("projectId"))
                if (!$util.isString(message.projectId))
                    return "projectId: string expected";
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                if (!$util.isString(message.obligationId))
                    return "obligationId: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isString(message.updatedAt))
                    return "updatedAt: string expected";
            return null;
        };

        /**
         * Creates a ProjectObligationProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {projects.ProjectObligationProto} ProjectObligationProto
         */
        ProjectObligationProto.fromObject = function fromObject(object) {
            if (object instanceof $root.projects.ProjectObligationProto)
                return object;
            var message = new $root.projects.ProjectObligationProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.projectId != null)
                message.projectId = String(object.projectId);
            if (object.obligationId != null)
                message.obligationId = String(object.obligationId);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.updatedAt != null)
                message.updatedAt = String(object.updatedAt);
            return message;
        };

        /**
         * Creates a plain object from a ProjectObligationProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {projects.ProjectObligationProto} message ProjectObligationProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProjectObligationProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.projectId = "";
                object.obligationId = "";
                object.createdAt = "";
                object.updatedAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.projectId != null && message.hasOwnProperty("projectId"))
                object.projectId = message.projectId;
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                object.obligationId = message.obligationId;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                object.updatedAt = message.updatedAt;
            return object;
        };

        /**
         * Converts this ProjectObligationProto to JSON.
         * @function toJSON
         * @memberof projects.ProjectObligationProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProjectObligationProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProjectObligationProto
         * @function getTypeUrl
         * @memberof projects.ProjectObligationProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProjectObligationProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/projects.ProjectObligationProto";
        };

        return ProjectObligationProto;
    })();

    projects.ProjectCollection = (function() {

        /**
         * Properties of a ProjectCollection.
         * @memberof projects
         * @interface IProjectCollection
         * @property {Array.<projects.IProjectProto>|null} [projects] ProjectCollection projects
         */

        /**
         * Constructs a new ProjectCollection.
         * @memberof projects
         * @classdesc Represents a ProjectCollection.
         * @implements IProjectCollection
         * @constructor
         * @param {projects.IProjectCollection=} [properties] Properties to set
         */
        function ProjectCollection(properties) {
            this.projects = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProjectCollection projects.
         * @member {Array.<projects.IProjectProto>} projects
         * @memberof projects.ProjectCollection
         * @instance
         */
        ProjectCollection.prototype.projects = $util.emptyArray;

        /**
         * Creates a new ProjectCollection instance using the specified properties.
         * @function create
         * @memberof projects.ProjectCollection
         * @static
         * @param {projects.IProjectCollection=} [properties] Properties to set
         * @returns {projects.ProjectCollection} ProjectCollection instance
         */
        ProjectCollection.create = function create(properties) {
            return new ProjectCollection(properties);
        };

        /**
         * Encodes the specified ProjectCollection message. Does not implicitly {@link projects.ProjectCollection.verify|verify} messages.
         * @function encode
         * @memberof projects.ProjectCollection
         * @static
         * @param {projects.IProjectCollection} message ProjectCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.projects != null && message.projects.length)
                for (var i = 0; i < message.projects.length; ++i)
                    $root.projects.ProjectProto.encode(message.projects[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ProjectCollection message, length delimited. Does not implicitly {@link projects.ProjectCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof projects.ProjectCollection
         * @static
         * @param {projects.IProjectCollection} message ProjectCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProjectCollection message from the specified reader or buffer.
         * @function decode
         * @memberof projects.ProjectCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {projects.ProjectCollection} ProjectCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.projects.ProjectCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.projects && message.projects.length))
                            message.projects = [];
                        message.projects.push($root.projects.ProjectProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProjectCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof projects.ProjectCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {projects.ProjectCollection} ProjectCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProjectCollection message.
         * @function verify
         * @memberof projects.ProjectCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProjectCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.projects != null && message.hasOwnProperty("projects")) {
                if (!Array.isArray(message.projects))
                    return "projects: array expected";
                for (var i = 0; i < message.projects.length; ++i) {
                    var error = $root.projects.ProjectProto.verify(message.projects[i]);
                    if (error)
                        return "projects." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ProjectCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof projects.ProjectCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {projects.ProjectCollection} ProjectCollection
         */
        ProjectCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.projects.ProjectCollection)
                return object;
            var message = new $root.projects.ProjectCollection();
            if (object.projects) {
                if (!Array.isArray(object.projects))
                    throw TypeError(".projects.ProjectCollection.projects: array expected");
                message.projects = [];
                for (var i = 0; i < object.projects.length; ++i) {
                    if (typeof object.projects[i] !== "object")
                        throw TypeError(".projects.ProjectCollection.projects: object expected");
                    message.projects[i] = $root.projects.ProjectProto.fromObject(object.projects[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ProjectCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof projects.ProjectCollection
         * @static
         * @param {projects.ProjectCollection} message ProjectCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProjectCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.projects = [];
            if (message.projects && message.projects.length) {
                object.projects = [];
                for (var j = 0; j < message.projects.length; ++j)
                    object.projects[j] = $root.projects.ProjectProto.toObject(message.projects[j], options);
            }
            return object;
        };

        /**
         * Converts this ProjectCollection to JSON.
         * @function toJSON
         * @memberof projects.ProjectCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProjectCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProjectCollection
         * @function getTypeUrl
         * @memberof projects.ProjectCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProjectCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/projects.ProjectCollection";
        };

        return ProjectCollection;
    })();

    projects.ProjectMembershipCollection = (function() {

        /**
         * Properties of a ProjectMembershipCollection.
         * @memberof projects
         * @interface IProjectMembershipCollection
         * @property {Array.<projects.IProjectMembershipProto>|null} [memberships] ProjectMembershipCollection memberships
         */

        /**
         * Constructs a new ProjectMembershipCollection.
         * @memberof projects
         * @classdesc Represents a ProjectMembershipCollection.
         * @implements IProjectMembershipCollection
         * @constructor
         * @param {projects.IProjectMembershipCollection=} [properties] Properties to set
         */
        function ProjectMembershipCollection(properties) {
            this.memberships = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProjectMembershipCollection memberships.
         * @member {Array.<projects.IProjectMembershipProto>} memberships
         * @memberof projects.ProjectMembershipCollection
         * @instance
         */
        ProjectMembershipCollection.prototype.memberships = $util.emptyArray;

        /**
         * Creates a new ProjectMembershipCollection instance using the specified properties.
         * @function create
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {projects.IProjectMembershipCollection=} [properties] Properties to set
         * @returns {projects.ProjectMembershipCollection} ProjectMembershipCollection instance
         */
        ProjectMembershipCollection.create = function create(properties) {
            return new ProjectMembershipCollection(properties);
        };

        /**
         * Encodes the specified ProjectMembershipCollection message. Does not implicitly {@link projects.ProjectMembershipCollection.verify|verify} messages.
         * @function encode
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {projects.IProjectMembershipCollection} message ProjectMembershipCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectMembershipCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.memberships != null && message.memberships.length)
                for (var i = 0; i < message.memberships.length; ++i)
                    $root.projects.ProjectMembershipProto.encode(message.memberships[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ProjectMembershipCollection message, length delimited. Does not implicitly {@link projects.ProjectMembershipCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {projects.IProjectMembershipCollection} message ProjectMembershipCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectMembershipCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProjectMembershipCollection message from the specified reader or buffer.
         * @function decode
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {projects.ProjectMembershipCollection} ProjectMembershipCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectMembershipCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.projects.ProjectMembershipCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.memberships && message.memberships.length))
                            message.memberships = [];
                        message.memberships.push($root.projects.ProjectMembershipProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProjectMembershipCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {projects.ProjectMembershipCollection} ProjectMembershipCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectMembershipCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProjectMembershipCollection message.
         * @function verify
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProjectMembershipCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.memberships != null && message.hasOwnProperty("memberships")) {
                if (!Array.isArray(message.memberships))
                    return "memberships: array expected";
                for (var i = 0; i < message.memberships.length; ++i) {
                    var error = $root.projects.ProjectMembershipProto.verify(message.memberships[i]);
                    if (error)
                        return "memberships." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ProjectMembershipCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {projects.ProjectMembershipCollection} ProjectMembershipCollection
         */
        ProjectMembershipCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.projects.ProjectMembershipCollection)
                return object;
            var message = new $root.projects.ProjectMembershipCollection();
            if (object.memberships) {
                if (!Array.isArray(object.memberships))
                    throw TypeError(".projects.ProjectMembershipCollection.memberships: array expected");
                message.memberships = [];
                for (var i = 0; i < object.memberships.length; ++i) {
                    if (typeof object.memberships[i] !== "object")
                        throw TypeError(".projects.ProjectMembershipCollection.memberships: object expected");
                    message.memberships[i] = $root.projects.ProjectMembershipProto.fromObject(object.memberships[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ProjectMembershipCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {projects.ProjectMembershipCollection} message ProjectMembershipCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProjectMembershipCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.memberships = [];
            if (message.memberships && message.memberships.length) {
                object.memberships = [];
                for (var j = 0; j < message.memberships.length; ++j)
                    object.memberships[j] = $root.projects.ProjectMembershipProto.toObject(message.memberships[j], options);
            }
            return object;
        };

        /**
         * Converts this ProjectMembershipCollection to JSON.
         * @function toJSON
         * @memberof projects.ProjectMembershipCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProjectMembershipCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProjectMembershipCollection
         * @function getTypeUrl
         * @memberof projects.ProjectMembershipCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProjectMembershipCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/projects.ProjectMembershipCollection";
        };

        return ProjectMembershipCollection;
    })();

    projects.ProjectObligationCollection = (function() {

        /**
         * Properties of a ProjectObligationCollection.
         * @memberof projects
         * @interface IProjectObligationCollection
         * @property {Array.<projects.IProjectObligationProto>|null} [projectObligations] ProjectObligationCollection projectObligations
         */

        /**
         * Constructs a new ProjectObligationCollection.
         * @memberof projects
         * @classdesc Represents a ProjectObligationCollection.
         * @implements IProjectObligationCollection
         * @constructor
         * @param {projects.IProjectObligationCollection=} [properties] Properties to set
         */
        function ProjectObligationCollection(properties) {
            this.projectObligations = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProjectObligationCollection projectObligations.
         * @member {Array.<projects.IProjectObligationProto>} projectObligations
         * @memberof projects.ProjectObligationCollection
         * @instance
         */
        ProjectObligationCollection.prototype.projectObligations = $util.emptyArray;

        /**
         * Creates a new ProjectObligationCollection instance using the specified properties.
         * @function create
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {projects.IProjectObligationCollection=} [properties] Properties to set
         * @returns {projects.ProjectObligationCollection} ProjectObligationCollection instance
         */
        ProjectObligationCollection.create = function create(properties) {
            return new ProjectObligationCollection(properties);
        };

        /**
         * Encodes the specified ProjectObligationCollection message. Does not implicitly {@link projects.ProjectObligationCollection.verify|verify} messages.
         * @function encode
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {projects.IProjectObligationCollection} message ProjectObligationCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectObligationCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.projectObligations != null && message.projectObligations.length)
                for (var i = 0; i < message.projectObligations.length; ++i)
                    $root.projects.ProjectObligationProto.encode(message.projectObligations[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ProjectObligationCollection message, length delimited. Does not implicitly {@link projects.ProjectObligationCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {projects.IProjectObligationCollection} message ProjectObligationCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProjectObligationCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProjectObligationCollection message from the specified reader or buffer.
         * @function decode
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {projects.ProjectObligationCollection} ProjectObligationCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectObligationCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.projects.ProjectObligationCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.projectObligations && message.projectObligations.length))
                            message.projectObligations = [];
                        message.projectObligations.push($root.projects.ProjectObligationProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProjectObligationCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {projects.ProjectObligationCollection} ProjectObligationCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProjectObligationCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProjectObligationCollection message.
         * @function verify
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProjectObligationCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.projectObligations != null && message.hasOwnProperty("projectObligations")) {
                if (!Array.isArray(message.projectObligations))
                    return "projectObligations: array expected";
                for (var i = 0; i < message.projectObligations.length; ++i) {
                    var error = $root.projects.ProjectObligationProto.verify(message.projectObligations[i]);
                    if (error)
                        return "projectObligations." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ProjectObligationCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {projects.ProjectObligationCollection} ProjectObligationCollection
         */
        ProjectObligationCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.projects.ProjectObligationCollection)
                return object;
            var message = new $root.projects.ProjectObligationCollection();
            if (object.projectObligations) {
                if (!Array.isArray(object.projectObligations))
                    throw TypeError(".projects.ProjectObligationCollection.projectObligations: array expected");
                message.projectObligations = [];
                for (var i = 0; i < object.projectObligations.length; ++i) {
                    if (typeof object.projectObligations[i] !== "object")
                        throw TypeError(".projects.ProjectObligationCollection.projectObligations: object expected");
                    message.projectObligations[i] = $root.projects.ProjectObligationProto.fromObject(object.projectObligations[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ProjectObligationCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {projects.ProjectObligationCollection} message ProjectObligationCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProjectObligationCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.projectObligations = [];
            if (message.projectObligations && message.projectObligations.length) {
                object.projectObligations = [];
                for (var j = 0; j < message.projectObligations.length; ++j)
                    object.projectObligations[j] = $root.projects.ProjectObligationProto.toObject(message.projectObligations[j], options);
            }
            return object;
        };

        /**
         * Converts this ProjectObligationCollection to JSON.
         * @function toJSON
         * @memberof projects.ProjectObligationCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProjectObligationCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProjectObligationCollection
         * @function getTypeUrl
         * @memberof projects.ProjectObligationCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProjectObligationCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/projects.ProjectObligationCollection";
        };

        return ProjectObligationCollection;
    })();

    return projects;
})();

$root.users = (function() {

    /**
     * Namespace users.
     * @exports users
     * @namespace
     */
    var users = {};

    users.UserProto = (function() {

        /**
         * Properties of a UserProto.
         * @memberof users
         * @interface IUserProto
         * @property {string|null} [id] UserProto id
         * @property {string|null} [username] UserProto username
         * @property {string|null} [email] UserProto email
         * @property {string|null} [firstName] UserProto firstName
         * @property {string|null} [lastName] UserProto lastName
         * @property {boolean|null} [isActive] UserProto isActive
         * @property {string|null} [dateJoined] UserProto dateJoined
         */

        /**
         * Constructs a new UserProto.
         * @memberof users
         * @classdesc Represents a UserProto.
         * @implements IUserProto
         * @constructor
         * @param {users.IUserProto=} [properties] Properties to set
         */
        function UserProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * UserProto id.
         * @member {string} id
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.id = "";

        /**
         * UserProto username.
         * @member {string} username
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.username = "";

        /**
         * UserProto email.
         * @member {string} email
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.email = "";

        /**
         * UserProto firstName.
         * @member {string} firstName
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.firstName = "";

        /**
         * UserProto lastName.
         * @member {string} lastName
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.lastName = "";

        /**
         * UserProto isActive.
         * @member {boolean} isActive
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.isActive = false;

        /**
         * UserProto dateJoined.
         * @member {string} dateJoined
         * @memberof users.UserProto
         * @instance
         */
        UserProto.prototype.dateJoined = "";

        /**
         * Creates a new UserProto instance using the specified properties.
         * @function create
         * @memberof users.UserProto
         * @static
         * @param {users.IUserProto=} [properties] Properties to set
         * @returns {users.UserProto} UserProto instance
         */
        UserProto.create = function create(properties) {
            return new UserProto(properties);
        };

        /**
         * Encodes the specified UserProto message. Does not implicitly {@link users.UserProto.verify|verify} messages.
         * @function encode
         * @memberof users.UserProto
         * @static
         * @param {users.IUserProto} message UserProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        UserProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.username != null && Object.hasOwnProperty.call(message, "username"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.username);
            if (message.email != null && Object.hasOwnProperty.call(message, "email"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.email);
            if (message.firstName != null && Object.hasOwnProperty.call(message, "firstName"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.firstName);
            if (message.lastName != null && Object.hasOwnProperty.call(message, "lastName"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.lastName);
            if (message.isActive != null && Object.hasOwnProperty.call(message, "isActive"))
                writer.uint32(/* id 6, wireType 0 =*/48).bool(message.isActive);
            if (message.dateJoined != null && Object.hasOwnProperty.call(message, "dateJoined"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.dateJoined);
            return writer;
        };

        /**
         * Encodes the specified UserProto message, length delimited. Does not implicitly {@link users.UserProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof users.UserProto
         * @static
         * @param {users.IUserProto} message UserProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        UserProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a UserProto message from the specified reader or buffer.
         * @function decode
         * @memberof users.UserProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {users.UserProto} UserProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        UserProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.users.UserProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.username = reader.string();
                        break;
                    }
                case 3: {
                        message.email = reader.string();
                        break;
                    }
                case 4: {
                        message.firstName = reader.string();
                        break;
                    }
                case 5: {
                        message.lastName = reader.string();
                        break;
                    }
                case 6: {
                        message.isActive = reader.bool();
                        break;
                    }
                case 7: {
                        message.dateJoined = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a UserProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof users.UserProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {users.UserProto} UserProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        UserProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a UserProto message.
         * @function verify
         * @memberof users.UserProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        UserProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.username != null && message.hasOwnProperty("username"))
                if (!$util.isString(message.username))
                    return "username: string expected";
            if (message.email != null && message.hasOwnProperty("email"))
                if (!$util.isString(message.email))
                    return "email: string expected";
            if (message.firstName != null && message.hasOwnProperty("firstName"))
                if (!$util.isString(message.firstName))
                    return "firstName: string expected";
            if (message.lastName != null && message.hasOwnProperty("lastName"))
                if (!$util.isString(message.lastName))
                    return "lastName: string expected";
            if (message.isActive != null && message.hasOwnProperty("isActive"))
                if (typeof message.isActive !== "boolean")
                    return "isActive: boolean expected";
            if (message.dateJoined != null && message.hasOwnProperty("dateJoined"))
                if (!$util.isString(message.dateJoined))
                    return "dateJoined: string expected";
            return null;
        };

        /**
         * Creates a UserProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof users.UserProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {users.UserProto} UserProto
         */
        UserProto.fromObject = function fromObject(object) {
            if (object instanceof $root.users.UserProto)
                return object;
            var message = new $root.users.UserProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.username != null)
                message.username = String(object.username);
            if (object.email != null)
                message.email = String(object.email);
            if (object.firstName != null)
                message.firstName = String(object.firstName);
            if (object.lastName != null)
                message.lastName = String(object.lastName);
            if (object.isActive != null)
                message.isActive = Boolean(object.isActive);
            if (object.dateJoined != null)
                message.dateJoined = String(object.dateJoined);
            return message;
        };

        /**
         * Creates a plain object from a UserProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof users.UserProto
         * @static
         * @param {users.UserProto} message UserProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        UserProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.username = "";
                object.email = "";
                object.firstName = "";
                object.lastName = "";
                object.isActive = false;
                object.dateJoined = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.username != null && message.hasOwnProperty("username"))
                object.username = message.username;
            if (message.email != null && message.hasOwnProperty("email"))
                object.email = message.email;
            if (message.firstName != null && message.hasOwnProperty("firstName"))
                object.firstName = message.firstName;
            if (message.lastName != null && message.hasOwnProperty("lastName"))
                object.lastName = message.lastName;
            if (message.isActive != null && message.hasOwnProperty("isActive"))
                object.isActive = message.isActive;
            if (message.dateJoined != null && message.hasOwnProperty("dateJoined"))
                object.dateJoined = message.dateJoined;
            return object;
        };

        /**
         * Converts this UserProto to JSON.
         * @function toJSON
         * @memberof users.UserProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        UserProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for UserProto
         * @function getTypeUrl
         * @memberof users.UserProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        UserProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/users.UserProto";
        };

        return UserProto;
    })();

    users.ProfileProto = (function() {

        /**
         * Properties of a ProfileProto.
         * @memberof users
         * @interface IProfileProto
         * @property {string|null} [id] ProfileProto id
         * @property {string|null} [userId] ProfileProto userId
         * @property {string|null} [bio] ProfileProto bio
         * @property {string|null} [position] ProfileProto position
         * @property {string|null} [department] ProfileProto department
         * @property {string|null} [phoneNumber] ProfileProto phoneNumber
         * @property {string|null} [profileImageUrl] ProfileProto profileImageUrl
         * @property {string|null} [createdAt] ProfileProto createdAt
         * @property {string|null} [updatedAt] ProfileProto updatedAt
         */

        /**
         * Constructs a new ProfileProto.
         * @memberof users
         * @classdesc Represents a ProfileProto.
         * @implements IProfileProto
         * @constructor
         * @param {users.IProfileProto=} [properties] Properties to set
         */
        function ProfileProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProfileProto id.
         * @member {string} id
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.id = "";

        /**
         * ProfileProto userId.
         * @member {string} userId
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.userId = "";

        /**
         * ProfileProto bio.
         * @member {string} bio
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.bio = "";

        /**
         * ProfileProto position.
         * @member {string} position
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.position = "";

        /**
         * ProfileProto department.
         * @member {string} department
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.department = "";

        /**
         * ProfileProto phoneNumber.
         * @member {string} phoneNumber
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.phoneNumber = "";

        /**
         * ProfileProto profileImageUrl.
         * @member {string} profileImageUrl
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.profileImageUrl = "";

        /**
         * ProfileProto createdAt.
         * @member {string} createdAt
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.createdAt = "";

        /**
         * ProfileProto updatedAt.
         * @member {string} updatedAt
         * @memberof users.ProfileProto
         * @instance
         */
        ProfileProto.prototype.updatedAt = "";

        /**
         * Creates a new ProfileProto instance using the specified properties.
         * @function create
         * @memberof users.ProfileProto
         * @static
         * @param {users.IProfileProto=} [properties] Properties to set
         * @returns {users.ProfileProto} ProfileProto instance
         */
        ProfileProto.create = function create(properties) {
            return new ProfileProto(properties);
        };

        /**
         * Encodes the specified ProfileProto message. Does not implicitly {@link users.ProfileProto.verify|verify} messages.
         * @function encode
         * @memberof users.ProfileProto
         * @static
         * @param {users.IProfileProto} message ProfileProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProfileProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.userId != null && Object.hasOwnProperty.call(message, "userId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.userId);
            if (message.bio != null && Object.hasOwnProperty.call(message, "bio"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.bio);
            if (message.position != null && Object.hasOwnProperty.call(message, "position"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.position);
            if (message.department != null && Object.hasOwnProperty.call(message, "department"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.department);
            if (message.phoneNumber != null && Object.hasOwnProperty.call(message, "phoneNumber"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.phoneNumber);
            if (message.profileImageUrl != null && Object.hasOwnProperty.call(message, "profileImageUrl"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.profileImageUrl);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 8, wireType 2 =*/66).string(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 9, wireType 2 =*/74).string(message.updatedAt);
            return writer;
        };

        /**
         * Encodes the specified ProfileProto message, length delimited. Does not implicitly {@link users.ProfileProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof users.ProfileProto
         * @static
         * @param {users.IProfileProto} message ProfileProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProfileProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProfileProto message from the specified reader or buffer.
         * @function decode
         * @memberof users.ProfileProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {users.ProfileProto} ProfileProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProfileProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.users.ProfileProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.userId = reader.string();
                        break;
                    }
                case 3: {
                        message.bio = reader.string();
                        break;
                    }
                case 4: {
                        message.position = reader.string();
                        break;
                    }
                case 5: {
                        message.department = reader.string();
                        break;
                    }
                case 6: {
                        message.phoneNumber = reader.string();
                        break;
                    }
                case 7: {
                        message.profileImageUrl = reader.string();
                        break;
                    }
                case 8: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 9: {
                        message.updatedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProfileProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof users.ProfileProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {users.ProfileProto} ProfileProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProfileProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProfileProto message.
         * @function verify
         * @memberof users.ProfileProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProfileProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.userId != null && message.hasOwnProperty("userId"))
                if (!$util.isString(message.userId))
                    return "userId: string expected";
            if (message.bio != null && message.hasOwnProperty("bio"))
                if (!$util.isString(message.bio))
                    return "bio: string expected";
            if (message.position != null && message.hasOwnProperty("position"))
                if (!$util.isString(message.position))
                    return "position: string expected";
            if (message.department != null && message.hasOwnProperty("department"))
                if (!$util.isString(message.department))
                    return "department: string expected";
            if (message.phoneNumber != null && message.hasOwnProperty("phoneNumber"))
                if (!$util.isString(message.phoneNumber))
                    return "phoneNumber: string expected";
            if (message.profileImageUrl != null && message.hasOwnProperty("profileImageUrl"))
                if (!$util.isString(message.profileImageUrl))
                    return "profileImageUrl: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isString(message.updatedAt))
                    return "updatedAt: string expected";
            return null;
        };

        /**
         * Creates a ProfileProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof users.ProfileProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {users.ProfileProto} ProfileProto
         */
        ProfileProto.fromObject = function fromObject(object) {
            if (object instanceof $root.users.ProfileProto)
                return object;
            var message = new $root.users.ProfileProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.userId != null)
                message.userId = String(object.userId);
            if (object.bio != null)
                message.bio = String(object.bio);
            if (object.position != null)
                message.position = String(object.position);
            if (object.department != null)
                message.department = String(object.department);
            if (object.phoneNumber != null)
                message.phoneNumber = String(object.phoneNumber);
            if (object.profileImageUrl != null)
                message.profileImageUrl = String(object.profileImageUrl);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.updatedAt != null)
                message.updatedAt = String(object.updatedAt);
            return message;
        };

        /**
         * Creates a plain object from a ProfileProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof users.ProfileProto
         * @static
         * @param {users.ProfileProto} message ProfileProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProfileProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.userId = "";
                object.bio = "";
                object.position = "";
                object.department = "";
                object.phoneNumber = "";
                object.profileImageUrl = "";
                object.createdAt = "";
                object.updatedAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.userId != null && message.hasOwnProperty("userId"))
                object.userId = message.userId;
            if (message.bio != null && message.hasOwnProperty("bio"))
                object.bio = message.bio;
            if (message.position != null && message.hasOwnProperty("position"))
                object.position = message.position;
            if (message.department != null && message.hasOwnProperty("department"))
                object.department = message.department;
            if (message.phoneNumber != null && message.hasOwnProperty("phoneNumber"))
                object.phoneNumber = message.phoneNumber;
            if (message.profileImageUrl != null && message.hasOwnProperty("profileImageUrl"))
                object.profileImageUrl = message.profileImageUrl;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                object.updatedAt = message.updatedAt;
            return object;
        };

        /**
         * Converts this ProfileProto to JSON.
         * @function toJSON
         * @memberof users.ProfileProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProfileProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProfileProto
         * @function getTypeUrl
         * @memberof users.ProfileProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProfileProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/users.ProfileProto";
        };

        return ProfileProto;
    })();

    users.UserCollection = (function() {

        /**
         * Properties of a UserCollection.
         * @memberof users
         * @interface IUserCollection
         * @property {Array.<users.IUserProto>|null} [users] UserCollection users
         */

        /**
         * Constructs a new UserCollection.
         * @memberof users
         * @classdesc Represents a UserCollection.
         * @implements IUserCollection
         * @constructor
         * @param {users.IUserCollection=} [properties] Properties to set
         */
        function UserCollection(properties) {
            this.users = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * UserCollection users.
         * @member {Array.<users.IUserProto>} users
         * @memberof users.UserCollection
         * @instance
         */
        UserCollection.prototype.users = $util.emptyArray;

        /**
         * Creates a new UserCollection instance using the specified properties.
         * @function create
         * @memberof users.UserCollection
         * @static
         * @param {users.IUserCollection=} [properties] Properties to set
         * @returns {users.UserCollection} UserCollection instance
         */
        UserCollection.create = function create(properties) {
            return new UserCollection(properties);
        };

        /**
         * Encodes the specified UserCollection message. Does not implicitly {@link users.UserCollection.verify|verify} messages.
         * @function encode
         * @memberof users.UserCollection
         * @static
         * @param {users.IUserCollection} message UserCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        UserCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.users != null && message.users.length)
                for (var i = 0; i < message.users.length; ++i)
                    $root.users.UserProto.encode(message.users[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified UserCollection message, length delimited. Does not implicitly {@link users.UserCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof users.UserCollection
         * @static
         * @param {users.IUserCollection} message UserCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        UserCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a UserCollection message from the specified reader or buffer.
         * @function decode
         * @memberof users.UserCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {users.UserCollection} UserCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        UserCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.users.UserCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.users && message.users.length))
                            message.users = [];
                        message.users.push($root.users.UserProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a UserCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof users.UserCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {users.UserCollection} UserCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        UserCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a UserCollection message.
         * @function verify
         * @memberof users.UserCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        UserCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.users != null && message.hasOwnProperty("users")) {
                if (!Array.isArray(message.users))
                    return "users: array expected";
                for (var i = 0; i < message.users.length; ++i) {
                    var error = $root.users.UserProto.verify(message.users[i]);
                    if (error)
                        return "users." + error;
                }
            }
            return null;
        };

        /**
         * Creates a UserCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof users.UserCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {users.UserCollection} UserCollection
         */
        UserCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.users.UserCollection)
                return object;
            var message = new $root.users.UserCollection();
            if (object.users) {
                if (!Array.isArray(object.users))
                    throw TypeError(".users.UserCollection.users: array expected");
                message.users = [];
                for (var i = 0; i < object.users.length; ++i) {
                    if (typeof object.users[i] !== "object")
                        throw TypeError(".users.UserCollection.users: object expected");
                    message.users[i] = $root.users.UserProto.fromObject(object.users[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a UserCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof users.UserCollection
         * @static
         * @param {users.UserCollection} message UserCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        UserCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.users = [];
            if (message.users && message.users.length) {
                object.users = [];
                for (var j = 0; j < message.users.length; ++j)
                    object.users[j] = $root.users.UserProto.toObject(message.users[j], options);
            }
            return object;
        };

        /**
         * Converts this UserCollection to JSON.
         * @function toJSON
         * @memberof users.UserCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        UserCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for UserCollection
         * @function getTypeUrl
         * @memberof users.UserCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        UserCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/users.UserCollection";
        };

        return UserCollection;
    })();

    users.ProfileCollection = (function() {

        /**
         * Properties of a ProfileCollection.
         * @memberof users
         * @interface IProfileCollection
         * @property {Array.<users.IProfileProto>|null} [profiles] ProfileCollection profiles
         */

        /**
         * Constructs a new ProfileCollection.
         * @memberof users
         * @classdesc Represents a ProfileCollection.
         * @implements IProfileCollection
         * @constructor
         * @param {users.IProfileCollection=} [properties] Properties to set
         */
        function ProfileCollection(properties) {
            this.profiles = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ProfileCollection profiles.
         * @member {Array.<users.IProfileProto>} profiles
         * @memberof users.ProfileCollection
         * @instance
         */
        ProfileCollection.prototype.profiles = $util.emptyArray;

        /**
         * Creates a new ProfileCollection instance using the specified properties.
         * @function create
         * @memberof users.ProfileCollection
         * @static
         * @param {users.IProfileCollection=} [properties] Properties to set
         * @returns {users.ProfileCollection} ProfileCollection instance
         */
        ProfileCollection.create = function create(properties) {
            return new ProfileCollection(properties);
        };

        /**
         * Encodes the specified ProfileCollection message. Does not implicitly {@link users.ProfileCollection.verify|verify} messages.
         * @function encode
         * @memberof users.ProfileCollection
         * @static
         * @param {users.IProfileCollection} message ProfileCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProfileCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.profiles != null && message.profiles.length)
                for (var i = 0; i < message.profiles.length; ++i)
                    $root.users.ProfileProto.encode(message.profiles[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ProfileCollection message, length delimited. Does not implicitly {@link users.ProfileCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof users.ProfileCollection
         * @static
         * @param {users.IProfileCollection} message ProfileCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ProfileCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ProfileCollection message from the specified reader or buffer.
         * @function decode
         * @memberof users.ProfileCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {users.ProfileCollection} ProfileCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProfileCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.users.ProfileCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.profiles && message.profiles.length))
                            message.profiles = [];
                        message.profiles.push($root.users.ProfileProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ProfileCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof users.ProfileCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {users.ProfileCollection} ProfileCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ProfileCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ProfileCollection message.
         * @function verify
         * @memberof users.ProfileCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ProfileCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.profiles != null && message.hasOwnProperty("profiles")) {
                if (!Array.isArray(message.profiles))
                    return "profiles: array expected";
                for (var i = 0; i < message.profiles.length; ++i) {
                    var error = $root.users.ProfileProto.verify(message.profiles[i]);
                    if (error)
                        return "profiles." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ProfileCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof users.ProfileCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {users.ProfileCollection} ProfileCollection
         */
        ProfileCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.users.ProfileCollection)
                return object;
            var message = new $root.users.ProfileCollection();
            if (object.profiles) {
                if (!Array.isArray(object.profiles))
                    throw TypeError(".users.ProfileCollection.profiles: array expected");
                message.profiles = [];
                for (var i = 0; i < object.profiles.length; ++i) {
                    if (typeof object.profiles[i] !== "object")
                        throw TypeError(".users.ProfileCollection.profiles: object expected");
                    message.profiles[i] = $root.users.ProfileProto.fromObject(object.profiles[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ProfileCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof users.ProfileCollection
         * @static
         * @param {users.ProfileCollection} message ProfileCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ProfileCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.profiles = [];
            if (message.profiles && message.profiles.length) {
                object.profiles = [];
                for (var j = 0; j < message.profiles.length; ++j)
                    object.profiles[j] = $root.users.ProfileProto.toObject(message.profiles[j], options);
            }
            return object;
        };

        /**
         * Converts this ProfileCollection to JSON.
         * @function toJSON
         * @memberof users.ProfileCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ProfileCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ProfileCollection
         * @function getTypeUrl
         * @memberof users.ProfileCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ProfileCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/users.ProfileCollection";
        };

        return ProfileCollection;
    })();

    return users;
})();

$root.auditing = (function() {

    /**
     * Namespace auditing.
     * @exports auditing
     * @namespace
     */
    var auditing = {};

    auditing.MitigationProto = (function() {

        /**
         * Properties of a MitigationProto.
         * @memberof auditing
         * @interface IMitigationProto
         * @property {string|null} [id] MitigationProto id
         * @property {string|null} [auditEntryId] MitigationProto auditEntryId
         * @property {string|null} [description] MitigationProto description
         * @property {string|null} [status] MitigationProto status
         * @property {string|null} [createdAt] MitigationProto createdAt
         */

        /**
         * Constructs a new MitigationProto.
         * @memberof auditing
         * @classdesc Represents a MitigationProto.
         * @implements IMitigationProto
         * @constructor
         * @param {auditing.IMitigationProto=} [properties] Properties to set
         */
        function MitigationProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * MitigationProto id.
         * @member {string} id
         * @memberof auditing.MitigationProto
         * @instance
         */
        MitigationProto.prototype.id = "";

        /**
         * MitigationProto auditEntryId.
         * @member {string} auditEntryId
         * @memberof auditing.MitigationProto
         * @instance
         */
        MitigationProto.prototype.auditEntryId = "";

        /**
         * MitigationProto description.
         * @member {string} description
         * @memberof auditing.MitigationProto
         * @instance
         */
        MitigationProto.prototype.description = "";

        /**
         * MitigationProto status.
         * @member {string} status
         * @memberof auditing.MitigationProto
         * @instance
         */
        MitigationProto.prototype.status = "";

        /**
         * MitigationProto createdAt.
         * @member {string} createdAt
         * @memberof auditing.MitigationProto
         * @instance
         */
        MitigationProto.prototype.createdAt = "";

        /**
         * Creates a new MitigationProto instance using the specified properties.
         * @function create
         * @memberof auditing.MitigationProto
         * @static
         * @param {auditing.IMitigationProto=} [properties] Properties to set
         * @returns {auditing.MitigationProto} MitigationProto instance
         */
        MitigationProto.create = function create(properties) {
            return new MitigationProto(properties);
        };

        /**
         * Encodes the specified MitigationProto message. Does not implicitly {@link auditing.MitigationProto.verify|verify} messages.
         * @function encode
         * @memberof auditing.MitigationProto
         * @static
         * @param {auditing.IMitigationProto} message MitigationProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        MitigationProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.auditEntryId != null && Object.hasOwnProperty.call(message, "auditEntryId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.auditEntryId);
            if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.description);
            if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.status);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.createdAt);
            return writer;
        };

        /**
         * Encodes the specified MitigationProto message, length delimited. Does not implicitly {@link auditing.MitigationProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.MitigationProto
         * @static
         * @param {auditing.IMitigationProto} message MitigationProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        MitigationProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a MitigationProto message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.MitigationProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.MitigationProto} MitigationProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        MitigationProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.MitigationProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.auditEntryId = reader.string();
                        break;
                    }
                case 3: {
                        message.description = reader.string();
                        break;
                    }
                case 4: {
                        message.status = reader.string();
                        break;
                    }
                case 5: {
                        message.createdAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a MitigationProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.MitigationProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.MitigationProto} MitigationProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        MitigationProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a MitigationProto message.
         * @function verify
         * @memberof auditing.MitigationProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        MitigationProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.auditEntryId != null && message.hasOwnProperty("auditEntryId"))
                if (!$util.isString(message.auditEntryId))
                    return "auditEntryId: string expected";
            if (message.description != null && message.hasOwnProperty("description"))
                if (!$util.isString(message.description))
                    return "description: string expected";
            if (message.status != null && message.hasOwnProperty("status"))
                if (!$util.isString(message.status))
                    return "status: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            return null;
        };

        /**
         * Creates a MitigationProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.MitigationProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.MitigationProto} MitigationProto
         */
        MitigationProto.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.MitigationProto)
                return object;
            var message = new $root.auditing.MitigationProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.auditEntryId != null)
                message.auditEntryId = String(object.auditEntryId);
            if (object.description != null)
                message.description = String(object.description);
            if (object.status != null)
                message.status = String(object.status);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            return message;
        };

        /**
         * Creates a plain object from a MitigationProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.MitigationProto
         * @static
         * @param {auditing.MitigationProto} message MitigationProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        MitigationProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.auditEntryId = "";
                object.description = "";
                object.status = "";
                object.createdAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.auditEntryId != null && message.hasOwnProperty("auditEntryId"))
                object.auditEntryId = message.auditEntryId;
            if (message.description != null && message.hasOwnProperty("description"))
                object.description = message.description;
            if (message.status != null && message.hasOwnProperty("status"))
                object.status = message.status;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            return object;
        };

        /**
         * Converts this MitigationProto to JSON.
         * @function toJSON
         * @memberof auditing.MitigationProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        MitigationProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for MitigationProto
         * @function getTypeUrl
         * @memberof auditing.MitigationProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        MitigationProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.MitigationProto";
        };

        return MitigationProto;
    })();

    auditing.CorrectiveActionProto = (function() {

        /**
         * Properties of a CorrectiveActionProto.
         * @memberof auditing
         * @interface ICorrectiveActionProto
         * @property {string|null} [id] CorrectiveActionProto id
         * @property {string|null} [mitigationId] CorrectiveActionProto mitigationId
         * @property {string|null} [task] CorrectiveActionProto task
         * @property {string|null} [status] CorrectiveActionProto status
         * @property {string|null} [assignedToUserId] CorrectiveActionProto assignedToUserId
         * @property {string|null} [createdAt] CorrectiveActionProto createdAt
         * @property {string|null} [dueDate] CorrectiveActionProto dueDate
         */

        /**
         * Constructs a new CorrectiveActionProto.
         * @memberof auditing
         * @classdesc Represents a CorrectiveActionProto.
         * @implements ICorrectiveActionProto
         * @constructor
         * @param {auditing.ICorrectiveActionProto=} [properties] Properties to set
         */
        function CorrectiveActionProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CorrectiveActionProto id.
         * @member {string} id
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.id = "";

        /**
         * CorrectiveActionProto mitigationId.
         * @member {string} mitigationId
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.mitigationId = "";

        /**
         * CorrectiveActionProto task.
         * @member {string} task
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.task = "";

        /**
         * CorrectiveActionProto status.
         * @member {string} status
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.status = "";

        /**
         * CorrectiveActionProto assignedToUserId.
         * @member {string} assignedToUserId
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.assignedToUserId = "";

        /**
         * CorrectiveActionProto createdAt.
         * @member {string} createdAt
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.createdAt = "";

        /**
         * CorrectiveActionProto dueDate.
         * @member {string} dueDate
         * @memberof auditing.CorrectiveActionProto
         * @instance
         */
        CorrectiveActionProto.prototype.dueDate = "";

        /**
         * Creates a new CorrectiveActionProto instance using the specified properties.
         * @function create
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {auditing.ICorrectiveActionProto=} [properties] Properties to set
         * @returns {auditing.CorrectiveActionProto} CorrectiveActionProto instance
         */
        CorrectiveActionProto.create = function create(properties) {
            return new CorrectiveActionProto(properties);
        };

        /**
         * Encodes the specified CorrectiveActionProto message. Does not implicitly {@link auditing.CorrectiveActionProto.verify|verify} messages.
         * @function encode
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {auditing.ICorrectiveActionProto} message CorrectiveActionProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CorrectiveActionProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.mitigationId != null && Object.hasOwnProperty.call(message, "mitigationId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.mitigationId);
            if (message.task != null && Object.hasOwnProperty.call(message, "task"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.task);
            if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.status);
            if (message.assignedToUserId != null && Object.hasOwnProperty.call(message, "assignedToUserId"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.assignedToUserId);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.createdAt);
            if (message.dueDate != null && Object.hasOwnProperty.call(message, "dueDate"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.dueDate);
            return writer;
        };

        /**
         * Encodes the specified CorrectiveActionProto message, length delimited. Does not implicitly {@link auditing.CorrectiveActionProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {auditing.ICorrectiveActionProto} message CorrectiveActionProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CorrectiveActionProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CorrectiveActionProto message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.CorrectiveActionProto} CorrectiveActionProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CorrectiveActionProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.CorrectiveActionProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.mitigationId = reader.string();
                        break;
                    }
                case 3: {
                        message.task = reader.string();
                        break;
                    }
                case 4: {
                        message.status = reader.string();
                        break;
                    }
                case 5: {
                        message.assignedToUserId = reader.string();
                        break;
                    }
                case 6: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 7: {
                        message.dueDate = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CorrectiveActionProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.CorrectiveActionProto} CorrectiveActionProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CorrectiveActionProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CorrectiveActionProto message.
         * @function verify
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CorrectiveActionProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.mitigationId != null && message.hasOwnProperty("mitigationId"))
                if (!$util.isString(message.mitigationId))
                    return "mitigationId: string expected";
            if (message.task != null && message.hasOwnProperty("task"))
                if (!$util.isString(message.task))
                    return "task: string expected";
            if (message.status != null && message.hasOwnProperty("status"))
                if (!$util.isString(message.status))
                    return "status: string expected";
            if (message.assignedToUserId != null && message.hasOwnProperty("assignedToUserId"))
                if (!$util.isString(message.assignedToUserId))
                    return "assignedToUserId: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.dueDate != null && message.hasOwnProperty("dueDate"))
                if (!$util.isString(message.dueDate))
                    return "dueDate: string expected";
            return null;
        };

        /**
         * Creates a CorrectiveActionProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.CorrectiveActionProto} CorrectiveActionProto
         */
        CorrectiveActionProto.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.CorrectiveActionProto)
                return object;
            var message = new $root.auditing.CorrectiveActionProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.mitigationId != null)
                message.mitigationId = String(object.mitigationId);
            if (object.task != null)
                message.task = String(object.task);
            if (object.status != null)
                message.status = String(object.status);
            if (object.assignedToUserId != null)
                message.assignedToUserId = String(object.assignedToUserId);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.dueDate != null)
                message.dueDate = String(object.dueDate);
            return message;
        };

        /**
         * Creates a plain object from a CorrectiveActionProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {auditing.CorrectiveActionProto} message CorrectiveActionProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CorrectiveActionProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.mitigationId = "";
                object.task = "";
                object.status = "";
                object.assignedToUserId = "";
                object.createdAt = "";
                object.dueDate = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.mitigationId != null && message.hasOwnProperty("mitigationId"))
                object.mitigationId = message.mitigationId;
            if (message.task != null && message.hasOwnProperty("task"))
                object.task = message.task;
            if (message.status != null && message.hasOwnProperty("status"))
                object.status = message.status;
            if (message.assignedToUserId != null && message.hasOwnProperty("assignedToUserId"))
                object.assignedToUserId = message.assignedToUserId;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.dueDate != null && message.hasOwnProperty("dueDate"))
                object.dueDate = message.dueDate;
            return object;
        };

        /**
         * Converts this CorrectiveActionProto to JSON.
         * @function toJSON
         * @memberof auditing.CorrectiveActionProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CorrectiveActionProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CorrectiveActionProto
         * @function getTypeUrl
         * @memberof auditing.CorrectiveActionProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CorrectiveActionProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.CorrectiveActionProto";
        };

        return CorrectiveActionProto;
    })();

    auditing.AuditProto = (function() {

        /**
         * Properties of an AuditProto.
         * @memberof auditing
         * @interface IAuditProto
         * @property {string|null} [id] AuditProto id
         * @property {string|null} [name] AuditProto name
         * @property {string|null} [createdAt] AuditProto createdAt
         * @property {Array.<string>|null} [mechanismIds] AuditProto mechanismIds
         */

        /**
         * Constructs a new AuditProto.
         * @memberof auditing
         * @classdesc Represents an AuditProto.
         * @implements IAuditProto
         * @constructor
         * @param {auditing.IAuditProto=} [properties] Properties to set
         */
        function AuditProto(properties) {
            this.mechanismIds = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AuditProto id.
         * @member {string} id
         * @memberof auditing.AuditProto
         * @instance
         */
        AuditProto.prototype.id = "";

        /**
         * AuditProto name.
         * @member {string} name
         * @memberof auditing.AuditProto
         * @instance
         */
        AuditProto.prototype.name = "";

        /**
         * AuditProto createdAt.
         * @member {string} createdAt
         * @memberof auditing.AuditProto
         * @instance
         */
        AuditProto.prototype.createdAt = "";

        /**
         * AuditProto mechanismIds.
         * @member {Array.<string>} mechanismIds
         * @memberof auditing.AuditProto
         * @instance
         */
        AuditProto.prototype.mechanismIds = $util.emptyArray;

        /**
         * Creates a new AuditProto instance using the specified properties.
         * @function create
         * @memberof auditing.AuditProto
         * @static
         * @param {auditing.IAuditProto=} [properties] Properties to set
         * @returns {auditing.AuditProto} AuditProto instance
         */
        AuditProto.create = function create(properties) {
            return new AuditProto(properties);
        };

        /**
         * Encodes the specified AuditProto message. Does not implicitly {@link auditing.AuditProto.verify|verify} messages.
         * @function encode
         * @memberof auditing.AuditProto
         * @static
         * @param {auditing.IAuditProto} message AuditProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.createdAt);
            if (message.mechanismIds != null && message.mechanismIds.length)
                for (var i = 0; i < message.mechanismIds.length; ++i)
                    writer.uint32(/* id 4, wireType 2 =*/34).string(message.mechanismIds[i]);
            return writer;
        };

        /**
         * Encodes the specified AuditProto message, length delimited. Does not implicitly {@link auditing.AuditProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.AuditProto
         * @static
         * @param {auditing.IAuditProto} message AuditProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AuditProto message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.AuditProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.AuditProto} AuditProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.AuditProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 4: {
                        if (!(message.mechanismIds && message.mechanismIds.length))
                            message.mechanismIds = [];
                        message.mechanismIds.push(reader.string());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AuditProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.AuditProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.AuditProto} AuditProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AuditProto message.
         * @function verify
         * @memberof auditing.AuditProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AuditProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.mechanismIds != null && message.hasOwnProperty("mechanismIds")) {
                if (!Array.isArray(message.mechanismIds))
                    return "mechanismIds: array expected";
                for (var i = 0; i < message.mechanismIds.length; ++i)
                    if (!$util.isString(message.mechanismIds[i]))
                        return "mechanismIds: string[] expected";
            }
            return null;
        };

        /**
         * Creates an AuditProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.AuditProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.AuditProto} AuditProto
         */
        AuditProto.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.AuditProto)
                return object;
            var message = new $root.auditing.AuditProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.name != null)
                message.name = String(object.name);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.mechanismIds) {
                if (!Array.isArray(object.mechanismIds))
                    throw TypeError(".auditing.AuditProto.mechanismIds: array expected");
                message.mechanismIds = [];
                for (var i = 0; i < object.mechanismIds.length; ++i)
                    message.mechanismIds[i] = String(object.mechanismIds[i]);
            }
            return message;
        };

        /**
         * Creates a plain object from an AuditProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.AuditProto
         * @static
         * @param {auditing.AuditProto} message AuditProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AuditProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.mechanismIds = [];
            if (options.defaults) {
                object.id = "";
                object.name = "";
                object.createdAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.mechanismIds && message.mechanismIds.length) {
                object.mechanismIds = [];
                for (var j = 0; j < message.mechanismIds.length; ++j)
                    object.mechanismIds[j] = message.mechanismIds[j];
            }
            return object;
        };

        /**
         * Converts this AuditProto to JSON.
         * @function toJSON
         * @memberof auditing.AuditProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AuditProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AuditProto
         * @function getTypeUrl
         * @memberof auditing.AuditProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AuditProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.AuditProto";
        };

        return AuditProto;
    })();

    auditing.AuditEntryProto = (function() {

        /**
         * Properties of an AuditEntryProto.
         * @memberof auditing
         * @interface IAuditEntryProto
         * @property {string|null} [id] AuditEntryProto id
         * @property {string|null} [auditId] AuditEntryProto auditId
         * @property {string|null} [obligationId] AuditEntryProto obligationId
         * @property {string|null} [status] AuditEntryProto status
         * @property {string|null} [finding] AuditEntryProto finding
         */

        /**
         * Constructs a new AuditEntryProto.
         * @memberof auditing
         * @classdesc Represents an AuditEntryProto.
         * @implements IAuditEntryProto
         * @constructor
         * @param {auditing.IAuditEntryProto=} [properties] Properties to set
         */
        function AuditEntryProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AuditEntryProto id.
         * @member {string} id
         * @memberof auditing.AuditEntryProto
         * @instance
         */
        AuditEntryProto.prototype.id = "";

        /**
         * AuditEntryProto auditId.
         * @member {string} auditId
         * @memberof auditing.AuditEntryProto
         * @instance
         */
        AuditEntryProto.prototype.auditId = "";

        /**
         * AuditEntryProto obligationId.
         * @member {string} obligationId
         * @memberof auditing.AuditEntryProto
         * @instance
         */
        AuditEntryProto.prototype.obligationId = "";

        /**
         * AuditEntryProto status.
         * @member {string} status
         * @memberof auditing.AuditEntryProto
         * @instance
         */
        AuditEntryProto.prototype.status = "";

        /**
         * AuditEntryProto finding.
         * @member {string} finding
         * @memberof auditing.AuditEntryProto
         * @instance
         */
        AuditEntryProto.prototype.finding = "";

        /**
         * Creates a new AuditEntryProto instance using the specified properties.
         * @function create
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {auditing.IAuditEntryProto=} [properties] Properties to set
         * @returns {auditing.AuditEntryProto} AuditEntryProto instance
         */
        AuditEntryProto.create = function create(properties) {
            return new AuditEntryProto(properties);
        };

        /**
         * Encodes the specified AuditEntryProto message. Does not implicitly {@link auditing.AuditEntryProto.verify|verify} messages.
         * @function encode
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {auditing.IAuditEntryProto} message AuditEntryProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditEntryProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.auditId != null && Object.hasOwnProperty.call(message, "auditId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.auditId);
            if (message.obligationId != null && Object.hasOwnProperty.call(message, "obligationId"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.obligationId);
            if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.status);
            if (message.finding != null && Object.hasOwnProperty.call(message, "finding"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.finding);
            return writer;
        };

        /**
         * Encodes the specified AuditEntryProto message, length delimited. Does not implicitly {@link auditing.AuditEntryProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {auditing.IAuditEntryProto} message AuditEntryProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditEntryProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AuditEntryProto message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.AuditEntryProto} AuditEntryProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditEntryProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.AuditEntryProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.auditId = reader.string();
                        break;
                    }
                case 3: {
                        message.obligationId = reader.string();
                        break;
                    }
                case 4: {
                        message.status = reader.string();
                        break;
                    }
                case 5: {
                        message.finding = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AuditEntryProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.AuditEntryProto} AuditEntryProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditEntryProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AuditEntryProto message.
         * @function verify
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AuditEntryProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.auditId != null && message.hasOwnProperty("auditId"))
                if (!$util.isString(message.auditId))
                    return "auditId: string expected";
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                if (!$util.isString(message.obligationId))
                    return "obligationId: string expected";
            if (message.status != null && message.hasOwnProperty("status"))
                if (!$util.isString(message.status))
                    return "status: string expected";
            if (message.finding != null && message.hasOwnProperty("finding"))
                if (!$util.isString(message.finding))
                    return "finding: string expected";
            return null;
        };

        /**
         * Creates an AuditEntryProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.AuditEntryProto} AuditEntryProto
         */
        AuditEntryProto.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.AuditEntryProto)
                return object;
            var message = new $root.auditing.AuditEntryProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.auditId != null)
                message.auditId = String(object.auditId);
            if (object.obligationId != null)
                message.obligationId = String(object.obligationId);
            if (object.status != null)
                message.status = String(object.status);
            if (object.finding != null)
                message.finding = String(object.finding);
            return message;
        };

        /**
         * Creates a plain object from an AuditEntryProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {auditing.AuditEntryProto} message AuditEntryProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AuditEntryProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.auditId = "";
                object.obligationId = "";
                object.status = "";
                object.finding = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.auditId != null && message.hasOwnProperty("auditId"))
                object.auditId = message.auditId;
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                object.obligationId = message.obligationId;
            if (message.status != null && message.hasOwnProperty("status"))
                object.status = message.status;
            if (message.finding != null && message.hasOwnProperty("finding"))
                object.finding = message.finding;
            return object;
        };

        /**
         * Converts this AuditEntryProto to JSON.
         * @function toJSON
         * @memberof auditing.AuditEntryProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AuditEntryProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AuditEntryProto
         * @function getTypeUrl
         * @memberof auditing.AuditEntryProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AuditEntryProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.AuditEntryProto";
        };

        return AuditEntryProto;
    })();

    auditing.ComplianceCommentProto = (function() {

        /**
         * Properties of a ComplianceCommentProto.
         * @memberof auditing
         * @interface IComplianceCommentProto
         * @property {string|null} [id] ComplianceCommentProto id
         * @property {string|null} [obligationId] ComplianceCommentProto obligationId
         * @property {string|null} [text] ComplianceCommentProto text
         * @property {string|null} [createdAt] ComplianceCommentProto createdAt
         */

        /**
         * Constructs a new ComplianceCommentProto.
         * @memberof auditing
         * @classdesc Represents a ComplianceCommentProto.
         * @implements IComplianceCommentProto
         * @constructor
         * @param {auditing.IComplianceCommentProto=} [properties] Properties to set
         */
        function ComplianceCommentProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ComplianceCommentProto id.
         * @member {string} id
         * @memberof auditing.ComplianceCommentProto
         * @instance
         */
        ComplianceCommentProto.prototype.id = "";

        /**
         * ComplianceCommentProto obligationId.
         * @member {string} obligationId
         * @memberof auditing.ComplianceCommentProto
         * @instance
         */
        ComplianceCommentProto.prototype.obligationId = "";

        /**
         * ComplianceCommentProto text.
         * @member {string} text
         * @memberof auditing.ComplianceCommentProto
         * @instance
         */
        ComplianceCommentProto.prototype.text = "";

        /**
         * ComplianceCommentProto createdAt.
         * @member {string} createdAt
         * @memberof auditing.ComplianceCommentProto
         * @instance
         */
        ComplianceCommentProto.prototype.createdAt = "";

        /**
         * Creates a new ComplianceCommentProto instance using the specified properties.
         * @function create
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {auditing.IComplianceCommentProto=} [properties] Properties to set
         * @returns {auditing.ComplianceCommentProto} ComplianceCommentProto instance
         */
        ComplianceCommentProto.create = function create(properties) {
            return new ComplianceCommentProto(properties);
        };

        /**
         * Encodes the specified ComplianceCommentProto message. Does not implicitly {@link auditing.ComplianceCommentProto.verify|verify} messages.
         * @function encode
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {auditing.IComplianceCommentProto} message ComplianceCommentProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ComplianceCommentProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.obligationId != null && Object.hasOwnProperty.call(message, "obligationId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.obligationId);
            if (message.text != null && Object.hasOwnProperty.call(message, "text"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.text);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.createdAt);
            return writer;
        };

        /**
         * Encodes the specified ComplianceCommentProto message, length delimited. Does not implicitly {@link auditing.ComplianceCommentProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {auditing.IComplianceCommentProto} message ComplianceCommentProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ComplianceCommentProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ComplianceCommentProto message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.ComplianceCommentProto} ComplianceCommentProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ComplianceCommentProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.ComplianceCommentProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.obligationId = reader.string();
                        break;
                    }
                case 3: {
                        message.text = reader.string();
                        break;
                    }
                case 4: {
                        message.createdAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ComplianceCommentProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.ComplianceCommentProto} ComplianceCommentProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ComplianceCommentProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ComplianceCommentProto message.
         * @function verify
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ComplianceCommentProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                if (!$util.isString(message.obligationId))
                    return "obligationId: string expected";
            if (message.text != null && message.hasOwnProperty("text"))
                if (!$util.isString(message.text))
                    return "text: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            return null;
        };

        /**
         * Creates a ComplianceCommentProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.ComplianceCommentProto} ComplianceCommentProto
         */
        ComplianceCommentProto.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.ComplianceCommentProto)
                return object;
            var message = new $root.auditing.ComplianceCommentProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.obligationId != null)
                message.obligationId = String(object.obligationId);
            if (object.text != null)
                message.text = String(object.text);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            return message;
        };

        /**
         * Creates a plain object from a ComplianceCommentProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {auditing.ComplianceCommentProto} message ComplianceCommentProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ComplianceCommentProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.obligationId = "";
                object.text = "";
                object.createdAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                object.obligationId = message.obligationId;
            if (message.text != null && message.hasOwnProperty("text"))
                object.text = message.text;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            return object;
        };

        /**
         * Converts this ComplianceCommentProto to JSON.
         * @function toJSON
         * @memberof auditing.ComplianceCommentProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ComplianceCommentProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ComplianceCommentProto
         * @function getTypeUrl
         * @memberof auditing.ComplianceCommentProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ComplianceCommentProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.ComplianceCommentProto";
        };

        return ComplianceCommentProto;
    })();

    auditing.NonConformanceCommentProto = (function() {

        /**
         * Properties of a NonConformanceCommentProto.
         * @memberof auditing
         * @interface INonConformanceCommentProto
         * @property {string|null} [id] NonConformanceCommentProto id
         * @property {string|null} [obligationId] NonConformanceCommentProto obligationId
         * @property {string|null} [text] NonConformanceCommentProto text
         * @property {string|null} [createdAt] NonConformanceCommentProto createdAt
         */

        /**
         * Constructs a new NonConformanceCommentProto.
         * @memberof auditing
         * @classdesc Represents a NonConformanceCommentProto.
         * @implements INonConformanceCommentProto
         * @constructor
         * @param {auditing.INonConformanceCommentProto=} [properties] Properties to set
         */
        function NonConformanceCommentProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NonConformanceCommentProto id.
         * @member {string} id
         * @memberof auditing.NonConformanceCommentProto
         * @instance
         */
        NonConformanceCommentProto.prototype.id = "";

        /**
         * NonConformanceCommentProto obligationId.
         * @member {string} obligationId
         * @memberof auditing.NonConformanceCommentProto
         * @instance
         */
        NonConformanceCommentProto.prototype.obligationId = "";

        /**
         * NonConformanceCommentProto text.
         * @member {string} text
         * @memberof auditing.NonConformanceCommentProto
         * @instance
         */
        NonConformanceCommentProto.prototype.text = "";

        /**
         * NonConformanceCommentProto createdAt.
         * @member {string} createdAt
         * @memberof auditing.NonConformanceCommentProto
         * @instance
         */
        NonConformanceCommentProto.prototype.createdAt = "";

        /**
         * Creates a new NonConformanceCommentProto instance using the specified properties.
         * @function create
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {auditing.INonConformanceCommentProto=} [properties] Properties to set
         * @returns {auditing.NonConformanceCommentProto} NonConformanceCommentProto instance
         */
        NonConformanceCommentProto.create = function create(properties) {
            return new NonConformanceCommentProto(properties);
        };

        /**
         * Encodes the specified NonConformanceCommentProto message. Does not implicitly {@link auditing.NonConformanceCommentProto.verify|verify} messages.
         * @function encode
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {auditing.INonConformanceCommentProto} message NonConformanceCommentProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NonConformanceCommentProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.obligationId != null && Object.hasOwnProperty.call(message, "obligationId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.obligationId);
            if (message.text != null && Object.hasOwnProperty.call(message, "text"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.text);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.createdAt);
            return writer;
        };

        /**
         * Encodes the specified NonConformanceCommentProto message, length delimited. Does not implicitly {@link auditing.NonConformanceCommentProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {auditing.INonConformanceCommentProto} message NonConformanceCommentProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NonConformanceCommentProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NonConformanceCommentProto message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.NonConformanceCommentProto} NonConformanceCommentProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NonConformanceCommentProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.NonConformanceCommentProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.obligationId = reader.string();
                        break;
                    }
                case 3: {
                        message.text = reader.string();
                        break;
                    }
                case 4: {
                        message.createdAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NonConformanceCommentProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.NonConformanceCommentProto} NonConformanceCommentProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NonConformanceCommentProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NonConformanceCommentProto message.
         * @function verify
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NonConformanceCommentProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                if (!$util.isString(message.obligationId))
                    return "obligationId: string expected";
            if (message.text != null && message.hasOwnProperty("text"))
                if (!$util.isString(message.text))
                    return "text: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            return null;
        };

        /**
         * Creates a NonConformanceCommentProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.NonConformanceCommentProto} NonConformanceCommentProto
         */
        NonConformanceCommentProto.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.NonConformanceCommentProto)
                return object;
            var message = new $root.auditing.NonConformanceCommentProto();
            if (object.id != null)
                message.id = String(object.id);
            if (object.obligationId != null)
                message.obligationId = String(object.obligationId);
            if (object.text != null)
                message.text = String(object.text);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            return message;
        };

        /**
         * Creates a plain object from a NonConformanceCommentProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {auditing.NonConformanceCommentProto} message NonConformanceCommentProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NonConformanceCommentProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = "";
                object.obligationId = "";
                object.text = "";
                object.createdAt = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.obligationId != null && message.hasOwnProperty("obligationId"))
                object.obligationId = message.obligationId;
            if (message.text != null && message.hasOwnProperty("text"))
                object.text = message.text;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            return object;
        };

        /**
         * Converts this NonConformanceCommentProto to JSON.
         * @function toJSON
         * @memberof auditing.NonConformanceCommentProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NonConformanceCommentProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NonConformanceCommentProto
         * @function getTypeUrl
         * @memberof auditing.NonConformanceCommentProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NonConformanceCommentProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.NonConformanceCommentProto";
        };

        return NonConformanceCommentProto;
    })();

    auditing.MitigationCollection = (function() {

        /**
         * Properties of a MitigationCollection.
         * @memberof auditing
         * @interface IMitigationCollection
         * @property {Array.<auditing.IMitigationProto>|null} [mitigations] MitigationCollection mitigations
         */

        /**
         * Constructs a new MitigationCollection.
         * @memberof auditing
         * @classdesc Represents a MitigationCollection.
         * @implements IMitigationCollection
         * @constructor
         * @param {auditing.IMitigationCollection=} [properties] Properties to set
         */
        function MitigationCollection(properties) {
            this.mitigations = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * MitigationCollection mitigations.
         * @member {Array.<auditing.IMitigationProto>} mitigations
         * @memberof auditing.MitigationCollection
         * @instance
         */
        MitigationCollection.prototype.mitigations = $util.emptyArray;

        /**
         * Creates a new MitigationCollection instance using the specified properties.
         * @function create
         * @memberof auditing.MitigationCollection
         * @static
         * @param {auditing.IMitigationCollection=} [properties] Properties to set
         * @returns {auditing.MitigationCollection} MitigationCollection instance
         */
        MitigationCollection.create = function create(properties) {
            return new MitigationCollection(properties);
        };

        /**
         * Encodes the specified MitigationCollection message. Does not implicitly {@link auditing.MitigationCollection.verify|verify} messages.
         * @function encode
         * @memberof auditing.MitigationCollection
         * @static
         * @param {auditing.IMitigationCollection} message MitigationCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        MitigationCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.mitigations != null && message.mitigations.length)
                for (var i = 0; i < message.mitigations.length; ++i)
                    $root.auditing.MitigationProto.encode(message.mitigations[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified MitigationCollection message, length delimited. Does not implicitly {@link auditing.MitigationCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.MitigationCollection
         * @static
         * @param {auditing.IMitigationCollection} message MitigationCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        MitigationCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a MitigationCollection message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.MitigationCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.MitigationCollection} MitigationCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        MitigationCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.MitigationCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.mitigations && message.mitigations.length))
                            message.mitigations = [];
                        message.mitigations.push($root.auditing.MitigationProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a MitigationCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.MitigationCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.MitigationCollection} MitigationCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        MitigationCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a MitigationCollection message.
         * @function verify
         * @memberof auditing.MitigationCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        MitigationCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.mitigations != null && message.hasOwnProperty("mitigations")) {
                if (!Array.isArray(message.mitigations))
                    return "mitigations: array expected";
                for (var i = 0; i < message.mitigations.length; ++i) {
                    var error = $root.auditing.MitigationProto.verify(message.mitigations[i]);
                    if (error)
                        return "mitigations." + error;
                }
            }
            return null;
        };

        /**
         * Creates a MitigationCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.MitigationCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.MitigationCollection} MitigationCollection
         */
        MitigationCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.MitigationCollection)
                return object;
            var message = new $root.auditing.MitigationCollection();
            if (object.mitigations) {
                if (!Array.isArray(object.mitigations))
                    throw TypeError(".auditing.MitigationCollection.mitigations: array expected");
                message.mitigations = [];
                for (var i = 0; i < object.mitigations.length; ++i) {
                    if (typeof object.mitigations[i] !== "object")
                        throw TypeError(".auditing.MitigationCollection.mitigations: object expected");
                    message.mitigations[i] = $root.auditing.MitigationProto.fromObject(object.mitigations[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a MitigationCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.MitigationCollection
         * @static
         * @param {auditing.MitigationCollection} message MitigationCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        MitigationCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.mitigations = [];
            if (message.mitigations && message.mitigations.length) {
                object.mitigations = [];
                for (var j = 0; j < message.mitigations.length; ++j)
                    object.mitigations[j] = $root.auditing.MitigationProto.toObject(message.mitigations[j], options);
            }
            return object;
        };

        /**
         * Converts this MitigationCollection to JSON.
         * @function toJSON
         * @memberof auditing.MitigationCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        MitigationCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for MitigationCollection
         * @function getTypeUrl
         * @memberof auditing.MitigationCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        MitigationCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.MitigationCollection";
        };

        return MitigationCollection;
    })();

    auditing.CorrectiveActionCollection = (function() {

        /**
         * Properties of a CorrectiveActionCollection.
         * @memberof auditing
         * @interface ICorrectiveActionCollection
         * @property {Array.<auditing.ICorrectiveActionProto>|null} [correctiveActions] CorrectiveActionCollection correctiveActions
         */

        /**
         * Constructs a new CorrectiveActionCollection.
         * @memberof auditing
         * @classdesc Represents a CorrectiveActionCollection.
         * @implements ICorrectiveActionCollection
         * @constructor
         * @param {auditing.ICorrectiveActionCollection=} [properties] Properties to set
         */
        function CorrectiveActionCollection(properties) {
            this.correctiveActions = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CorrectiveActionCollection correctiveActions.
         * @member {Array.<auditing.ICorrectiveActionProto>} correctiveActions
         * @memberof auditing.CorrectiveActionCollection
         * @instance
         */
        CorrectiveActionCollection.prototype.correctiveActions = $util.emptyArray;

        /**
         * Creates a new CorrectiveActionCollection instance using the specified properties.
         * @function create
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {auditing.ICorrectiveActionCollection=} [properties] Properties to set
         * @returns {auditing.CorrectiveActionCollection} CorrectiveActionCollection instance
         */
        CorrectiveActionCollection.create = function create(properties) {
            return new CorrectiveActionCollection(properties);
        };

        /**
         * Encodes the specified CorrectiveActionCollection message. Does not implicitly {@link auditing.CorrectiveActionCollection.verify|verify} messages.
         * @function encode
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {auditing.ICorrectiveActionCollection} message CorrectiveActionCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CorrectiveActionCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.correctiveActions != null && message.correctiveActions.length)
                for (var i = 0; i < message.correctiveActions.length; ++i)
                    $root.auditing.CorrectiveActionProto.encode(message.correctiveActions[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified CorrectiveActionCollection message, length delimited. Does not implicitly {@link auditing.CorrectiveActionCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {auditing.ICorrectiveActionCollection} message CorrectiveActionCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CorrectiveActionCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CorrectiveActionCollection message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.CorrectiveActionCollection} CorrectiveActionCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CorrectiveActionCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.CorrectiveActionCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.correctiveActions && message.correctiveActions.length))
                            message.correctiveActions = [];
                        message.correctiveActions.push($root.auditing.CorrectiveActionProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CorrectiveActionCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.CorrectiveActionCollection} CorrectiveActionCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CorrectiveActionCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CorrectiveActionCollection message.
         * @function verify
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CorrectiveActionCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.correctiveActions != null && message.hasOwnProperty("correctiveActions")) {
                if (!Array.isArray(message.correctiveActions))
                    return "correctiveActions: array expected";
                for (var i = 0; i < message.correctiveActions.length; ++i) {
                    var error = $root.auditing.CorrectiveActionProto.verify(message.correctiveActions[i]);
                    if (error)
                        return "correctiveActions." + error;
                }
            }
            return null;
        };

        /**
         * Creates a CorrectiveActionCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.CorrectiveActionCollection} CorrectiveActionCollection
         */
        CorrectiveActionCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.CorrectiveActionCollection)
                return object;
            var message = new $root.auditing.CorrectiveActionCollection();
            if (object.correctiveActions) {
                if (!Array.isArray(object.correctiveActions))
                    throw TypeError(".auditing.CorrectiveActionCollection.correctiveActions: array expected");
                message.correctiveActions = [];
                for (var i = 0; i < object.correctiveActions.length; ++i) {
                    if (typeof object.correctiveActions[i] !== "object")
                        throw TypeError(".auditing.CorrectiveActionCollection.correctiveActions: object expected");
                    message.correctiveActions[i] = $root.auditing.CorrectiveActionProto.fromObject(object.correctiveActions[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a CorrectiveActionCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {auditing.CorrectiveActionCollection} message CorrectiveActionCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CorrectiveActionCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.correctiveActions = [];
            if (message.correctiveActions && message.correctiveActions.length) {
                object.correctiveActions = [];
                for (var j = 0; j < message.correctiveActions.length; ++j)
                    object.correctiveActions[j] = $root.auditing.CorrectiveActionProto.toObject(message.correctiveActions[j], options);
            }
            return object;
        };

        /**
         * Converts this CorrectiveActionCollection to JSON.
         * @function toJSON
         * @memberof auditing.CorrectiveActionCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CorrectiveActionCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CorrectiveActionCollection
         * @function getTypeUrl
         * @memberof auditing.CorrectiveActionCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CorrectiveActionCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.CorrectiveActionCollection";
        };

        return CorrectiveActionCollection;
    })();

    auditing.AuditCollection = (function() {

        /**
         * Properties of an AuditCollection.
         * @memberof auditing
         * @interface IAuditCollection
         * @property {Array.<auditing.IAuditProto>|null} [audits] AuditCollection audits
         */

        /**
         * Constructs a new AuditCollection.
         * @memberof auditing
         * @classdesc Represents an AuditCollection.
         * @implements IAuditCollection
         * @constructor
         * @param {auditing.IAuditCollection=} [properties] Properties to set
         */
        function AuditCollection(properties) {
            this.audits = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AuditCollection audits.
         * @member {Array.<auditing.IAuditProto>} audits
         * @memberof auditing.AuditCollection
         * @instance
         */
        AuditCollection.prototype.audits = $util.emptyArray;

        /**
         * Creates a new AuditCollection instance using the specified properties.
         * @function create
         * @memberof auditing.AuditCollection
         * @static
         * @param {auditing.IAuditCollection=} [properties] Properties to set
         * @returns {auditing.AuditCollection} AuditCollection instance
         */
        AuditCollection.create = function create(properties) {
            return new AuditCollection(properties);
        };

        /**
         * Encodes the specified AuditCollection message. Does not implicitly {@link auditing.AuditCollection.verify|verify} messages.
         * @function encode
         * @memberof auditing.AuditCollection
         * @static
         * @param {auditing.IAuditCollection} message AuditCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.audits != null && message.audits.length)
                for (var i = 0; i < message.audits.length; ++i)
                    $root.auditing.AuditProto.encode(message.audits[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified AuditCollection message, length delimited. Does not implicitly {@link auditing.AuditCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.AuditCollection
         * @static
         * @param {auditing.IAuditCollection} message AuditCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AuditCollection message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.AuditCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.AuditCollection} AuditCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.AuditCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.audits && message.audits.length))
                            message.audits = [];
                        message.audits.push($root.auditing.AuditProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AuditCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.AuditCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.AuditCollection} AuditCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AuditCollection message.
         * @function verify
         * @memberof auditing.AuditCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AuditCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.audits != null && message.hasOwnProperty("audits")) {
                if (!Array.isArray(message.audits))
                    return "audits: array expected";
                for (var i = 0; i < message.audits.length; ++i) {
                    var error = $root.auditing.AuditProto.verify(message.audits[i]);
                    if (error)
                        return "audits." + error;
                }
            }
            return null;
        };

        /**
         * Creates an AuditCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.AuditCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.AuditCollection} AuditCollection
         */
        AuditCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.AuditCollection)
                return object;
            var message = new $root.auditing.AuditCollection();
            if (object.audits) {
                if (!Array.isArray(object.audits))
                    throw TypeError(".auditing.AuditCollection.audits: array expected");
                message.audits = [];
                for (var i = 0; i < object.audits.length; ++i) {
                    if (typeof object.audits[i] !== "object")
                        throw TypeError(".auditing.AuditCollection.audits: object expected");
                    message.audits[i] = $root.auditing.AuditProto.fromObject(object.audits[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from an AuditCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.AuditCollection
         * @static
         * @param {auditing.AuditCollection} message AuditCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AuditCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.audits = [];
            if (message.audits && message.audits.length) {
                object.audits = [];
                for (var j = 0; j < message.audits.length; ++j)
                    object.audits[j] = $root.auditing.AuditProto.toObject(message.audits[j], options);
            }
            return object;
        };

        /**
         * Converts this AuditCollection to JSON.
         * @function toJSON
         * @memberof auditing.AuditCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AuditCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AuditCollection
         * @function getTypeUrl
         * @memberof auditing.AuditCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AuditCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.AuditCollection";
        };

        return AuditCollection;
    })();

    auditing.AuditEntryCollection = (function() {

        /**
         * Properties of an AuditEntryCollection.
         * @memberof auditing
         * @interface IAuditEntryCollection
         * @property {Array.<auditing.IAuditEntryProto>|null} [auditEntries] AuditEntryCollection auditEntries
         */

        /**
         * Constructs a new AuditEntryCollection.
         * @memberof auditing
         * @classdesc Represents an AuditEntryCollection.
         * @implements IAuditEntryCollection
         * @constructor
         * @param {auditing.IAuditEntryCollection=} [properties] Properties to set
         */
        function AuditEntryCollection(properties) {
            this.auditEntries = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AuditEntryCollection auditEntries.
         * @member {Array.<auditing.IAuditEntryProto>} auditEntries
         * @memberof auditing.AuditEntryCollection
         * @instance
         */
        AuditEntryCollection.prototype.auditEntries = $util.emptyArray;

        /**
         * Creates a new AuditEntryCollection instance using the specified properties.
         * @function create
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {auditing.IAuditEntryCollection=} [properties] Properties to set
         * @returns {auditing.AuditEntryCollection} AuditEntryCollection instance
         */
        AuditEntryCollection.create = function create(properties) {
            return new AuditEntryCollection(properties);
        };

        /**
         * Encodes the specified AuditEntryCollection message. Does not implicitly {@link auditing.AuditEntryCollection.verify|verify} messages.
         * @function encode
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {auditing.IAuditEntryCollection} message AuditEntryCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditEntryCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.auditEntries != null && message.auditEntries.length)
                for (var i = 0; i < message.auditEntries.length; ++i)
                    $root.auditing.AuditEntryProto.encode(message.auditEntries[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified AuditEntryCollection message, length delimited. Does not implicitly {@link auditing.AuditEntryCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {auditing.IAuditEntryCollection} message AuditEntryCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AuditEntryCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AuditEntryCollection message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.AuditEntryCollection} AuditEntryCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditEntryCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.AuditEntryCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.auditEntries && message.auditEntries.length))
                            message.auditEntries = [];
                        message.auditEntries.push($root.auditing.AuditEntryProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AuditEntryCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.AuditEntryCollection} AuditEntryCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AuditEntryCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AuditEntryCollection message.
         * @function verify
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AuditEntryCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.auditEntries != null && message.hasOwnProperty("auditEntries")) {
                if (!Array.isArray(message.auditEntries))
                    return "auditEntries: array expected";
                for (var i = 0; i < message.auditEntries.length; ++i) {
                    var error = $root.auditing.AuditEntryProto.verify(message.auditEntries[i]);
                    if (error)
                        return "auditEntries." + error;
                }
            }
            return null;
        };

        /**
         * Creates an AuditEntryCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.AuditEntryCollection} AuditEntryCollection
         */
        AuditEntryCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.AuditEntryCollection)
                return object;
            var message = new $root.auditing.AuditEntryCollection();
            if (object.auditEntries) {
                if (!Array.isArray(object.auditEntries))
                    throw TypeError(".auditing.AuditEntryCollection.auditEntries: array expected");
                message.auditEntries = [];
                for (var i = 0; i < object.auditEntries.length; ++i) {
                    if (typeof object.auditEntries[i] !== "object")
                        throw TypeError(".auditing.AuditEntryCollection.auditEntries: object expected");
                    message.auditEntries[i] = $root.auditing.AuditEntryProto.fromObject(object.auditEntries[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from an AuditEntryCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {auditing.AuditEntryCollection} message AuditEntryCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AuditEntryCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.auditEntries = [];
            if (message.auditEntries && message.auditEntries.length) {
                object.auditEntries = [];
                for (var j = 0; j < message.auditEntries.length; ++j)
                    object.auditEntries[j] = $root.auditing.AuditEntryProto.toObject(message.auditEntries[j], options);
            }
            return object;
        };

        /**
         * Converts this AuditEntryCollection to JSON.
         * @function toJSON
         * @memberof auditing.AuditEntryCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AuditEntryCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AuditEntryCollection
         * @function getTypeUrl
         * @memberof auditing.AuditEntryCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AuditEntryCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.AuditEntryCollection";
        };

        return AuditEntryCollection;
    })();

    auditing.ComplianceCommentCollection = (function() {

        /**
         * Properties of a ComplianceCommentCollection.
         * @memberof auditing
         * @interface IComplianceCommentCollection
         * @property {Array.<auditing.IComplianceCommentProto>|null} [complianceComments] ComplianceCommentCollection complianceComments
         */

        /**
         * Constructs a new ComplianceCommentCollection.
         * @memberof auditing
         * @classdesc Represents a ComplianceCommentCollection.
         * @implements IComplianceCommentCollection
         * @constructor
         * @param {auditing.IComplianceCommentCollection=} [properties] Properties to set
         */
        function ComplianceCommentCollection(properties) {
            this.complianceComments = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ComplianceCommentCollection complianceComments.
         * @member {Array.<auditing.IComplianceCommentProto>} complianceComments
         * @memberof auditing.ComplianceCommentCollection
         * @instance
         */
        ComplianceCommentCollection.prototype.complianceComments = $util.emptyArray;

        /**
         * Creates a new ComplianceCommentCollection instance using the specified properties.
         * @function create
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {auditing.IComplianceCommentCollection=} [properties] Properties to set
         * @returns {auditing.ComplianceCommentCollection} ComplianceCommentCollection instance
         */
        ComplianceCommentCollection.create = function create(properties) {
            return new ComplianceCommentCollection(properties);
        };

        /**
         * Encodes the specified ComplianceCommentCollection message. Does not implicitly {@link auditing.ComplianceCommentCollection.verify|verify} messages.
         * @function encode
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {auditing.IComplianceCommentCollection} message ComplianceCommentCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ComplianceCommentCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.complianceComments != null && message.complianceComments.length)
                for (var i = 0; i < message.complianceComments.length; ++i)
                    $root.auditing.ComplianceCommentProto.encode(message.complianceComments[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ComplianceCommentCollection message, length delimited. Does not implicitly {@link auditing.ComplianceCommentCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {auditing.IComplianceCommentCollection} message ComplianceCommentCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ComplianceCommentCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ComplianceCommentCollection message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.ComplianceCommentCollection} ComplianceCommentCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ComplianceCommentCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.ComplianceCommentCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.complianceComments && message.complianceComments.length))
                            message.complianceComments = [];
                        message.complianceComments.push($root.auditing.ComplianceCommentProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ComplianceCommentCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.ComplianceCommentCollection} ComplianceCommentCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ComplianceCommentCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ComplianceCommentCollection message.
         * @function verify
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ComplianceCommentCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.complianceComments != null && message.hasOwnProperty("complianceComments")) {
                if (!Array.isArray(message.complianceComments))
                    return "complianceComments: array expected";
                for (var i = 0; i < message.complianceComments.length; ++i) {
                    var error = $root.auditing.ComplianceCommentProto.verify(message.complianceComments[i]);
                    if (error)
                        return "complianceComments." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ComplianceCommentCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.ComplianceCommentCollection} ComplianceCommentCollection
         */
        ComplianceCommentCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.ComplianceCommentCollection)
                return object;
            var message = new $root.auditing.ComplianceCommentCollection();
            if (object.complianceComments) {
                if (!Array.isArray(object.complianceComments))
                    throw TypeError(".auditing.ComplianceCommentCollection.complianceComments: array expected");
                message.complianceComments = [];
                for (var i = 0; i < object.complianceComments.length; ++i) {
                    if (typeof object.complianceComments[i] !== "object")
                        throw TypeError(".auditing.ComplianceCommentCollection.complianceComments: object expected");
                    message.complianceComments[i] = $root.auditing.ComplianceCommentProto.fromObject(object.complianceComments[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ComplianceCommentCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {auditing.ComplianceCommentCollection} message ComplianceCommentCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ComplianceCommentCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.complianceComments = [];
            if (message.complianceComments && message.complianceComments.length) {
                object.complianceComments = [];
                for (var j = 0; j < message.complianceComments.length; ++j)
                    object.complianceComments[j] = $root.auditing.ComplianceCommentProto.toObject(message.complianceComments[j], options);
            }
            return object;
        };

        /**
         * Converts this ComplianceCommentCollection to JSON.
         * @function toJSON
         * @memberof auditing.ComplianceCommentCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ComplianceCommentCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ComplianceCommentCollection
         * @function getTypeUrl
         * @memberof auditing.ComplianceCommentCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ComplianceCommentCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.ComplianceCommentCollection";
        };

        return ComplianceCommentCollection;
    })();

    auditing.NonConformanceCommentCollection = (function() {

        /**
         * Properties of a NonConformanceCommentCollection.
         * @memberof auditing
         * @interface INonConformanceCommentCollection
         * @property {Array.<auditing.INonConformanceCommentProto>|null} [nonConformanceComments] NonConformanceCommentCollection nonConformanceComments
         */

        /**
         * Constructs a new NonConformanceCommentCollection.
         * @memberof auditing
         * @classdesc Represents a NonConformanceCommentCollection.
         * @implements INonConformanceCommentCollection
         * @constructor
         * @param {auditing.INonConformanceCommentCollection=} [properties] Properties to set
         */
        function NonConformanceCommentCollection(properties) {
            this.nonConformanceComments = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NonConformanceCommentCollection nonConformanceComments.
         * @member {Array.<auditing.INonConformanceCommentProto>} nonConformanceComments
         * @memberof auditing.NonConformanceCommentCollection
         * @instance
         */
        NonConformanceCommentCollection.prototype.nonConformanceComments = $util.emptyArray;

        /**
         * Creates a new NonConformanceCommentCollection instance using the specified properties.
         * @function create
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {auditing.INonConformanceCommentCollection=} [properties] Properties to set
         * @returns {auditing.NonConformanceCommentCollection} NonConformanceCommentCollection instance
         */
        NonConformanceCommentCollection.create = function create(properties) {
            return new NonConformanceCommentCollection(properties);
        };

        /**
         * Encodes the specified NonConformanceCommentCollection message. Does not implicitly {@link auditing.NonConformanceCommentCollection.verify|verify} messages.
         * @function encode
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {auditing.INonConformanceCommentCollection} message NonConformanceCommentCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NonConformanceCommentCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.nonConformanceComments != null && message.nonConformanceComments.length)
                for (var i = 0; i < message.nonConformanceComments.length; ++i)
                    $root.auditing.NonConformanceCommentProto.encode(message.nonConformanceComments[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified NonConformanceCommentCollection message, length delimited. Does not implicitly {@link auditing.NonConformanceCommentCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {auditing.INonConformanceCommentCollection} message NonConformanceCommentCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NonConformanceCommentCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NonConformanceCommentCollection message from the specified reader or buffer.
         * @function decode
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {auditing.NonConformanceCommentCollection} NonConformanceCommentCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NonConformanceCommentCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.auditing.NonConformanceCommentCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.nonConformanceComments && message.nonConformanceComments.length))
                            message.nonConformanceComments = [];
                        message.nonConformanceComments.push($root.auditing.NonConformanceCommentProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NonConformanceCommentCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {auditing.NonConformanceCommentCollection} NonConformanceCommentCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NonConformanceCommentCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NonConformanceCommentCollection message.
         * @function verify
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NonConformanceCommentCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.nonConformanceComments != null && message.hasOwnProperty("nonConformanceComments")) {
                if (!Array.isArray(message.nonConformanceComments))
                    return "nonConformanceComments: array expected";
                for (var i = 0; i < message.nonConformanceComments.length; ++i) {
                    var error = $root.auditing.NonConformanceCommentProto.verify(message.nonConformanceComments[i]);
                    if (error)
                        return "nonConformanceComments." + error;
                }
            }
            return null;
        };

        /**
         * Creates a NonConformanceCommentCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {auditing.NonConformanceCommentCollection} NonConformanceCommentCollection
         */
        NonConformanceCommentCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.auditing.NonConformanceCommentCollection)
                return object;
            var message = new $root.auditing.NonConformanceCommentCollection();
            if (object.nonConformanceComments) {
                if (!Array.isArray(object.nonConformanceComments))
                    throw TypeError(".auditing.NonConformanceCommentCollection.nonConformanceComments: array expected");
                message.nonConformanceComments = [];
                for (var i = 0; i < object.nonConformanceComments.length; ++i) {
                    if (typeof object.nonConformanceComments[i] !== "object")
                        throw TypeError(".auditing.NonConformanceCommentCollection.nonConformanceComments: object expected");
                    message.nonConformanceComments[i] = $root.auditing.NonConformanceCommentProto.fromObject(object.nonConformanceComments[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a NonConformanceCommentCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {auditing.NonConformanceCommentCollection} message NonConformanceCommentCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NonConformanceCommentCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.nonConformanceComments = [];
            if (message.nonConformanceComments && message.nonConformanceComments.length) {
                object.nonConformanceComments = [];
                for (var j = 0; j < message.nonConformanceComments.length; ++j)
                    object.nonConformanceComments[j] = $root.auditing.NonConformanceCommentProto.toObject(message.nonConformanceComments[j], options);
            }
            return object;
        };

        /**
         * Converts this NonConformanceCommentCollection to JSON.
         * @function toJSON
         * @memberof auditing.NonConformanceCommentCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NonConformanceCommentCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NonConformanceCommentCollection
         * @function getTypeUrl
         * @memberof auditing.NonConformanceCommentCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NonConformanceCommentCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/auditing.NonConformanceCommentCollection";
        };

        return NonConformanceCommentCollection;
    })();

    return auditing;
})();

$root.obligations = (function() {

    /**
     * Namespace obligations.
     * @exports obligations
     * @namespace
     */
    var obligations = {};

    obligations.ObligationProto = (function() {

        /**
         * Properties of an ObligationProto.
         * @memberof obligations
         * @interface IObligationProto
         * @property {string|null} [obligationNumber] ObligationProto obligationNumber
         * @property {string|null} [projectId] ObligationProto projectId
         * @property {string|null} [primaryEnvironmentalMechanismId] ObligationProto primaryEnvironmentalMechanismId
         * @property {string|null} [procedure] ObligationProto procedure
         * @property {string|null} [environmentalAspect] ObligationProto environmentalAspect
         * @property {string|null} [customEnvironmentalAspect] ObligationProto customEnvironmentalAspect
         * @property {string|null} [obligation] ObligationProto obligation
         * @property {string|null} [accountability] ObligationProto accountability
         * @property {Array.<string>|null} [responsibleUserIds] ObligationProto responsibleUserIds
         * @property {string|null} [projectPhase] ObligationProto projectPhase
         * @property {string|null} [actionDueDate] ObligationProto actionDueDate
         * @property {string|null} [closeOutDate] ObligationProto closeOutDate
         * @property {string|null} [status] ObligationProto status
         * @property {string|null} [supportingInformation] ObligationProto supportingInformation
         * @property {string|null} [generalComments] ObligationProto generalComments
         * @property {string|null} [evidenceNotes] ObligationProto evidenceNotes
         * @property {boolean|null} [recurringObligation] ObligationProto recurringObligation
         * @property {string|null} [recurringFrequency] ObligationProto recurringFrequency
         * @property {string|null} [recurringStatus] ObligationProto recurringStatus
         * @property {string|null} [recurringForecastedDate] ObligationProto recurringForecastedDate
         * @property {boolean|null} [inspection] ObligationProto inspection
         * @property {string|null} [inspectionFrequency] ObligationProto inspectionFrequency
         * @property {string|null} [siteOrDesktop] ObligationProto siteOrDesktop
         * @property {boolean|null} [newControlActionRequired] ObligationProto newControlActionRequired
         * @property {string|null} [obligationType] ObligationProto obligationType
         * @property {boolean|null} [gapAnalysis] ObligationProto gapAnalysis
         * @property {string|null} [notesForGapAnalysis] ObligationProto notesForGapAnalysis
         * @property {string|null} [createdAt] ObligationProto createdAt
         * @property {string|null} [updatedAt] ObligationProto updatedAt
         */

        /**
         * Constructs a new ObligationProto.
         * @memberof obligations
         * @classdesc Represents an ObligationProto.
         * @implements IObligationProto
         * @constructor
         * @param {obligations.IObligationProto=} [properties] Properties to set
         */
        function ObligationProto(properties) {
            this.responsibleUserIds = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ObligationProto obligationNumber.
         * @member {string} obligationNumber
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.obligationNumber = "";

        /**
         * ObligationProto projectId.
         * @member {string} projectId
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.projectId = "";

        /**
         * ObligationProto primaryEnvironmentalMechanismId.
         * @member {string} primaryEnvironmentalMechanismId
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.primaryEnvironmentalMechanismId = "";

        /**
         * ObligationProto procedure.
         * @member {string} procedure
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.procedure = "";

        /**
         * ObligationProto environmentalAspect.
         * @member {string} environmentalAspect
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.environmentalAspect = "";

        /**
         * ObligationProto customEnvironmentalAspect.
         * @member {string} customEnvironmentalAspect
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.customEnvironmentalAspect = "";

        /**
         * ObligationProto obligation.
         * @member {string} obligation
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.obligation = "";

        /**
         * ObligationProto accountability.
         * @member {string} accountability
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.accountability = "";

        /**
         * ObligationProto responsibleUserIds.
         * @member {Array.<string>} responsibleUserIds
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.responsibleUserIds = $util.emptyArray;

        /**
         * ObligationProto projectPhase.
         * @member {string} projectPhase
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.projectPhase = "";

        /**
         * ObligationProto actionDueDate.
         * @member {string} actionDueDate
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.actionDueDate = "";

        /**
         * ObligationProto closeOutDate.
         * @member {string} closeOutDate
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.closeOutDate = "";

        /**
         * ObligationProto status.
         * @member {string} status
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.status = "";

        /**
         * ObligationProto supportingInformation.
         * @member {string} supportingInformation
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.supportingInformation = "";

        /**
         * ObligationProto generalComments.
         * @member {string} generalComments
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.generalComments = "";

        /**
         * ObligationProto evidenceNotes.
         * @member {string} evidenceNotes
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.evidenceNotes = "";

        /**
         * ObligationProto recurringObligation.
         * @member {boolean} recurringObligation
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.recurringObligation = false;

        /**
         * ObligationProto recurringFrequency.
         * @member {string} recurringFrequency
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.recurringFrequency = "";

        /**
         * ObligationProto recurringStatus.
         * @member {string} recurringStatus
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.recurringStatus = "";

        /**
         * ObligationProto recurringForecastedDate.
         * @member {string} recurringForecastedDate
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.recurringForecastedDate = "";

        /**
         * ObligationProto inspection.
         * @member {boolean} inspection
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.inspection = false;

        /**
         * ObligationProto inspectionFrequency.
         * @member {string} inspectionFrequency
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.inspectionFrequency = "";

        /**
         * ObligationProto siteOrDesktop.
         * @member {string} siteOrDesktop
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.siteOrDesktop = "";

        /**
         * ObligationProto newControlActionRequired.
         * @member {boolean} newControlActionRequired
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.newControlActionRequired = false;

        /**
         * ObligationProto obligationType.
         * @member {string} obligationType
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.obligationType = "";

        /**
         * ObligationProto gapAnalysis.
         * @member {boolean} gapAnalysis
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.gapAnalysis = false;

        /**
         * ObligationProto notesForGapAnalysis.
         * @member {string} notesForGapAnalysis
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.notesForGapAnalysis = "";

        /**
         * ObligationProto createdAt.
         * @member {string} createdAt
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.createdAt = "";

        /**
         * ObligationProto updatedAt.
         * @member {string} updatedAt
         * @memberof obligations.ObligationProto
         * @instance
         */
        ObligationProto.prototype.updatedAt = "";

        /**
         * Creates a new ObligationProto instance using the specified properties.
         * @function create
         * @memberof obligations.ObligationProto
         * @static
         * @param {obligations.IObligationProto=} [properties] Properties to set
         * @returns {obligations.ObligationProto} ObligationProto instance
         */
        ObligationProto.create = function create(properties) {
            return new ObligationProto(properties);
        };

        /**
         * Encodes the specified ObligationProto message. Does not implicitly {@link obligations.ObligationProto.verify|verify} messages.
         * @function encode
         * @memberof obligations.ObligationProto
         * @static
         * @param {obligations.IObligationProto} message ObligationProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ObligationProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.obligationNumber != null && Object.hasOwnProperty.call(message, "obligationNumber"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.obligationNumber);
            if (message.projectId != null && Object.hasOwnProperty.call(message, "projectId"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.projectId);
            if (message.primaryEnvironmentalMechanismId != null && Object.hasOwnProperty.call(message, "primaryEnvironmentalMechanismId"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.primaryEnvironmentalMechanismId);
            if (message.procedure != null && Object.hasOwnProperty.call(message, "procedure"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.procedure);
            if (message.environmentalAspect != null && Object.hasOwnProperty.call(message, "environmentalAspect"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.environmentalAspect);
            if (message.customEnvironmentalAspect != null && Object.hasOwnProperty.call(message, "customEnvironmentalAspect"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.customEnvironmentalAspect);
            if (message.obligation != null && Object.hasOwnProperty.call(message, "obligation"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.obligation);
            if (message.accountability != null && Object.hasOwnProperty.call(message, "accountability"))
                writer.uint32(/* id 8, wireType 2 =*/66).string(message.accountability);
            if (message.responsibleUserIds != null && message.responsibleUserIds.length)
                for (var i = 0; i < message.responsibleUserIds.length; ++i)
                    writer.uint32(/* id 9, wireType 2 =*/74).string(message.responsibleUserIds[i]);
            if (message.projectPhase != null && Object.hasOwnProperty.call(message, "projectPhase"))
                writer.uint32(/* id 10, wireType 2 =*/82).string(message.projectPhase);
            if (message.actionDueDate != null && Object.hasOwnProperty.call(message, "actionDueDate"))
                writer.uint32(/* id 11, wireType 2 =*/90).string(message.actionDueDate);
            if (message.closeOutDate != null && Object.hasOwnProperty.call(message, "closeOutDate"))
                writer.uint32(/* id 12, wireType 2 =*/98).string(message.closeOutDate);
            if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                writer.uint32(/* id 13, wireType 2 =*/106).string(message.status);
            if (message.supportingInformation != null && Object.hasOwnProperty.call(message, "supportingInformation"))
                writer.uint32(/* id 14, wireType 2 =*/114).string(message.supportingInformation);
            if (message.generalComments != null && Object.hasOwnProperty.call(message, "generalComments"))
                writer.uint32(/* id 15, wireType 2 =*/122).string(message.generalComments);
            if (message.evidenceNotes != null && Object.hasOwnProperty.call(message, "evidenceNotes"))
                writer.uint32(/* id 16, wireType 2 =*/130).string(message.evidenceNotes);
            if (message.recurringObligation != null && Object.hasOwnProperty.call(message, "recurringObligation"))
                writer.uint32(/* id 17, wireType 0 =*/136).bool(message.recurringObligation);
            if (message.recurringFrequency != null && Object.hasOwnProperty.call(message, "recurringFrequency"))
                writer.uint32(/* id 18, wireType 2 =*/146).string(message.recurringFrequency);
            if (message.recurringStatus != null && Object.hasOwnProperty.call(message, "recurringStatus"))
                writer.uint32(/* id 19, wireType 2 =*/154).string(message.recurringStatus);
            if (message.recurringForecastedDate != null && Object.hasOwnProperty.call(message, "recurringForecastedDate"))
                writer.uint32(/* id 20, wireType 2 =*/162).string(message.recurringForecastedDate);
            if (message.inspection != null && Object.hasOwnProperty.call(message, "inspection"))
                writer.uint32(/* id 21, wireType 0 =*/168).bool(message.inspection);
            if (message.inspectionFrequency != null && Object.hasOwnProperty.call(message, "inspectionFrequency"))
                writer.uint32(/* id 22, wireType 2 =*/178).string(message.inspectionFrequency);
            if (message.siteOrDesktop != null && Object.hasOwnProperty.call(message, "siteOrDesktop"))
                writer.uint32(/* id 23, wireType 2 =*/186).string(message.siteOrDesktop);
            if (message.newControlActionRequired != null && Object.hasOwnProperty.call(message, "newControlActionRequired"))
                writer.uint32(/* id 24, wireType 0 =*/192).bool(message.newControlActionRequired);
            if (message.obligationType != null && Object.hasOwnProperty.call(message, "obligationType"))
                writer.uint32(/* id 25, wireType 2 =*/202).string(message.obligationType);
            if (message.gapAnalysis != null && Object.hasOwnProperty.call(message, "gapAnalysis"))
                writer.uint32(/* id 26, wireType 0 =*/208).bool(message.gapAnalysis);
            if (message.notesForGapAnalysis != null && Object.hasOwnProperty.call(message, "notesForGapAnalysis"))
                writer.uint32(/* id 27, wireType 2 =*/218).string(message.notesForGapAnalysis);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 28, wireType 2 =*/226).string(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 29, wireType 2 =*/234).string(message.updatedAt);
            return writer;
        };

        /**
         * Encodes the specified ObligationProto message, length delimited. Does not implicitly {@link obligations.ObligationProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof obligations.ObligationProto
         * @static
         * @param {obligations.IObligationProto} message ObligationProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ObligationProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an ObligationProto message from the specified reader or buffer.
         * @function decode
         * @memberof obligations.ObligationProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {obligations.ObligationProto} ObligationProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ObligationProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.obligations.ObligationProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.obligationNumber = reader.string();
                        break;
                    }
                case 2: {
                        message.projectId = reader.string();
                        break;
                    }
                case 3: {
                        message.primaryEnvironmentalMechanismId = reader.string();
                        break;
                    }
                case 4: {
                        message.procedure = reader.string();
                        break;
                    }
                case 5: {
                        message.environmentalAspect = reader.string();
                        break;
                    }
                case 6: {
                        message.customEnvironmentalAspect = reader.string();
                        break;
                    }
                case 7: {
                        message.obligation = reader.string();
                        break;
                    }
                case 8: {
                        message.accountability = reader.string();
                        break;
                    }
                case 9: {
                        if (!(message.responsibleUserIds && message.responsibleUserIds.length))
                            message.responsibleUserIds = [];
                        message.responsibleUserIds.push(reader.string());
                        break;
                    }
                case 10: {
                        message.projectPhase = reader.string();
                        break;
                    }
                case 11: {
                        message.actionDueDate = reader.string();
                        break;
                    }
                case 12: {
                        message.closeOutDate = reader.string();
                        break;
                    }
                case 13: {
                        message.status = reader.string();
                        break;
                    }
                case 14: {
                        message.supportingInformation = reader.string();
                        break;
                    }
                case 15: {
                        message.generalComments = reader.string();
                        break;
                    }
                case 16: {
                        message.evidenceNotes = reader.string();
                        break;
                    }
                case 17: {
                        message.recurringObligation = reader.bool();
                        break;
                    }
                case 18: {
                        message.recurringFrequency = reader.string();
                        break;
                    }
                case 19: {
                        message.recurringStatus = reader.string();
                        break;
                    }
                case 20: {
                        message.recurringForecastedDate = reader.string();
                        break;
                    }
                case 21: {
                        message.inspection = reader.bool();
                        break;
                    }
                case 22: {
                        message.inspectionFrequency = reader.string();
                        break;
                    }
                case 23: {
                        message.siteOrDesktop = reader.string();
                        break;
                    }
                case 24: {
                        message.newControlActionRequired = reader.bool();
                        break;
                    }
                case 25: {
                        message.obligationType = reader.string();
                        break;
                    }
                case 26: {
                        message.gapAnalysis = reader.bool();
                        break;
                    }
                case 27: {
                        message.notesForGapAnalysis = reader.string();
                        break;
                    }
                case 28: {
                        message.createdAt = reader.string();
                        break;
                    }
                case 29: {
                        message.updatedAt = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an ObligationProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof obligations.ObligationProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {obligations.ObligationProto} ObligationProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ObligationProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an ObligationProto message.
         * @function verify
         * @memberof obligations.ObligationProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ObligationProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.obligationNumber != null && message.hasOwnProperty("obligationNumber"))
                if (!$util.isString(message.obligationNumber))
                    return "obligationNumber: string expected";
            if (message.projectId != null && message.hasOwnProperty("projectId"))
                if (!$util.isString(message.projectId))
                    return "projectId: string expected";
            if (message.primaryEnvironmentalMechanismId != null && message.hasOwnProperty("primaryEnvironmentalMechanismId"))
                if (!$util.isString(message.primaryEnvironmentalMechanismId))
                    return "primaryEnvironmentalMechanismId: string expected";
            if (message.procedure != null && message.hasOwnProperty("procedure"))
                if (!$util.isString(message.procedure))
                    return "procedure: string expected";
            if (message.environmentalAspect != null && message.hasOwnProperty("environmentalAspect"))
                if (!$util.isString(message.environmentalAspect))
                    return "environmentalAspect: string expected";
            if (message.customEnvironmentalAspect != null && message.hasOwnProperty("customEnvironmentalAspect"))
                if (!$util.isString(message.customEnvironmentalAspect))
                    return "customEnvironmentalAspect: string expected";
            if (message.obligation != null && message.hasOwnProperty("obligation"))
                if (!$util.isString(message.obligation))
                    return "obligation: string expected";
            if (message.accountability != null && message.hasOwnProperty("accountability"))
                if (!$util.isString(message.accountability))
                    return "accountability: string expected";
            if (message.responsibleUserIds != null && message.hasOwnProperty("responsibleUserIds")) {
                if (!Array.isArray(message.responsibleUserIds))
                    return "responsibleUserIds: array expected";
                for (var i = 0; i < message.responsibleUserIds.length; ++i)
                    if (!$util.isString(message.responsibleUserIds[i]))
                        return "responsibleUserIds: string[] expected";
            }
            if (message.projectPhase != null && message.hasOwnProperty("projectPhase"))
                if (!$util.isString(message.projectPhase))
                    return "projectPhase: string expected";
            if (message.actionDueDate != null && message.hasOwnProperty("actionDueDate"))
                if (!$util.isString(message.actionDueDate))
                    return "actionDueDate: string expected";
            if (message.closeOutDate != null && message.hasOwnProperty("closeOutDate"))
                if (!$util.isString(message.closeOutDate))
                    return "closeOutDate: string expected";
            if (message.status != null && message.hasOwnProperty("status"))
                if (!$util.isString(message.status))
                    return "status: string expected";
            if (message.supportingInformation != null && message.hasOwnProperty("supportingInformation"))
                if (!$util.isString(message.supportingInformation))
                    return "supportingInformation: string expected";
            if (message.generalComments != null && message.hasOwnProperty("generalComments"))
                if (!$util.isString(message.generalComments))
                    return "generalComments: string expected";
            if (message.evidenceNotes != null && message.hasOwnProperty("evidenceNotes"))
                if (!$util.isString(message.evidenceNotes))
                    return "evidenceNotes: string expected";
            if (message.recurringObligation != null && message.hasOwnProperty("recurringObligation"))
                if (typeof message.recurringObligation !== "boolean")
                    return "recurringObligation: boolean expected";
            if (message.recurringFrequency != null && message.hasOwnProperty("recurringFrequency"))
                if (!$util.isString(message.recurringFrequency))
                    return "recurringFrequency: string expected";
            if (message.recurringStatus != null && message.hasOwnProperty("recurringStatus"))
                if (!$util.isString(message.recurringStatus))
                    return "recurringStatus: string expected";
            if (message.recurringForecastedDate != null && message.hasOwnProperty("recurringForecastedDate"))
                if (!$util.isString(message.recurringForecastedDate))
                    return "recurringForecastedDate: string expected";
            if (message.inspection != null && message.hasOwnProperty("inspection"))
                if (typeof message.inspection !== "boolean")
                    return "inspection: boolean expected";
            if (message.inspectionFrequency != null && message.hasOwnProperty("inspectionFrequency"))
                if (!$util.isString(message.inspectionFrequency))
                    return "inspectionFrequency: string expected";
            if (message.siteOrDesktop != null && message.hasOwnProperty("siteOrDesktop"))
                if (!$util.isString(message.siteOrDesktop))
                    return "siteOrDesktop: string expected";
            if (message.newControlActionRequired != null && message.hasOwnProperty("newControlActionRequired"))
                if (typeof message.newControlActionRequired !== "boolean")
                    return "newControlActionRequired: boolean expected";
            if (message.obligationType != null && message.hasOwnProperty("obligationType"))
                if (!$util.isString(message.obligationType))
                    return "obligationType: string expected";
            if (message.gapAnalysis != null && message.hasOwnProperty("gapAnalysis"))
                if (typeof message.gapAnalysis !== "boolean")
                    return "gapAnalysis: boolean expected";
            if (message.notesForGapAnalysis != null && message.hasOwnProperty("notesForGapAnalysis"))
                if (!$util.isString(message.notesForGapAnalysis))
                    return "notesForGapAnalysis: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isString(message.createdAt))
                    return "createdAt: string expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isString(message.updatedAt))
                    return "updatedAt: string expected";
            return null;
        };

        /**
         * Creates an ObligationProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof obligations.ObligationProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {obligations.ObligationProto} ObligationProto
         */
        ObligationProto.fromObject = function fromObject(object) {
            if (object instanceof $root.obligations.ObligationProto)
                return object;
            var message = new $root.obligations.ObligationProto();
            if (object.obligationNumber != null)
                message.obligationNumber = String(object.obligationNumber);
            if (object.projectId != null)
                message.projectId = String(object.projectId);
            if (object.primaryEnvironmentalMechanismId != null)
                message.primaryEnvironmentalMechanismId = String(object.primaryEnvironmentalMechanismId);
            if (object.procedure != null)
                message.procedure = String(object.procedure);
            if (object.environmentalAspect != null)
                message.environmentalAspect = String(object.environmentalAspect);
            if (object.customEnvironmentalAspect != null)
                message.customEnvironmentalAspect = String(object.customEnvironmentalAspect);
            if (object.obligation != null)
                message.obligation = String(object.obligation);
            if (object.accountability != null)
                message.accountability = String(object.accountability);
            if (object.responsibleUserIds) {
                if (!Array.isArray(object.responsibleUserIds))
                    throw TypeError(".obligations.ObligationProto.responsibleUserIds: array expected");
                message.responsibleUserIds = [];
                for (var i = 0; i < object.responsibleUserIds.length; ++i)
                    message.responsibleUserIds[i] = String(object.responsibleUserIds[i]);
            }
            if (object.projectPhase != null)
                message.projectPhase = String(object.projectPhase);
            if (object.actionDueDate != null)
                message.actionDueDate = String(object.actionDueDate);
            if (object.closeOutDate != null)
                message.closeOutDate = String(object.closeOutDate);
            if (object.status != null)
                message.status = String(object.status);
            if (object.supportingInformation != null)
                message.supportingInformation = String(object.supportingInformation);
            if (object.generalComments != null)
                message.generalComments = String(object.generalComments);
            if (object.evidenceNotes != null)
                message.evidenceNotes = String(object.evidenceNotes);
            if (object.recurringObligation != null)
                message.recurringObligation = Boolean(object.recurringObligation);
            if (object.recurringFrequency != null)
                message.recurringFrequency = String(object.recurringFrequency);
            if (object.recurringStatus != null)
                message.recurringStatus = String(object.recurringStatus);
            if (object.recurringForecastedDate != null)
                message.recurringForecastedDate = String(object.recurringForecastedDate);
            if (object.inspection != null)
                message.inspection = Boolean(object.inspection);
            if (object.inspectionFrequency != null)
                message.inspectionFrequency = String(object.inspectionFrequency);
            if (object.siteOrDesktop != null)
                message.siteOrDesktop = String(object.siteOrDesktop);
            if (object.newControlActionRequired != null)
                message.newControlActionRequired = Boolean(object.newControlActionRequired);
            if (object.obligationType != null)
                message.obligationType = String(object.obligationType);
            if (object.gapAnalysis != null)
                message.gapAnalysis = Boolean(object.gapAnalysis);
            if (object.notesForGapAnalysis != null)
                message.notesForGapAnalysis = String(object.notesForGapAnalysis);
            if (object.createdAt != null)
                message.createdAt = String(object.createdAt);
            if (object.updatedAt != null)
                message.updatedAt = String(object.updatedAt);
            return message;
        };

        /**
         * Creates a plain object from an ObligationProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof obligations.ObligationProto
         * @static
         * @param {obligations.ObligationProto} message ObligationProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ObligationProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.responsibleUserIds = [];
            if (options.defaults) {
                object.obligationNumber = "";
                object.projectId = "";
                object.primaryEnvironmentalMechanismId = "";
                object.procedure = "";
                object.environmentalAspect = "";
                object.customEnvironmentalAspect = "";
                object.obligation = "";
                object.accountability = "";
                object.projectPhase = "";
                object.actionDueDate = "";
                object.closeOutDate = "";
                object.status = "";
                object.supportingInformation = "";
                object.generalComments = "";
                object.evidenceNotes = "";
                object.recurringObligation = false;
                object.recurringFrequency = "";
                object.recurringStatus = "";
                object.recurringForecastedDate = "";
                object.inspection = false;
                object.inspectionFrequency = "";
                object.siteOrDesktop = "";
                object.newControlActionRequired = false;
                object.obligationType = "";
                object.gapAnalysis = false;
                object.notesForGapAnalysis = "";
                object.createdAt = "";
                object.updatedAt = "";
            }
            if (message.obligationNumber != null && message.hasOwnProperty("obligationNumber"))
                object.obligationNumber = message.obligationNumber;
            if (message.projectId != null && message.hasOwnProperty("projectId"))
                object.projectId = message.projectId;
            if (message.primaryEnvironmentalMechanismId != null && message.hasOwnProperty("primaryEnvironmentalMechanismId"))
                object.primaryEnvironmentalMechanismId = message.primaryEnvironmentalMechanismId;
            if (message.procedure != null && message.hasOwnProperty("procedure"))
                object.procedure = message.procedure;
            if (message.environmentalAspect != null && message.hasOwnProperty("environmentalAspect"))
                object.environmentalAspect = message.environmentalAspect;
            if (message.customEnvironmentalAspect != null && message.hasOwnProperty("customEnvironmentalAspect"))
                object.customEnvironmentalAspect = message.customEnvironmentalAspect;
            if (message.obligation != null && message.hasOwnProperty("obligation"))
                object.obligation = message.obligation;
            if (message.accountability != null && message.hasOwnProperty("accountability"))
                object.accountability = message.accountability;
            if (message.responsibleUserIds && message.responsibleUserIds.length) {
                object.responsibleUserIds = [];
                for (var j = 0; j < message.responsibleUserIds.length; ++j)
                    object.responsibleUserIds[j] = message.responsibleUserIds[j];
            }
            if (message.projectPhase != null && message.hasOwnProperty("projectPhase"))
                object.projectPhase = message.projectPhase;
            if (message.actionDueDate != null && message.hasOwnProperty("actionDueDate"))
                object.actionDueDate = message.actionDueDate;
            if (message.closeOutDate != null && message.hasOwnProperty("closeOutDate"))
                object.closeOutDate = message.closeOutDate;
            if (message.status != null && message.hasOwnProperty("status"))
                object.status = message.status;
            if (message.supportingInformation != null && message.hasOwnProperty("supportingInformation"))
                object.supportingInformation = message.supportingInformation;
            if (message.generalComments != null && message.hasOwnProperty("generalComments"))
                object.generalComments = message.generalComments;
            if (message.evidenceNotes != null && message.hasOwnProperty("evidenceNotes"))
                object.evidenceNotes = message.evidenceNotes;
            if (message.recurringObligation != null && message.hasOwnProperty("recurringObligation"))
                object.recurringObligation = message.recurringObligation;
            if (message.recurringFrequency != null && message.hasOwnProperty("recurringFrequency"))
                object.recurringFrequency = message.recurringFrequency;
            if (message.recurringStatus != null && message.hasOwnProperty("recurringStatus"))
                object.recurringStatus = message.recurringStatus;
            if (message.recurringForecastedDate != null && message.hasOwnProperty("recurringForecastedDate"))
                object.recurringForecastedDate = message.recurringForecastedDate;
            if (message.inspection != null && message.hasOwnProperty("inspection"))
                object.inspection = message.inspection;
            if (message.inspectionFrequency != null && message.hasOwnProperty("inspectionFrequency"))
                object.inspectionFrequency = message.inspectionFrequency;
            if (message.siteOrDesktop != null && message.hasOwnProperty("siteOrDesktop"))
                object.siteOrDesktop = message.siteOrDesktop;
            if (message.newControlActionRequired != null && message.hasOwnProperty("newControlActionRequired"))
                object.newControlActionRequired = message.newControlActionRequired;
            if (message.obligationType != null && message.hasOwnProperty("obligationType"))
                object.obligationType = message.obligationType;
            if (message.gapAnalysis != null && message.hasOwnProperty("gapAnalysis"))
                object.gapAnalysis = message.gapAnalysis;
            if (message.notesForGapAnalysis != null && message.hasOwnProperty("notesForGapAnalysis"))
                object.notesForGapAnalysis = message.notesForGapAnalysis;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                object.createdAt = message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                object.updatedAt = message.updatedAt;
            return object;
        };

        /**
         * Converts this ObligationProto to JSON.
         * @function toJSON
         * @memberof obligations.ObligationProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ObligationProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ObligationProto
         * @function getTypeUrl
         * @memberof obligations.ObligationProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ObligationProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/obligations.ObligationProto";
        };

        return ObligationProto;
    })();

    obligations.ObligationCollection = (function() {

        /**
         * Properties of an ObligationCollection.
         * @memberof obligations
         * @interface IObligationCollection
         * @property {Array.<obligations.IObligationProto>|null} [obligations] ObligationCollection obligations
         */

        /**
         * Constructs a new ObligationCollection.
         * @memberof obligations
         * @classdesc Represents an ObligationCollection.
         * @implements IObligationCollection
         * @constructor
         * @param {obligations.IObligationCollection=} [properties] Properties to set
         */
        function ObligationCollection(properties) {
            this.obligations = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ObligationCollection obligations.
         * @member {Array.<obligations.IObligationProto>} obligations
         * @memberof obligations.ObligationCollection
         * @instance
         */
        ObligationCollection.prototype.obligations = $util.emptyArray;

        /**
         * Creates a new ObligationCollection instance using the specified properties.
         * @function create
         * @memberof obligations.ObligationCollection
         * @static
         * @param {obligations.IObligationCollection=} [properties] Properties to set
         * @returns {obligations.ObligationCollection} ObligationCollection instance
         */
        ObligationCollection.create = function create(properties) {
            return new ObligationCollection(properties);
        };

        /**
         * Encodes the specified ObligationCollection message. Does not implicitly {@link obligations.ObligationCollection.verify|verify} messages.
         * @function encode
         * @memberof obligations.ObligationCollection
         * @static
         * @param {obligations.IObligationCollection} message ObligationCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ObligationCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.obligations != null && message.obligations.length)
                for (var i = 0; i < message.obligations.length; ++i)
                    $root.obligations.ObligationProto.encode(message.obligations[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ObligationCollection message, length delimited. Does not implicitly {@link obligations.ObligationCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof obligations.ObligationCollection
         * @static
         * @param {obligations.IObligationCollection} message ObligationCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ObligationCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an ObligationCollection message from the specified reader or buffer.
         * @function decode
         * @memberof obligations.ObligationCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {obligations.ObligationCollection} ObligationCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ObligationCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.obligations.ObligationCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.obligations && message.obligations.length))
                            message.obligations = [];
                        message.obligations.push($root.obligations.ObligationProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an ObligationCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof obligations.ObligationCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {obligations.ObligationCollection} ObligationCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ObligationCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an ObligationCollection message.
         * @function verify
         * @memberof obligations.ObligationCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ObligationCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.obligations != null && message.hasOwnProperty("obligations")) {
                if (!Array.isArray(message.obligations))
                    return "obligations: array expected";
                for (var i = 0; i < message.obligations.length; ++i) {
                    var error = $root.obligations.ObligationProto.verify(message.obligations[i]);
                    if (error)
                        return "obligations." + error;
                }
            }
            return null;
        };

        /**
         * Creates an ObligationCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof obligations.ObligationCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {obligations.ObligationCollection} ObligationCollection
         */
        ObligationCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.obligations.ObligationCollection)
                return object;
            var message = new $root.obligations.ObligationCollection();
            if (object.obligations) {
                if (!Array.isArray(object.obligations))
                    throw TypeError(".obligations.ObligationCollection.obligations: array expected");
                message.obligations = [];
                for (var i = 0; i < object.obligations.length; ++i) {
                    if (typeof object.obligations[i] !== "object")
                        throw TypeError(".obligations.ObligationCollection.obligations: object expected");
                    message.obligations[i] = $root.obligations.ObligationProto.fromObject(object.obligations[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from an ObligationCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof obligations.ObligationCollection
         * @static
         * @param {obligations.ObligationCollection} message ObligationCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ObligationCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.obligations = [];
            if (message.obligations && message.obligations.length) {
                object.obligations = [];
                for (var j = 0; j < message.obligations.length; ++j)
                    object.obligations[j] = $root.obligations.ObligationProto.toObject(message.obligations[j], options);
            }
            return object;
        };

        /**
         * Converts this ObligationCollection to JSON.
         * @function toJSON
         * @memberof obligations.ObligationCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ObligationCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ObligationCollection
         * @function getTypeUrl
         * @memberof obligations.ObligationCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ObligationCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/obligations.ObligationCollection";
        };

        return ObligationCollection;
    })();

    return obligations;
})();

$root.greenova = (function() {

    /**
     * Namespace greenova.
     * @exports greenova
     * @namespace
     */
    var greenova = {};

    greenova.mechanisms = (function() {

        /**
         * Namespace mechanisms.
         * @memberof greenova
         * @namespace
         */
        var mechanisms = {};

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
        mechanisms.ObligationStatus = (function() {
            var valuesById = {}, values = Object.create(valuesById);
            values[valuesById[0] = "STATUS_UNKNOWN"] = 0;
            values[valuesById[1] = "STATUS_NOT_STARTED"] = 1;
            values[valuesById[2] = "STATUS_IN_PROGRESS"] = 2;
            values[valuesById[3] = "STATUS_COMPLETED"] = 3;
            values[valuesById[4] = "STATUS_OVERDUE"] = 4;
            return values;
        })();

        mechanisms.ObligationInsight = (function() {

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
            function ObligationInsight(properties) {
                if (properties)
                    for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ObligationInsight obligationNumber.
             * @member {string} obligationNumber
             * @memberof greenova.mechanisms.ObligationInsight
             * @instance
             */
            ObligationInsight.prototype.obligationNumber = "";

            /**
             * ObligationInsight dueDate.
             * @member {string} dueDate
             * @memberof greenova.mechanisms.ObligationInsight
             * @instance
             */
            ObligationInsight.prototype.dueDate = "";

            /**
             * ObligationInsight closeOutDate.
             * @member {string} closeOutDate
             * @memberof greenova.mechanisms.ObligationInsight
             * @instance
             */
            ObligationInsight.prototype.closeOutDate = "";

            /**
             * Creates a new ObligationInsight instance using the specified properties.
             * @function create
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {greenova.mechanisms.IObligationInsight=} [properties] Properties to set
             * @returns {greenova.mechanisms.ObligationInsight} ObligationInsight instance
             */
            ObligationInsight.create = function create(properties) {
                return new ObligationInsight(properties);
            };

            /**
             * Encodes the specified ObligationInsight message. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
             * @function encode
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {greenova.mechanisms.IObligationInsight} message ObligationInsight message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ObligationInsight.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.obligationNumber != null && Object.hasOwnProperty.call(message, "obligationNumber"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.obligationNumber);
                if (message.dueDate != null && Object.hasOwnProperty.call(message, "dueDate"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.dueDate);
                if (message.closeOutDate != null && Object.hasOwnProperty.call(message, "closeOutDate"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.closeOutDate);
                return writer;
            };

            /**
             * Encodes the specified ObligationInsight message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
             * @function encodeDelimited
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {greenova.mechanisms.IObligationInsight} message ObligationInsight message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ObligationInsight.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

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
            ObligationInsight.decode = function decode(reader, length, error) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                var end = length === undefined ? reader.len : reader.pos + length, message = new $root.greenova.mechanisms.ObligationInsight();
                while (reader.pos < end) {
                    var tag = reader.uint32();
                    if (tag === error)
                        break;
                    switch (tag >>> 3) {
                    case 1: {
                            message.obligationNumber = reader.string();
                            break;
                        }
                    case 2: {
                            message.dueDate = reader.string();
                            break;
                        }
                    case 3: {
                            message.closeOutDate = reader.string();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

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
            ObligationInsight.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies an ObligationInsight message.
             * @function verify
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ObligationInsight.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.obligationNumber != null && message.hasOwnProperty("obligationNumber"))
                    if (!$util.isString(message.obligationNumber))
                        return "obligationNumber: string expected";
                if (message.dueDate != null && message.hasOwnProperty("dueDate"))
                    if (!$util.isString(message.dueDate))
                        return "dueDate: string expected";
                if (message.closeOutDate != null && message.hasOwnProperty("closeOutDate"))
                    if (!$util.isString(message.closeOutDate))
                        return "closeOutDate: string expected";
                return null;
            };

            /**
             * Creates an ObligationInsight message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {greenova.mechanisms.ObligationInsight} ObligationInsight
             */
            ObligationInsight.fromObject = function fromObject(object) {
                if (object instanceof $root.greenova.mechanisms.ObligationInsight)
                    return object;
                var message = new $root.greenova.mechanisms.ObligationInsight();
                if (object.obligationNumber != null)
                    message.obligationNumber = String(object.obligationNumber);
                if (object.dueDate != null)
                    message.dueDate = String(object.dueDate);
                if (object.closeOutDate != null)
                    message.closeOutDate = String(object.closeOutDate);
                return message;
            };

            /**
             * Creates a plain object from an ObligationInsight message. Also converts values to other types if specified.
             * @function toObject
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {greenova.mechanisms.ObligationInsight} message ObligationInsight
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ObligationInsight.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                var object = {};
                if (options.defaults) {
                    object.obligationNumber = "";
                    object.dueDate = "";
                    object.closeOutDate = "";
                }
                if (message.obligationNumber != null && message.hasOwnProperty("obligationNumber"))
                    object.obligationNumber = message.obligationNumber;
                if (message.dueDate != null && message.hasOwnProperty("dueDate"))
                    object.dueDate = message.dueDate;
                if (message.closeOutDate != null && message.hasOwnProperty("closeOutDate"))
                    object.closeOutDate = message.closeOutDate;
                return object;
            };

            /**
             * Converts this ObligationInsight to JSON.
             * @function toJSON
             * @memberof greenova.mechanisms.ObligationInsight
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ObligationInsight.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ObligationInsight
             * @function getTypeUrl
             * @memberof greenova.mechanisms.ObligationInsight
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ObligationInsight.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/greenova.mechanisms.ObligationInsight";
            };

            return ObligationInsight;
        })();

        mechanisms.ObligationInsightResponse = (function() {

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
            function ObligationInsightResponse(properties) {
                this.obligations = [];
                if (properties)
                    for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ObligationInsightResponse mechanismId.
             * @member {number} mechanismId
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.mechanismId = 0;

            /**
             * ObligationInsightResponse status.
             * @member {string} status
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.status = "";

            /**
             * ObligationInsightResponse statusKey.
             * @member {string} statusKey
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.statusKey = "";

            /**
             * ObligationInsightResponse count.
             * @member {number} count
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.count = 0;

            /**
             * ObligationInsightResponse totalCount.
             * @member {number} totalCount
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.totalCount = 0;

            /**
             * ObligationInsightResponse obligations.
             * @member {Array.<greenova.mechanisms.IObligationInsight>} obligations
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.obligations = $util.emptyArray;

            /**
             * ObligationInsightResponse error.
             * @member {string} error
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             */
            ObligationInsightResponse.prototype.error = "";

            /**
             * Creates a new ObligationInsightResponse instance using the specified properties.
             * @function create
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {greenova.mechanisms.IObligationInsightResponse=} [properties] Properties to set
             * @returns {greenova.mechanisms.ObligationInsightResponse} ObligationInsightResponse instance
             */
            ObligationInsightResponse.create = function create(properties) {
                return new ObligationInsightResponse(properties);
            };

            /**
             * Encodes the specified ObligationInsightResponse message. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
             * @function encode
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {greenova.mechanisms.IObligationInsightResponse} message ObligationInsightResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ObligationInsightResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.mechanismId != null && Object.hasOwnProperty.call(message, "mechanismId"))
                    writer.uint32(/* id 1, wireType 0 =*/8).int32(message.mechanismId);
                if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.status);
                if (message.statusKey != null && Object.hasOwnProperty.call(message, "statusKey"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.statusKey);
                if (message.count != null && Object.hasOwnProperty.call(message, "count"))
                    writer.uint32(/* id 4, wireType 0 =*/32).int32(message.count);
                if (message.totalCount != null && Object.hasOwnProperty.call(message, "totalCount"))
                    writer.uint32(/* id 5, wireType 0 =*/40).int32(message.totalCount);
                if (message.obligations != null && message.obligations.length)
                    for (var i = 0; i < message.obligations.length; ++i)
                        $root.greenova.mechanisms.ObligationInsight.encode(message.obligations[i], writer.uint32(/* id 6, wireType 2 =*/50).fork()).ldelim();
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 7, wireType 2 =*/58).string(message.error);
                return writer;
            };

            /**
             * Encodes the specified ObligationInsightResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {greenova.mechanisms.IObligationInsightResponse} message ObligationInsightResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ObligationInsightResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

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
            ObligationInsightResponse.decode = function decode(reader, length, error) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                var end = length === undefined ? reader.len : reader.pos + length, message = new $root.greenova.mechanisms.ObligationInsightResponse();
                while (reader.pos < end) {
                    var tag = reader.uint32();
                    if (tag === error)
                        break;
                    switch (tag >>> 3) {
                    case 1: {
                            message.mechanismId = reader.int32();
                            break;
                        }
                    case 2: {
                            message.status = reader.string();
                            break;
                        }
                    case 3: {
                            message.statusKey = reader.string();
                            break;
                        }
                    case 4: {
                            message.count = reader.int32();
                            break;
                        }
                    case 5: {
                            message.totalCount = reader.int32();
                            break;
                        }
                    case 6: {
                            if (!(message.obligations && message.obligations.length))
                                message.obligations = [];
                            message.obligations.push($root.greenova.mechanisms.ObligationInsight.decode(reader, reader.uint32()));
                            break;
                        }
                    case 7: {
                            message.error = reader.string();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

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
            ObligationInsightResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies an ObligationInsightResponse message.
             * @function verify
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ObligationInsightResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.mechanismId != null && message.hasOwnProperty("mechanismId"))
                    if (!$util.isInteger(message.mechanismId))
                        return "mechanismId: integer expected";
                if (message.status != null && message.hasOwnProperty("status"))
                    if (!$util.isString(message.status))
                        return "status: string expected";
                if (message.statusKey != null && message.hasOwnProperty("statusKey"))
                    if (!$util.isString(message.statusKey))
                        return "statusKey: string expected";
                if (message.count != null && message.hasOwnProperty("count"))
                    if (!$util.isInteger(message.count))
                        return "count: integer expected";
                if (message.totalCount != null && message.hasOwnProperty("totalCount"))
                    if (!$util.isInteger(message.totalCount))
                        return "totalCount: integer expected";
                if (message.obligations != null && message.hasOwnProperty("obligations")) {
                    if (!Array.isArray(message.obligations))
                        return "obligations: array expected";
                    for (var i = 0; i < message.obligations.length; ++i) {
                        var error = $root.greenova.mechanisms.ObligationInsight.verify(message.obligations[i]);
                        if (error)
                            return "obligations." + error;
                    }
                }
                if (message.error != null && message.hasOwnProperty("error"))
                    if (!$util.isString(message.error))
                        return "error: string expected";
                return null;
            };

            /**
             * Creates an ObligationInsightResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {greenova.mechanisms.ObligationInsightResponse} ObligationInsightResponse
             */
            ObligationInsightResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.greenova.mechanisms.ObligationInsightResponse)
                    return object;
                var message = new $root.greenova.mechanisms.ObligationInsightResponse();
                if (object.mechanismId != null)
                    message.mechanismId = object.mechanismId | 0;
                if (object.status != null)
                    message.status = String(object.status);
                if (object.statusKey != null)
                    message.statusKey = String(object.statusKey);
                if (object.count != null)
                    message.count = object.count | 0;
                if (object.totalCount != null)
                    message.totalCount = object.totalCount | 0;
                if (object.obligations) {
                    if (!Array.isArray(object.obligations))
                        throw TypeError(".greenova.mechanisms.ObligationInsightResponse.obligations: array expected");
                    message.obligations = [];
                    for (var i = 0; i < object.obligations.length; ++i) {
                        if (typeof object.obligations[i] !== "object")
                            throw TypeError(".greenova.mechanisms.ObligationInsightResponse.obligations: object expected");
                        message.obligations[i] = $root.greenova.mechanisms.ObligationInsight.fromObject(object.obligations[i]);
                    }
                }
                if (object.error != null)
                    message.error = String(object.error);
                return message;
            };

            /**
             * Creates a plain object from an ObligationInsightResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {greenova.mechanisms.ObligationInsightResponse} message ObligationInsightResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ObligationInsightResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                var object = {};
                if (options.arrays || options.defaults)
                    object.obligations = [];
                if (options.defaults) {
                    object.mechanismId = 0;
                    object.status = "";
                    object.statusKey = "";
                    object.count = 0;
                    object.totalCount = 0;
                    object.error = "";
                }
                if (message.mechanismId != null && message.hasOwnProperty("mechanismId"))
                    object.mechanismId = message.mechanismId;
                if (message.status != null && message.hasOwnProperty("status"))
                    object.status = message.status;
                if (message.statusKey != null && message.hasOwnProperty("statusKey"))
                    object.statusKey = message.statusKey;
                if (message.count != null && message.hasOwnProperty("count"))
                    object.count = message.count;
                if (message.totalCount != null && message.hasOwnProperty("totalCount"))
                    object.totalCount = message.totalCount;
                if (message.obligations && message.obligations.length) {
                    object.obligations = [];
                    for (var j = 0; j < message.obligations.length; ++j)
                        object.obligations[j] = $root.greenova.mechanisms.ObligationInsight.toObject(message.obligations[j], options);
                }
                if (message.error != null && message.hasOwnProperty("error"))
                    object.error = message.error;
                return object;
            };

            /**
             * Converts this ObligationInsightResponse to JSON.
             * @function toJSON
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ObligationInsightResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ObligationInsightResponse
             * @function getTypeUrl
             * @memberof greenova.mechanisms.ObligationInsightResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ObligationInsightResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/greenova.mechanisms.ObligationInsightResponse";
            };

            return ObligationInsightResponse;
        })();

        mechanisms.ChartSegment = (function() {

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
            function ChartSegment(properties) {
                if (properties)
                    for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ChartSegment label.
             * @member {string} label
             * @memberof greenova.mechanisms.ChartSegment
             * @instance
             */
            ChartSegment.prototype.label = "";

            /**
             * ChartSegment value.
             * @member {number} value
             * @memberof greenova.mechanisms.ChartSegment
             * @instance
             */
            ChartSegment.prototype.value = 0;

            /**
             * ChartSegment color.
             * @member {string} color
             * @memberof greenova.mechanisms.ChartSegment
             * @instance
             */
            ChartSegment.prototype.color = "";

            /**
             * Creates a new ChartSegment instance using the specified properties.
             * @function create
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {greenova.mechanisms.IChartSegment=} [properties] Properties to set
             * @returns {greenova.mechanisms.ChartSegment} ChartSegment instance
             */
            ChartSegment.create = function create(properties) {
                return new ChartSegment(properties);
            };

            /**
             * Encodes the specified ChartSegment message. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
             * @function encode
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {greenova.mechanisms.IChartSegment} message ChartSegment message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ChartSegment.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.label != null && Object.hasOwnProperty.call(message, "label"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.label);
                if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                    writer.uint32(/* id 2, wireType 0 =*/16).int32(message.value);
                if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.color);
                return writer;
            };

            /**
             * Encodes the specified ChartSegment message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
             * @function encodeDelimited
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {greenova.mechanisms.IChartSegment} message ChartSegment message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ChartSegment.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

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
            ChartSegment.decode = function decode(reader, length, error) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                var end = length === undefined ? reader.len : reader.pos + length, message = new $root.greenova.mechanisms.ChartSegment();
                while (reader.pos < end) {
                    var tag = reader.uint32();
                    if (tag === error)
                        break;
                    switch (tag >>> 3) {
                    case 1: {
                            message.label = reader.string();
                            break;
                        }
                    case 2: {
                            message.value = reader.int32();
                            break;
                        }
                    case 3: {
                            message.color = reader.string();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

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
            ChartSegment.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a ChartSegment message.
             * @function verify
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ChartSegment.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.label != null && message.hasOwnProperty("label"))
                    if (!$util.isString(message.label))
                        return "label: string expected";
                if (message.value != null && message.hasOwnProperty("value"))
                    if (!$util.isInteger(message.value))
                        return "value: integer expected";
                if (message.color != null && message.hasOwnProperty("color"))
                    if (!$util.isString(message.color))
                        return "color: string expected";
                return null;
            };

            /**
             * Creates a ChartSegment message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {greenova.mechanisms.ChartSegment} ChartSegment
             */
            ChartSegment.fromObject = function fromObject(object) {
                if (object instanceof $root.greenova.mechanisms.ChartSegment)
                    return object;
                var message = new $root.greenova.mechanisms.ChartSegment();
                if (object.label != null)
                    message.label = String(object.label);
                if (object.value != null)
                    message.value = object.value | 0;
                if (object.color != null)
                    message.color = String(object.color);
                return message;
            };

            /**
             * Creates a plain object from a ChartSegment message. Also converts values to other types if specified.
             * @function toObject
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {greenova.mechanisms.ChartSegment} message ChartSegment
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ChartSegment.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                var object = {};
                if (options.defaults) {
                    object.label = "";
                    object.value = 0;
                    object.color = "";
                }
                if (message.label != null && message.hasOwnProperty("label"))
                    object.label = message.label;
                if (message.value != null && message.hasOwnProperty("value"))
                    object.value = message.value;
                if (message.color != null && message.hasOwnProperty("color"))
                    object.color = message.color;
                return object;
            };

            /**
             * Converts this ChartSegment to JSON.
             * @function toJSON
             * @memberof greenova.mechanisms.ChartSegment
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ChartSegment.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ChartSegment
             * @function getTypeUrl
             * @memberof greenova.mechanisms.ChartSegment
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ChartSegment.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/greenova.mechanisms.ChartSegment";
            };

            return ChartSegment;
        })();

        mechanisms.ChartData = (function() {

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
            function ChartData(properties) {
                this.segments = [];
                if (properties)
                    for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ChartData segments.
             * @member {Array.<greenova.mechanisms.IChartSegment>} segments
             * @memberof greenova.mechanisms.ChartData
             * @instance
             */
            ChartData.prototype.segments = $util.emptyArray;

            /**
             * ChartData mechanismId.
             * @member {number} mechanismId
             * @memberof greenova.mechanisms.ChartData
             * @instance
             */
            ChartData.prototype.mechanismId = 0;

            /**
             * ChartData mechanismName.
             * @member {string} mechanismName
             * @memberof greenova.mechanisms.ChartData
             * @instance
             */
            ChartData.prototype.mechanismName = "";

            /**
             * Creates a new ChartData instance using the specified properties.
             * @function create
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {greenova.mechanisms.IChartData=} [properties] Properties to set
             * @returns {greenova.mechanisms.ChartData} ChartData instance
             */
            ChartData.create = function create(properties) {
                return new ChartData(properties);
            };

            /**
             * Encodes the specified ChartData message. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
             * @function encode
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {greenova.mechanisms.IChartData} message ChartData message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ChartData.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.segments != null && message.segments.length)
                    for (var i = 0; i < message.segments.length; ++i)
                        $root.greenova.mechanisms.ChartSegment.encode(message.segments[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.mechanismId != null && Object.hasOwnProperty.call(message, "mechanismId"))
                    writer.uint32(/* id 2, wireType 0 =*/16).int32(message.mechanismId);
                if (message.mechanismName != null && Object.hasOwnProperty.call(message, "mechanismName"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.mechanismName);
                return writer;
            };

            /**
             * Encodes the specified ChartData message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
             * @function encodeDelimited
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {greenova.mechanisms.IChartData} message ChartData message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ChartData.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

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
            ChartData.decode = function decode(reader, length, error) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                var end = length === undefined ? reader.len : reader.pos + length, message = new $root.greenova.mechanisms.ChartData();
                while (reader.pos < end) {
                    var tag = reader.uint32();
                    if (tag === error)
                        break;
                    switch (tag >>> 3) {
                    case 1: {
                            if (!(message.segments && message.segments.length))
                                message.segments = [];
                            message.segments.push($root.greenova.mechanisms.ChartSegment.decode(reader, reader.uint32()));
                            break;
                        }
                    case 2: {
                            message.mechanismId = reader.int32();
                            break;
                        }
                    case 3: {
                            message.mechanismName = reader.string();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

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
            ChartData.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a ChartData message.
             * @function verify
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ChartData.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.segments != null && message.hasOwnProperty("segments")) {
                    if (!Array.isArray(message.segments))
                        return "segments: array expected";
                    for (var i = 0; i < message.segments.length; ++i) {
                        var error = $root.greenova.mechanisms.ChartSegment.verify(message.segments[i]);
                        if (error)
                            return "segments." + error;
                    }
                }
                if (message.mechanismId != null && message.hasOwnProperty("mechanismId"))
                    if (!$util.isInteger(message.mechanismId))
                        return "mechanismId: integer expected";
                if (message.mechanismName != null && message.hasOwnProperty("mechanismName"))
                    if (!$util.isString(message.mechanismName))
                        return "mechanismName: string expected";
                return null;
            };

            /**
             * Creates a ChartData message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {greenova.mechanisms.ChartData} ChartData
             */
            ChartData.fromObject = function fromObject(object) {
                if (object instanceof $root.greenova.mechanisms.ChartData)
                    return object;
                var message = new $root.greenova.mechanisms.ChartData();
                if (object.segments) {
                    if (!Array.isArray(object.segments))
                        throw TypeError(".greenova.mechanisms.ChartData.segments: array expected");
                    message.segments = [];
                    for (var i = 0; i < object.segments.length; ++i) {
                        if (typeof object.segments[i] !== "object")
                            throw TypeError(".greenova.mechanisms.ChartData.segments: object expected");
                        message.segments[i] = $root.greenova.mechanisms.ChartSegment.fromObject(object.segments[i]);
                    }
                }
                if (object.mechanismId != null)
                    message.mechanismId = object.mechanismId | 0;
                if (object.mechanismName != null)
                    message.mechanismName = String(object.mechanismName);
                return message;
            };

            /**
             * Creates a plain object from a ChartData message. Also converts values to other types if specified.
             * @function toObject
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {greenova.mechanisms.ChartData} message ChartData
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ChartData.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                var object = {};
                if (options.arrays || options.defaults)
                    object.segments = [];
                if (options.defaults) {
                    object.mechanismId = 0;
                    object.mechanismName = "";
                }
                if (message.segments && message.segments.length) {
                    object.segments = [];
                    for (var j = 0; j < message.segments.length; ++j)
                        object.segments[j] = $root.greenova.mechanisms.ChartSegment.toObject(message.segments[j], options);
                }
                if (message.mechanismId != null && message.hasOwnProperty("mechanismId"))
                    object.mechanismId = message.mechanismId;
                if (message.mechanismName != null && message.hasOwnProperty("mechanismName"))
                    object.mechanismName = message.mechanismName;
                return object;
            };

            /**
             * Converts this ChartData to JSON.
             * @function toJSON
             * @memberof greenova.mechanisms.ChartData
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ChartData.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ChartData
             * @function getTypeUrl
             * @memberof greenova.mechanisms.ChartData
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ChartData.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/greenova.mechanisms.ChartData";
            };

            return ChartData;
        })();

        mechanisms.ChartResponse = (function() {

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
            function ChartResponse(properties) {
                this.charts = [];
                if (properties)
                    for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ChartResponse charts.
             * @member {Array.<greenova.mechanisms.IChartData>} charts
             * @memberof greenova.mechanisms.ChartResponse
             * @instance
             */
            ChartResponse.prototype.charts = $util.emptyArray;

            /**
             * ChartResponse error.
             * @member {string} error
             * @memberof greenova.mechanisms.ChartResponse
             * @instance
             */
            ChartResponse.prototype.error = "";

            /**
             * Creates a new ChartResponse instance using the specified properties.
             * @function create
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {greenova.mechanisms.IChartResponse=} [properties] Properties to set
             * @returns {greenova.mechanisms.ChartResponse} ChartResponse instance
             */
            ChartResponse.create = function create(properties) {
                return new ChartResponse(properties);
            };

            /**
             * Encodes the specified ChartResponse message. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
             * @function encode
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {greenova.mechanisms.IChartResponse} message ChartResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ChartResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.charts != null && message.charts.length)
                    for (var i = 0; i < message.charts.length; ++i)
                        $root.greenova.mechanisms.ChartData.encode(message.charts[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.error);
                return writer;
            };

            /**
             * Encodes the specified ChartResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {greenova.mechanisms.IChartResponse} message ChartResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ChartResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

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
            ChartResponse.decode = function decode(reader, length, error) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                var end = length === undefined ? reader.len : reader.pos + length, message = new $root.greenova.mechanisms.ChartResponse();
                while (reader.pos < end) {
                    var tag = reader.uint32();
                    if (tag === error)
                        break;
                    switch (tag >>> 3) {
                    case 1: {
                            if (!(message.charts && message.charts.length))
                                message.charts = [];
                            message.charts.push($root.greenova.mechanisms.ChartData.decode(reader, reader.uint32()));
                            break;
                        }
                    case 2: {
                            message.error = reader.string();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

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
            ChartResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a ChartResponse message.
             * @function verify
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ChartResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.charts != null && message.hasOwnProperty("charts")) {
                    if (!Array.isArray(message.charts))
                        return "charts: array expected";
                    for (var i = 0; i < message.charts.length; ++i) {
                        var error = $root.greenova.mechanisms.ChartData.verify(message.charts[i]);
                        if (error)
                            return "charts." + error;
                    }
                }
                if (message.error != null && message.hasOwnProperty("error"))
                    if (!$util.isString(message.error))
                        return "error: string expected";
                return null;
            };

            /**
             * Creates a ChartResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {greenova.mechanisms.ChartResponse} ChartResponse
             */
            ChartResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.greenova.mechanisms.ChartResponse)
                    return object;
                var message = new $root.greenova.mechanisms.ChartResponse();
                if (object.charts) {
                    if (!Array.isArray(object.charts))
                        throw TypeError(".greenova.mechanisms.ChartResponse.charts: array expected");
                    message.charts = [];
                    for (var i = 0; i < object.charts.length; ++i) {
                        if (typeof object.charts[i] !== "object")
                            throw TypeError(".greenova.mechanisms.ChartResponse.charts: object expected");
                        message.charts[i] = $root.greenova.mechanisms.ChartData.fromObject(object.charts[i]);
                    }
                }
                if (object.error != null)
                    message.error = String(object.error);
                return message;
            };

            /**
             * Creates a plain object from a ChartResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {greenova.mechanisms.ChartResponse} message ChartResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ChartResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                var object = {};
                if (options.arrays || options.defaults)
                    object.charts = [];
                if (options.defaults)
                    object.error = "";
                if (message.charts && message.charts.length) {
                    object.charts = [];
                    for (var j = 0; j < message.charts.length; ++j)
                        object.charts[j] = $root.greenova.mechanisms.ChartData.toObject(message.charts[j], options);
                }
                if (message.error != null && message.hasOwnProperty("error"))
                    object.error = message.error;
                return object;
            };

            /**
             * Converts this ChartResponse to JSON.
             * @function toJSON
             * @memberof greenova.mechanisms.ChartResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ChartResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ChartResponse
             * @function getTypeUrl
             * @memberof greenova.mechanisms.ChartResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ChartResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/greenova.mechanisms.ChartResponse";
            };

            return ChartResponse;
        })();

        return mechanisms;
    })();

    return greenova;
})();

$root.feedback = (function() {

    /**
     * Namespace feedback.
     * @exports feedback
     * @namespace
     */
    var feedback = {};

    feedback.BugReportProto = (function() {

        /**
         * Properties of a BugReportProto.
         * @memberof feedback
         * @interface IBugReportProto
         * @property {number|null} [id] BugReportProto id
         * @property {string|null} [title] BugReportProto title
         * @property {string|null} [description] BugReportProto description
         * @property {string|null} [applicationVersion] BugReportProto applicationVersion
         * @property {string|null} [operatingSystem] BugReportProto operatingSystem
         * @property {string|null} [browser] BugReportProto browser
         * @property {string|null} [deviceType] BugReportProto deviceType
         * @property {string|null} [stepsToReproduce] BugReportProto stepsToReproduce
         * @property {string|null} [expectedBehavior] BugReportProto expectedBehavior
         * @property {string|null} [actualBehavior] BugReportProto actualBehavior
         * @property {string|null} [errorMessages] BugReportProto errorMessages
         * @property {string|null} [traceReport] BugReportProto traceReport
         * @property {feedback.BugReportProto.Frequency|null} [frequency] BugReportProto frequency
         * @property {feedback.BugReportProto.Severity|null} [impactSeverity] BugReportProto impactSeverity
         * @property {feedback.BugReportProto.Severity|null} [adminSeverity] BugReportProto adminSeverity
         * @property {string|null} [userImpact] BugReportProto userImpact
         * @property {string|null} [workarounds] BugReportProto workarounds
         * @property {string|null} [additionalComments] BugReportProto additionalComments
         * @property {number|null} [userId] BugReportProto userId
         * @property {string|null} [username] BugReportProto username
         * @property {number|Long|null} [createdAt] BugReportProto createdAt
         * @property {number|Long|null} [updatedAt] BugReportProto updatedAt
         * @property {string|null} [githubIssueUrl] BugReportProto githubIssueUrl
         * @property {feedback.BugReportProto.Status|null} [status] BugReportProto status
         * @property {string|null} [adminComment] BugReportProto adminComment
         */

        /**
         * Constructs a new BugReportProto.
         * @memberof feedback
         * @classdesc Represents a BugReportProto.
         * @implements IBugReportProto
         * @constructor
         * @param {feedback.IBugReportProto=} [properties] Properties to set
         */
        function BugReportProto(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BugReportProto id.
         * @member {number} id
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.id = 0;

        /**
         * BugReportProto title.
         * @member {string} title
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.title = "";

        /**
         * BugReportProto description.
         * @member {string} description
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.description = "";

        /**
         * BugReportProto applicationVersion.
         * @member {string} applicationVersion
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.applicationVersion = "";

        /**
         * BugReportProto operatingSystem.
         * @member {string} operatingSystem
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.operatingSystem = "";

        /**
         * BugReportProto browser.
         * @member {string} browser
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.browser = "";

        /**
         * BugReportProto deviceType.
         * @member {string} deviceType
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.deviceType = "";

        /**
         * BugReportProto stepsToReproduce.
         * @member {string} stepsToReproduce
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.stepsToReproduce = "";

        /**
         * BugReportProto expectedBehavior.
         * @member {string} expectedBehavior
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.expectedBehavior = "";

        /**
         * BugReportProto actualBehavior.
         * @member {string} actualBehavior
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.actualBehavior = "";

        /**
         * BugReportProto errorMessages.
         * @member {string} errorMessages
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.errorMessages = "";

        /**
         * BugReportProto traceReport.
         * @member {string} traceReport
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.traceReport = "";

        /**
         * BugReportProto frequency.
         * @member {feedback.BugReportProto.Frequency} frequency
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.frequency = 0;

        /**
         * BugReportProto impactSeverity.
         * @member {feedback.BugReportProto.Severity} impactSeverity
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.impactSeverity = 0;

        /**
         * BugReportProto adminSeverity.
         * @member {feedback.BugReportProto.Severity} adminSeverity
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.adminSeverity = 0;

        /**
         * BugReportProto userImpact.
         * @member {string} userImpact
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.userImpact = "";

        /**
         * BugReportProto workarounds.
         * @member {string} workarounds
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.workarounds = "";

        /**
         * BugReportProto additionalComments.
         * @member {string} additionalComments
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.additionalComments = "";

        /**
         * BugReportProto userId.
         * @member {number} userId
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.userId = 0;

        /**
         * BugReportProto username.
         * @member {string} username
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.username = "";

        /**
         * BugReportProto createdAt.
         * @member {number|Long} createdAt
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.createdAt = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * BugReportProto updatedAt.
         * @member {number|Long} updatedAt
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.updatedAt = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * BugReportProto githubIssueUrl.
         * @member {string} githubIssueUrl
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.githubIssueUrl = "";

        /**
         * BugReportProto status.
         * @member {feedback.BugReportProto.Status} status
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.status = 0;

        /**
         * BugReportProto adminComment.
         * @member {string} adminComment
         * @memberof feedback.BugReportProto
         * @instance
         */
        BugReportProto.prototype.adminComment = "";

        /**
         * Creates a new BugReportProto instance using the specified properties.
         * @function create
         * @memberof feedback.BugReportProto
         * @static
         * @param {feedback.IBugReportProto=} [properties] Properties to set
         * @returns {feedback.BugReportProto} BugReportProto instance
         */
        BugReportProto.create = function create(properties) {
            return new BugReportProto(properties);
        };

        /**
         * Encodes the specified BugReportProto message. Does not implicitly {@link feedback.BugReportProto.verify|verify} messages.
         * @function encode
         * @memberof feedback.BugReportProto
         * @static
         * @param {feedback.IBugReportProto} message BugReportProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BugReportProto.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 0 =*/8).int32(message.id);
            if (message.title != null && Object.hasOwnProperty.call(message, "title"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.title);
            if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.description);
            if (message.applicationVersion != null && Object.hasOwnProperty.call(message, "applicationVersion"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.applicationVersion);
            if (message.operatingSystem != null && Object.hasOwnProperty.call(message, "operatingSystem"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.operatingSystem);
            if (message.browser != null && Object.hasOwnProperty.call(message, "browser"))
                writer.uint32(/* id 6, wireType 2 =*/50).string(message.browser);
            if (message.deviceType != null && Object.hasOwnProperty.call(message, "deviceType"))
                writer.uint32(/* id 7, wireType 2 =*/58).string(message.deviceType);
            if (message.stepsToReproduce != null && Object.hasOwnProperty.call(message, "stepsToReproduce"))
                writer.uint32(/* id 8, wireType 2 =*/66).string(message.stepsToReproduce);
            if (message.expectedBehavior != null && Object.hasOwnProperty.call(message, "expectedBehavior"))
                writer.uint32(/* id 9, wireType 2 =*/74).string(message.expectedBehavior);
            if (message.actualBehavior != null && Object.hasOwnProperty.call(message, "actualBehavior"))
                writer.uint32(/* id 10, wireType 2 =*/82).string(message.actualBehavior);
            if (message.errorMessages != null && Object.hasOwnProperty.call(message, "errorMessages"))
                writer.uint32(/* id 11, wireType 2 =*/90).string(message.errorMessages);
            if (message.traceReport != null && Object.hasOwnProperty.call(message, "traceReport"))
                writer.uint32(/* id 12, wireType 2 =*/98).string(message.traceReport);
            if (message.frequency != null && Object.hasOwnProperty.call(message, "frequency"))
                writer.uint32(/* id 13, wireType 0 =*/104).int32(message.frequency);
            if (message.impactSeverity != null && Object.hasOwnProperty.call(message, "impactSeverity"))
                writer.uint32(/* id 14, wireType 0 =*/112).int32(message.impactSeverity);
            if (message.adminSeverity != null && Object.hasOwnProperty.call(message, "adminSeverity"))
                writer.uint32(/* id 15, wireType 0 =*/120).int32(message.adminSeverity);
            if (message.userImpact != null && Object.hasOwnProperty.call(message, "userImpact"))
                writer.uint32(/* id 16, wireType 2 =*/130).string(message.userImpact);
            if (message.workarounds != null && Object.hasOwnProperty.call(message, "workarounds"))
                writer.uint32(/* id 17, wireType 2 =*/138).string(message.workarounds);
            if (message.additionalComments != null && Object.hasOwnProperty.call(message, "additionalComments"))
                writer.uint32(/* id 18, wireType 2 =*/146).string(message.additionalComments);
            if (message.userId != null && Object.hasOwnProperty.call(message, "userId"))
                writer.uint32(/* id 19, wireType 0 =*/152).int32(message.userId);
            if (message.username != null && Object.hasOwnProperty.call(message, "username"))
                writer.uint32(/* id 20, wireType 2 =*/162).string(message.username);
            if (message.createdAt != null && Object.hasOwnProperty.call(message, "createdAt"))
                writer.uint32(/* id 21, wireType 0 =*/168).int64(message.createdAt);
            if (message.updatedAt != null && Object.hasOwnProperty.call(message, "updatedAt"))
                writer.uint32(/* id 22, wireType 0 =*/176).int64(message.updatedAt);
            if (message.githubIssueUrl != null && Object.hasOwnProperty.call(message, "githubIssueUrl"))
                writer.uint32(/* id 23, wireType 2 =*/186).string(message.githubIssueUrl);
            if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                writer.uint32(/* id 24, wireType 0 =*/192).int32(message.status);
            if (message.adminComment != null && Object.hasOwnProperty.call(message, "adminComment"))
                writer.uint32(/* id 25, wireType 2 =*/202).string(message.adminComment);
            return writer;
        };

        /**
         * Encodes the specified BugReportProto message, length delimited. Does not implicitly {@link feedback.BugReportProto.verify|verify} messages.
         * @function encodeDelimited
         * @memberof feedback.BugReportProto
         * @static
         * @param {feedback.IBugReportProto} message BugReportProto message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BugReportProto.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BugReportProto message from the specified reader or buffer.
         * @function decode
         * @memberof feedback.BugReportProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {feedback.BugReportProto} BugReportProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BugReportProto.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.feedback.BugReportProto();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.int32();
                        break;
                    }
                case 2: {
                        message.title = reader.string();
                        break;
                    }
                case 3: {
                        message.description = reader.string();
                        break;
                    }
                case 4: {
                        message.applicationVersion = reader.string();
                        break;
                    }
                case 5: {
                        message.operatingSystem = reader.string();
                        break;
                    }
                case 6: {
                        message.browser = reader.string();
                        break;
                    }
                case 7: {
                        message.deviceType = reader.string();
                        break;
                    }
                case 8: {
                        message.stepsToReproduce = reader.string();
                        break;
                    }
                case 9: {
                        message.expectedBehavior = reader.string();
                        break;
                    }
                case 10: {
                        message.actualBehavior = reader.string();
                        break;
                    }
                case 11: {
                        message.errorMessages = reader.string();
                        break;
                    }
                case 12: {
                        message.traceReport = reader.string();
                        break;
                    }
                case 13: {
                        message.frequency = reader.int32();
                        break;
                    }
                case 14: {
                        message.impactSeverity = reader.int32();
                        break;
                    }
                case 15: {
                        message.adminSeverity = reader.int32();
                        break;
                    }
                case 16: {
                        message.userImpact = reader.string();
                        break;
                    }
                case 17: {
                        message.workarounds = reader.string();
                        break;
                    }
                case 18: {
                        message.additionalComments = reader.string();
                        break;
                    }
                case 19: {
                        message.userId = reader.int32();
                        break;
                    }
                case 20: {
                        message.username = reader.string();
                        break;
                    }
                case 21: {
                        message.createdAt = reader.int64();
                        break;
                    }
                case 22: {
                        message.updatedAt = reader.int64();
                        break;
                    }
                case 23: {
                        message.githubIssueUrl = reader.string();
                        break;
                    }
                case 24: {
                        message.status = reader.int32();
                        break;
                    }
                case 25: {
                        message.adminComment = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BugReportProto message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof feedback.BugReportProto
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {feedback.BugReportProto} BugReportProto
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BugReportProto.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BugReportProto message.
         * @function verify
         * @memberof feedback.BugReportProto
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BugReportProto.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isInteger(message.id))
                    return "id: integer expected";
            if (message.title != null && message.hasOwnProperty("title"))
                if (!$util.isString(message.title))
                    return "title: string expected";
            if (message.description != null && message.hasOwnProperty("description"))
                if (!$util.isString(message.description))
                    return "description: string expected";
            if (message.applicationVersion != null && message.hasOwnProperty("applicationVersion"))
                if (!$util.isString(message.applicationVersion))
                    return "applicationVersion: string expected";
            if (message.operatingSystem != null && message.hasOwnProperty("operatingSystem"))
                if (!$util.isString(message.operatingSystem))
                    return "operatingSystem: string expected";
            if (message.browser != null && message.hasOwnProperty("browser"))
                if (!$util.isString(message.browser))
                    return "browser: string expected";
            if (message.deviceType != null && message.hasOwnProperty("deviceType"))
                if (!$util.isString(message.deviceType))
                    return "deviceType: string expected";
            if (message.stepsToReproduce != null && message.hasOwnProperty("stepsToReproduce"))
                if (!$util.isString(message.stepsToReproduce))
                    return "stepsToReproduce: string expected";
            if (message.expectedBehavior != null && message.hasOwnProperty("expectedBehavior"))
                if (!$util.isString(message.expectedBehavior))
                    return "expectedBehavior: string expected";
            if (message.actualBehavior != null && message.hasOwnProperty("actualBehavior"))
                if (!$util.isString(message.actualBehavior))
                    return "actualBehavior: string expected";
            if (message.errorMessages != null && message.hasOwnProperty("errorMessages"))
                if (!$util.isString(message.errorMessages))
                    return "errorMessages: string expected";
            if (message.traceReport != null && message.hasOwnProperty("traceReport"))
                if (!$util.isString(message.traceReport))
                    return "traceReport: string expected";
            if (message.frequency != null && message.hasOwnProperty("frequency"))
                switch (message.frequency) {
                default:
                    return "frequency: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                    break;
                }
            if (message.impactSeverity != null && message.hasOwnProperty("impactSeverity"))
                switch (message.impactSeverity) {
                default:
                    return "impactSeverity: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                    break;
                }
            if (message.adminSeverity != null && message.hasOwnProperty("adminSeverity"))
                switch (message.adminSeverity) {
                default:
                    return "adminSeverity: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                    break;
                }
            if (message.userImpact != null && message.hasOwnProperty("userImpact"))
                if (!$util.isString(message.userImpact))
                    return "userImpact: string expected";
            if (message.workarounds != null && message.hasOwnProperty("workarounds"))
                if (!$util.isString(message.workarounds))
                    return "workarounds: string expected";
            if (message.additionalComments != null && message.hasOwnProperty("additionalComments"))
                if (!$util.isString(message.additionalComments))
                    return "additionalComments: string expected";
            if (message.userId != null && message.hasOwnProperty("userId"))
                if (!$util.isInteger(message.userId))
                    return "userId: integer expected";
            if (message.username != null && message.hasOwnProperty("username"))
                if (!$util.isString(message.username))
                    return "username: string expected";
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (!$util.isInteger(message.createdAt) && !(message.createdAt && $util.isInteger(message.createdAt.low) && $util.isInteger(message.createdAt.high)))
                    return "createdAt: integer|Long expected";
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (!$util.isInteger(message.updatedAt) && !(message.updatedAt && $util.isInteger(message.updatedAt.low) && $util.isInteger(message.updatedAt.high)))
                    return "updatedAt: integer|Long expected";
            if (message.githubIssueUrl != null && message.hasOwnProperty("githubIssueUrl"))
                if (!$util.isString(message.githubIssueUrl))
                    return "githubIssueUrl: string expected";
            if (message.status != null && message.hasOwnProperty("status"))
                switch (message.status) {
                default:
                    return "status: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                    break;
                }
            if (message.adminComment != null && message.hasOwnProperty("adminComment"))
                if (!$util.isString(message.adminComment))
                    return "adminComment: string expected";
            return null;
        };

        /**
         * Creates a BugReportProto message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof feedback.BugReportProto
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {feedback.BugReportProto} BugReportProto
         */
        BugReportProto.fromObject = function fromObject(object) {
            if (object instanceof $root.feedback.BugReportProto)
                return object;
            var message = new $root.feedback.BugReportProto();
            if (object.id != null)
                message.id = object.id | 0;
            if (object.title != null)
                message.title = String(object.title);
            if (object.description != null)
                message.description = String(object.description);
            if (object.applicationVersion != null)
                message.applicationVersion = String(object.applicationVersion);
            if (object.operatingSystem != null)
                message.operatingSystem = String(object.operatingSystem);
            if (object.browser != null)
                message.browser = String(object.browser);
            if (object.deviceType != null)
                message.deviceType = String(object.deviceType);
            if (object.stepsToReproduce != null)
                message.stepsToReproduce = String(object.stepsToReproduce);
            if (object.expectedBehavior != null)
                message.expectedBehavior = String(object.expectedBehavior);
            if (object.actualBehavior != null)
                message.actualBehavior = String(object.actualBehavior);
            if (object.errorMessages != null)
                message.errorMessages = String(object.errorMessages);
            if (object.traceReport != null)
                message.traceReport = String(object.traceReport);
            switch (object.frequency) {
            default:
                if (typeof object.frequency === "number") {
                    message.frequency = object.frequency;
                    break;
                }
                break;
            case "FREQUENCY_UNKNOWN_UNSPECIFIED":
            case 0:
                message.frequency = 0;
                break;
            case "FREQUENCY_ALWAYS":
            case 1:
                message.frequency = 1;
                break;
            case "FREQUENCY_FREQUENTLY":
            case 2:
                message.frequency = 2;
                break;
            case "FREQUENCY_OCCASIONALLY":
            case 3:
                message.frequency = 3;
                break;
            case "FREQUENCY_RARELY":
            case 4:
                message.frequency = 4;
                break;
            }
            switch (object.impactSeverity) {
            default:
                if (typeof object.impactSeverity === "number") {
                    message.impactSeverity = object.impactSeverity;
                    break;
                }
                break;
            case "SEVERITY_UNDEFINED_UNSPECIFIED":
            case 0:
                message.impactSeverity = 0;
                break;
            case "SEVERITY_LOW":
            case 1:
                message.impactSeverity = 1;
                break;
            case "SEVERITY_MEDIUM":
            case 2:
                message.impactSeverity = 2;
                break;
            case "SEVERITY_HIGH":
            case 3:
                message.impactSeverity = 3;
                break;
            case "SEVERITY_CRITICAL":
            case 4:
                message.impactSeverity = 4;
                break;
            }
            switch (object.adminSeverity) {
            default:
                if (typeof object.adminSeverity === "number") {
                    message.adminSeverity = object.adminSeverity;
                    break;
                }
                break;
            case "SEVERITY_UNDEFINED_UNSPECIFIED":
            case 0:
                message.adminSeverity = 0;
                break;
            case "SEVERITY_LOW":
            case 1:
                message.adminSeverity = 1;
                break;
            case "SEVERITY_MEDIUM":
            case 2:
                message.adminSeverity = 2;
                break;
            case "SEVERITY_HIGH":
            case 3:
                message.adminSeverity = 3;
                break;
            case "SEVERITY_CRITICAL":
            case 4:
                message.adminSeverity = 4;
                break;
            }
            if (object.userImpact != null)
                message.userImpact = String(object.userImpact);
            if (object.workarounds != null)
                message.workarounds = String(object.workarounds);
            if (object.additionalComments != null)
                message.additionalComments = String(object.additionalComments);
            if (object.userId != null)
                message.userId = object.userId | 0;
            if (object.username != null)
                message.username = String(object.username);
            if (object.createdAt != null)
                if ($util.Long)
                    (message.createdAt = $util.Long.fromValue(object.createdAt)).unsigned = false;
                else if (typeof object.createdAt === "string")
                    message.createdAt = parseInt(object.createdAt, 10);
                else if (typeof object.createdAt === "number")
                    message.createdAt = object.createdAt;
                else if (typeof object.createdAt === "object")
                    message.createdAt = new $util.LongBits(object.createdAt.low >>> 0, object.createdAt.high >>> 0).toNumber();
            if (object.updatedAt != null)
                if ($util.Long)
                    (message.updatedAt = $util.Long.fromValue(object.updatedAt)).unsigned = false;
                else if (typeof object.updatedAt === "string")
                    message.updatedAt = parseInt(object.updatedAt, 10);
                else if (typeof object.updatedAt === "number")
                    message.updatedAt = object.updatedAt;
                else if (typeof object.updatedAt === "object")
                    message.updatedAt = new $util.LongBits(object.updatedAt.low >>> 0, object.updatedAt.high >>> 0).toNumber();
            if (object.githubIssueUrl != null)
                message.githubIssueUrl = String(object.githubIssueUrl);
            switch (object.status) {
            default:
                if (typeof object.status === "number") {
                    message.status = object.status;
                    break;
                }
                break;
            case "STATUS_UNSPECIFIED":
            case 0:
                message.status = 0;
                break;
            case "STATUS_OPEN":
            case 1:
                message.status = 1;
                break;
            case "STATUS_IN_PROGRESS":
            case 2:
                message.status = 2;
                break;
            case "STATUS_RESOLVED":
            case 3:
                message.status = 3;
                break;
            case "STATUS_CLOSED":
            case 4:
                message.status = 4;
                break;
            case "STATUS_REJECTED":
            case 5:
                message.status = 5;
                break;
            }
            if (object.adminComment != null)
                message.adminComment = String(object.adminComment);
            return message;
        };

        /**
         * Creates a plain object from a BugReportProto message. Also converts values to other types if specified.
         * @function toObject
         * @memberof feedback.BugReportProto
         * @static
         * @param {feedback.BugReportProto} message BugReportProto
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BugReportProto.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.id = 0;
                object.title = "";
                object.description = "";
                object.applicationVersion = "";
                object.operatingSystem = "";
                object.browser = "";
                object.deviceType = "";
                object.stepsToReproduce = "";
                object.expectedBehavior = "";
                object.actualBehavior = "";
                object.errorMessages = "";
                object.traceReport = "";
                object.frequency = options.enums === String ? "FREQUENCY_UNKNOWN_UNSPECIFIED" : 0;
                object.impactSeverity = options.enums === String ? "SEVERITY_UNDEFINED_UNSPECIFIED" : 0;
                object.adminSeverity = options.enums === String ? "SEVERITY_UNDEFINED_UNSPECIFIED" : 0;
                object.userImpact = "";
                object.workarounds = "";
                object.additionalComments = "";
                object.userId = 0;
                object.username = "";
                if ($util.Long) {
                    var long = new $util.Long(0, 0, false);
                    object.createdAt = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.createdAt = options.longs === String ? "0" : 0;
                if ($util.Long) {
                    var long = new $util.Long(0, 0, false);
                    object.updatedAt = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.updatedAt = options.longs === String ? "0" : 0;
                object.githubIssueUrl = "";
                object.status = options.enums === String ? "STATUS_UNSPECIFIED" : 0;
                object.adminComment = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.title != null && message.hasOwnProperty("title"))
                object.title = message.title;
            if (message.description != null && message.hasOwnProperty("description"))
                object.description = message.description;
            if (message.applicationVersion != null && message.hasOwnProperty("applicationVersion"))
                object.applicationVersion = message.applicationVersion;
            if (message.operatingSystem != null && message.hasOwnProperty("operatingSystem"))
                object.operatingSystem = message.operatingSystem;
            if (message.browser != null && message.hasOwnProperty("browser"))
                object.browser = message.browser;
            if (message.deviceType != null && message.hasOwnProperty("deviceType"))
                object.deviceType = message.deviceType;
            if (message.stepsToReproduce != null && message.hasOwnProperty("stepsToReproduce"))
                object.stepsToReproduce = message.stepsToReproduce;
            if (message.expectedBehavior != null && message.hasOwnProperty("expectedBehavior"))
                object.expectedBehavior = message.expectedBehavior;
            if (message.actualBehavior != null && message.hasOwnProperty("actualBehavior"))
                object.actualBehavior = message.actualBehavior;
            if (message.errorMessages != null && message.hasOwnProperty("errorMessages"))
                object.errorMessages = message.errorMessages;
            if (message.traceReport != null && message.hasOwnProperty("traceReport"))
                object.traceReport = message.traceReport;
            if (message.frequency != null && message.hasOwnProperty("frequency"))
                object.frequency = options.enums === String ? $root.feedback.BugReportProto.Frequency[message.frequency] === undefined ? message.frequency : $root.feedback.BugReportProto.Frequency[message.frequency] : message.frequency;
            if (message.impactSeverity != null && message.hasOwnProperty("impactSeverity"))
                object.impactSeverity = options.enums === String ? $root.feedback.BugReportProto.Severity[message.impactSeverity] === undefined ? message.impactSeverity : $root.feedback.BugReportProto.Severity[message.impactSeverity] : message.impactSeverity;
            if (message.adminSeverity != null && message.hasOwnProperty("adminSeverity"))
                object.adminSeverity = options.enums === String ? $root.feedback.BugReportProto.Severity[message.adminSeverity] === undefined ? message.adminSeverity : $root.feedback.BugReportProto.Severity[message.adminSeverity] : message.adminSeverity;
            if (message.userImpact != null && message.hasOwnProperty("userImpact"))
                object.userImpact = message.userImpact;
            if (message.workarounds != null && message.hasOwnProperty("workarounds"))
                object.workarounds = message.workarounds;
            if (message.additionalComments != null && message.hasOwnProperty("additionalComments"))
                object.additionalComments = message.additionalComments;
            if (message.userId != null && message.hasOwnProperty("userId"))
                object.userId = message.userId;
            if (message.username != null && message.hasOwnProperty("username"))
                object.username = message.username;
            if (message.createdAt != null && message.hasOwnProperty("createdAt"))
                if (typeof message.createdAt === "number")
                    object.createdAt = options.longs === String ? String(message.createdAt) : message.createdAt;
                else
                    object.createdAt = options.longs === String ? $util.Long.prototype.toString.call(message.createdAt) : options.longs === Number ? new $util.LongBits(message.createdAt.low >>> 0, message.createdAt.high >>> 0).toNumber() : message.createdAt;
            if (message.updatedAt != null && message.hasOwnProperty("updatedAt"))
                if (typeof message.updatedAt === "number")
                    object.updatedAt = options.longs === String ? String(message.updatedAt) : message.updatedAt;
                else
                    object.updatedAt = options.longs === String ? $util.Long.prototype.toString.call(message.updatedAt) : options.longs === Number ? new $util.LongBits(message.updatedAt.low >>> 0, message.updatedAt.high >>> 0).toNumber() : message.updatedAt;
            if (message.githubIssueUrl != null && message.hasOwnProperty("githubIssueUrl"))
                object.githubIssueUrl = message.githubIssueUrl;
            if (message.status != null && message.hasOwnProperty("status"))
                object.status = options.enums === String ? $root.feedback.BugReportProto.Status[message.status] === undefined ? message.status : $root.feedback.BugReportProto.Status[message.status] : message.status;
            if (message.adminComment != null && message.hasOwnProperty("adminComment"))
                object.adminComment = message.adminComment;
            return object;
        };

        /**
         * Converts this BugReportProto to JSON.
         * @function toJSON
         * @memberof feedback.BugReportProto
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BugReportProto.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BugReportProto
         * @function getTypeUrl
         * @memberof feedback.BugReportProto
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BugReportProto.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/feedback.BugReportProto";
        };

        /**
         * Frequency enum.
         * @name feedback.BugReportProto.Frequency
         * @enum {number}
         * @property {number} FREQUENCY_UNKNOWN_UNSPECIFIED=0 FREQUENCY_UNKNOWN_UNSPECIFIED value
         * @property {number} FREQUENCY_ALWAYS=1 FREQUENCY_ALWAYS value
         * @property {number} FREQUENCY_FREQUENTLY=2 FREQUENCY_FREQUENTLY value
         * @property {number} FREQUENCY_OCCASIONALLY=3 FREQUENCY_OCCASIONALLY value
         * @property {number} FREQUENCY_RARELY=4 FREQUENCY_RARELY value
         */
        BugReportProto.Frequency = (function() {
            var valuesById = {}, values = Object.create(valuesById);
            values[valuesById[0] = "FREQUENCY_UNKNOWN_UNSPECIFIED"] = 0;
            values[valuesById[1] = "FREQUENCY_ALWAYS"] = 1;
            values[valuesById[2] = "FREQUENCY_FREQUENTLY"] = 2;
            values[valuesById[3] = "FREQUENCY_OCCASIONALLY"] = 3;
            values[valuesById[4] = "FREQUENCY_RARELY"] = 4;
            return values;
        })();

        /**
         * Severity enum.
         * @name feedback.BugReportProto.Severity
         * @enum {number}
         * @property {number} SEVERITY_UNDEFINED_UNSPECIFIED=0 SEVERITY_UNDEFINED_UNSPECIFIED value
         * @property {number} SEVERITY_LOW=1 SEVERITY_LOW value
         * @property {number} SEVERITY_MEDIUM=2 SEVERITY_MEDIUM value
         * @property {number} SEVERITY_HIGH=3 SEVERITY_HIGH value
         * @property {number} SEVERITY_CRITICAL=4 SEVERITY_CRITICAL value
         */
        BugReportProto.Severity = (function() {
            var valuesById = {}, values = Object.create(valuesById);
            values[valuesById[0] = "SEVERITY_UNDEFINED_UNSPECIFIED"] = 0;
            values[valuesById[1] = "SEVERITY_LOW"] = 1;
            values[valuesById[2] = "SEVERITY_MEDIUM"] = 2;
            values[valuesById[3] = "SEVERITY_HIGH"] = 3;
            values[valuesById[4] = "SEVERITY_CRITICAL"] = 4;
            return values;
        })();

        /**
         * Status enum.
         * @name feedback.BugReportProto.Status
         * @enum {number}
         * @property {number} STATUS_UNSPECIFIED=0 STATUS_UNSPECIFIED value
         * @property {number} STATUS_OPEN=1 STATUS_OPEN value
         * @property {number} STATUS_IN_PROGRESS=2 STATUS_IN_PROGRESS value
         * @property {number} STATUS_RESOLVED=3 STATUS_RESOLVED value
         * @property {number} STATUS_CLOSED=4 STATUS_CLOSED value
         * @property {number} STATUS_REJECTED=5 STATUS_REJECTED value
         */
        BugReportProto.Status = (function() {
            var valuesById = {}, values = Object.create(valuesById);
            values[valuesById[0] = "STATUS_UNSPECIFIED"] = 0;
            values[valuesById[1] = "STATUS_OPEN"] = 1;
            values[valuesById[2] = "STATUS_IN_PROGRESS"] = 2;
            values[valuesById[3] = "STATUS_RESOLVED"] = 3;
            values[valuesById[4] = "STATUS_CLOSED"] = 4;
            values[valuesById[5] = "STATUS_REJECTED"] = 5;
            return values;
        })();

        return BugReportProto;
    })();

    feedback.BugReportCollection = (function() {

        /**
         * Properties of a BugReportCollection.
         * @memberof feedback
         * @interface IBugReportCollection
         * @property {Array.<feedback.IBugReportProto>|null} [reports] BugReportCollection reports
         */

        /**
         * Constructs a new BugReportCollection.
         * @memberof feedback
         * @classdesc Represents a BugReportCollection.
         * @implements IBugReportCollection
         * @constructor
         * @param {feedback.IBugReportCollection=} [properties] Properties to set
         */
        function BugReportCollection(properties) {
            this.reports = [];
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BugReportCollection reports.
         * @member {Array.<feedback.IBugReportProto>} reports
         * @memberof feedback.BugReportCollection
         * @instance
         */
        BugReportCollection.prototype.reports = $util.emptyArray;

        /**
         * Creates a new BugReportCollection instance using the specified properties.
         * @function create
         * @memberof feedback.BugReportCollection
         * @static
         * @param {feedback.IBugReportCollection=} [properties] Properties to set
         * @returns {feedback.BugReportCollection} BugReportCollection instance
         */
        BugReportCollection.create = function create(properties) {
            return new BugReportCollection(properties);
        };

        /**
         * Encodes the specified BugReportCollection message. Does not implicitly {@link feedback.BugReportCollection.verify|verify} messages.
         * @function encode
         * @memberof feedback.BugReportCollection
         * @static
         * @param {feedback.IBugReportCollection} message BugReportCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BugReportCollection.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.reports != null && message.reports.length)
                for (var i = 0; i < message.reports.length; ++i)
                    $root.feedback.BugReportProto.encode(message.reports[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified BugReportCollection message, length delimited. Does not implicitly {@link feedback.BugReportCollection.verify|verify} messages.
         * @function encodeDelimited
         * @memberof feedback.BugReportCollection
         * @static
         * @param {feedback.IBugReportCollection} message BugReportCollection message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BugReportCollection.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BugReportCollection message from the specified reader or buffer.
         * @function decode
         * @memberof feedback.BugReportCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {feedback.BugReportCollection} BugReportCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BugReportCollection.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.feedback.BugReportCollection();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.reports && message.reports.length))
                            message.reports = [];
                        message.reports.push($root.feedback.BugReportProto.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BugReportCollection message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof feedback.BugReportCollection
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {feedback.BugReportCollection} BugReportCollection
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BugReportCollection.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BugReportCollection message.
         * @function verify
         * @memberof feedback.BugReportCollection
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BugReportCollection.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.reports != null && message.hasOwnProperty("reports")) {
                if (!Array.isArray(message.reports))
                    return "reports: array expected";
                for (var i = 0; i < message.reports.length; ++i) {
                    var error = $root.feedback.BugReportProto.verify(message.reports[i]);
                    if (error)
                        return "reports." + error;
                }
            }
            return null;
        };

        /**
         * Creates a BugReportCollection message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof feedback.BugReportCollection
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {feedback.BugReportCollection} BugReportCollection
         */
        BugReportCollection.fromObject = function fromObject(object) {
            if (object instanceof $root.feedback.BugReportCollection)
                return object;
            var message = new $root.feedback.BugReportCollection();
            if (object.reports) {
                if (!Array.isArray(object.reports))
                    throw TypeError(".feedback.BugReportCollection.reports: array expected");
                message.reports = [];
                for (var i = 0; i < object.reports.length; ++i) {
                    if (typeof object.reports[i] !== "object")
                        throw TypeError(".feedback.BugReportCollection.reports: object expected");
                    message.reports[i] = $root.feedback.BugReportProto.fromObject(object.reports[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a BugReportCollection message. Also converts values to other types if specified.
         * @function toObject
         * @memberof feedback.BugReportCollection
         * @static
         * @param {feedback.BugReportCollection} message BugReportCollection
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BugReportCollection.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.arrays || options.defaults)
                object.reports = [];
            if (message.reports && message.reports.length) {
                object.reports = [];
                for (var j = 0; j < message.reports.length; ++j)
                    object.reports[j] = $root.feedback.BugReportProto.toObject(message.reports[j], options);
            }
            return object;
        };

        /**
         * Converts this BugReportCollection to JSON.
         * @function toJSON
         * @memberof feedback.BugReportCollection
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BugReportCollection.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BugReportCollection
         * @function getTypeUrl
         * @memberof feedback.BugReportCollection
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BugReportCollection.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/feedback.BugReportCollection";
        };

        return BugReportCollection;
    })();

    return feedback;
})();

$root.chatbot = (function() {

    /**
     * Namespace chatbot.
     * @exports chatbot
     * @namespace
     */
    var chatbot = {};

    chatbot.ChatMessage = (function() {

        /**
         * Properties of a ChatMessage.
         * @memberof chatbot
         * @interface IChatMessage
         * @property {string|null} [userId] ChatMessage userId
         * @property {string|null} [content] ChatMessage content
         * @property {number|Long|null} [timestamp] ChatMessage timestamp
         * @property {chatbot.ChatMessage.MessageType|null} [type] ChatMessage type
         */

        /**
         * Constructs a new ChatMessage.
         * @memberof chatbot
         * @classdesc Represents a ChatMessage.
         * @implements IChatMessage
         * @constructor
         * @param {chatbot.IChatMessage=} [properties] Properties to set
         */
        function ChatMessage(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ChatMessage userId.
         * @member {string} userId
         * @memberof chatbot.ChatMessage
         * @instance
         */
        ChatMessage.prototype.userId = "";

        /**
         * ChatMessage content.
         * @member {string} content
         * @memberof chatbot.ChatMessage
         * @instance
         */
        ChatMessage.prototype.content = "";

        /**
         * ChatMessage timestamp.
         * @member {number|Long} timestamp
         * @memberof chatbot.ChatMessage
         * @instance
         */
        ChatMessage.prototype.timestamp = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * ChatMessage type.
         * @member {chatbot.ChatMessage.MessageType} type
         * @memberof chatbot.ChatMessage
         * @instance
         */
        ChatMessage.prototype.type = 0;

        /**
         * Creates a new ChatMessage instance using the specified properties.
         * @function create
         * @memberof chatbot.ChatMessage
         * @static
         * @param {chatbot.IChatMessage=} [properties] Properties to set
         * @returns {chatbot.ChatMessage} ChatMessage instance
         */
        ChatMessage.create = function create(properties) {
            return new ChatMessage(properties);
        };

        /**
         * Encodes the specified ChatMessage message. Does not implicitly {@link chatbot.ChatMessage.verify|verify} messages.
         * @function encode
         * @memberof chatbot.ChatMessage
         * @static
         * @param {chatbot.IChatMessage} message ChatMessage message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChatMessage.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.userId != null && Object.hasOwnProperty.call(message, "userId"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.userId);
            if (message.content != null && Object.hasOwnProperty.call(message, "content"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.content);
            if (message.timestamp != null && Object.hasOwnProperty.call(message, "timestamp"))
                writer.uint32(/* id 3, wireType 0 =*/24).int64(message.timestamp);
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 4, wireType 0 =*/32).int32(message.type);
            return writer;
        };

        /**
         * Encodes the specified ChatMessage message, length delimited. Does not implicitly {@link chatbot.ChatMessage.verify|verify} messages.
         * @function encodeDelimited
         * @memberof chatbot.ChatMessage
         * @static
         * @param {chatbot.IChatMessage} message ChatMessage message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChatMessage.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ChatMessage message from the specified reader or buffer.
         * @function decode
         * @memberof chatbot.ChatMessage
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {chatbot.ChatMessage} ChatMessage
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChatMessage.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.chatbot.ChatMessage();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.userId = reader.string();
                        break;
                    }
                case 2: {
                        message.content = reader.string();
                        break;
                    }
                case 3: {
                        message.timestamp = reader.int64();
                        break;
                    }
                case 4: {
                        message.type = reader.int32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ChatMessage message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof chatbot.ChatMessage
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {chatbot.ChatMessage} ChatMessage
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChatMessage.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ChatMessage message.
         * @function verify
         * @memberof chatbot.ChatMessage
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ChatMessage.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.userId != null && message.hasOwnProperty("userId"))
                if (!$util.isString(message.userId))
                    return "userId: string expected";
            if (message.content != null && message.hasOwnProperty("content"))
                if (!$util.isString(message.content))
                    return "content: string expected";
            if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                if (!$util.isInteger(message.timestamp) && !(message.timestamp && $util.isInteger(message.timestamp.low) && $util.isInteger(message.timestamp.high)))
                    return "timestamp: integer|Long expected";
            if (message.type != null && message.hasOwnProperty("type"))
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                    break;
                }
            return null;
        };

        /**
         * Creates a ChatMessage message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof chatbot.ChatMessage
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {chatbot.ChatMessage} ChatMessage
         */
        ChatMessage.fromObject = function fromObject(object) {
            if (object instanceof $root.chatbot.ChatMessage)
                return object;
            var message = new $root.chatbot.ChatMessage();
            if (object.userId != null)
                message.userId = String(object.userId);
            if (object.content != null)
                message.content = String(object.content);
            if (object.timestamp != null)
                if ($util.Long)
                    (message.timestamp = $util.Long.fromValue(object.timestamp)).unsigned = false;
                else if (typeof object.timestamp === "string")
                    message.timestamp = parseInt(object.timestamp, 10);
                else if (typeof object.timestamp === "number")
                    message.timestamp = object.timestamp;
                else if (typeof object.timestamp === "object")
                    message.timestamp = new $util.LongBits(object.timestamp.low >>> 0, object.timestamp.high >>> 0).toNumber();
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "MESSAGE_TYPE_TEXT_UNSPECIFIED":
            case 0:
                message.type = 0;
                break;
            case "MESSAGE_TYPE_IMAGE":
            case 1:
                message.type = 1;
                break;
            case "MESSAGE_TYPE_AUDIO":
            case 2:
                message.type = 2;
                break;
            }
            return message;
        };

        /**
         * Creates a plain object from a ChatMessage message. Also converts values to other types if specified.
         * @function toObject
         * @memberof chatbot.ChatMessage
         * @static
         * @param {chatbot.ChatMessage} message ChatMessage
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ChatMessage.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.userId = "";
                object.content = "";
                if ($util.Long) {
                    var long = new $util.Long(0, 0, false);
                    object.timestamp = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.timestamp = options.longs === String ? "0" : 0;
                object.type = options.enums === String ? "MESSAGE_TYPE_TEXT_UNSPECIFIED" : 0;
            }
            if (message.userId != null && message.hasOwnProperty("userId"))
                object.userId = message.userId;
            if (message.content != null && message.hasOwnProperty("content"))
                object.content = message.content;
            if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                if (typeof message.timestamp === "number")
                    object.timestamp = options.longs === String ? String(message.timestamp) : message.timestamp;
                else
                    object.timestamp = options.longs === String ? $util.Long.prototype.toString.call(message.timestamp) : options.longs === Number ? new $util.LongBits(message.timestamp.low >>> 0, message.timestamp.high >>> 0).toNumber() : message.timestamp;
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = options.enums === String ? $root.chatbot.ChatMessage.MessageType[message.type] === undefined ? message.type : $root.chatbot.ChatMessage.MessageType[message.type] : message.type;
            return object;
        };

        /**
         * Converts this ChatMessage to JSON.
         * @function toJSON
         * @memberof chatbot.ChatMessage
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ChatMessage.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ChatMessage
         * @function getTypeUrl
         * @memberof chatbot.ChatMessage
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ChatMessage.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/chatbot.ChatMessage";
        };

        /**
         * MessageType enum.
         * @name chatbot.ChatMessage.MessageType
         * @enum {number}
         * @property {number} MESSAGE_TYPE_TEXT_UNSPECIFIED=0 MESSAGE_TYPE_TEXT_UNSPECIFIED value
         * @property {number} MESSAGE_TYPE_IMAGE=1 MESSAGE_TYPE_IMAGE value
         * @property {number} MESSAGE_TYPE_AUDIO=2 MESSAGE_TYPE_AUDIO value
         */
        ChatMessage.MessageType = (function() {
            var valuesById = {}, values = Object.create(valuesById);
            values[valuesById[0] = "MESSAGE_TYPE_TEXT_UNSPECIFIED"] = 0;
            values[valuesById[1] = "MESSAGE_TYPE_IMAGE"] = 1;
            values[valuesById[2] = "MESSAGE_TYPE_AUDIO"] = 2;
            return values;
        })();

        return ChatMessage;
    })();

    chatbot.ChatResponse = (function() {

        /**
         * Properties of a ChatResponse.
         * @memberof chatbot
         * @interface IChatResponse
         * @property {string|null} [messageId] ChatResponse messageId
         * @property {string|null} [content] ChatResponse content
         * @property {number|Long|null} [timestamp] ChatResponse timestamp
         */

        /**
         * Constructs a new ChatResponse.
         * @memberof chatbot
         * @classdesc Represents a ChatResponse.
         * @implements IChatResponse
         * @constructor
         * @param {chatbot.IChatResponse=} [properties] Properties to set
         */
        function ChatResponse(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ChatResponse messageId.
         * @member {string} messageId
         * @memberof chatbot.ChatResponse
         * @instance
         */
        ChatResponse.prototype.messageId = "";

        /**
         * ChatResponse content.
         * @member {string} content
         * @memberof chatbot.ChatResponse
         * @instance
         */
        ChatResponse.prototype.content = "";

        /**
         * ChatResponse timestamp.
         * @member {number|Long} timestamp
         * @memberof chatbot.ChatResponse
         * @instance
         */
        ChatResponse.prototype.timestamp = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * Creates a new ChatResponse instance using the specified properties.
         * @function create
         * @memberof chatbot.ChatResponse
         * @static
         * @param {chatbot.IChatResponse=} [properties] Properties to set
         * @returns {chatbot.ChatResponse} ChatResponse instance
         */
        ChatResponse.create = function create(properties) {
            return new ChatResponse(properties);
        };

        /**
         * Encodes the specified ChatResponse message. Does not implicitly {@link chatbot.ChatResponse.verify|verify} messages.
         * @function encode
         * @memberof chatbot.ChatResponse
         * @static
         * @param {chatbot.IChatResponse} message ChatResponse message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChatResponse.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.messageId != null && Object.hasOwnProperty.call(message, "messageId"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.messageId);
            if (message.content != null && Object.hasOwnProperty.call(message, "content"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.content);
            if (message.timestamp != null && Object.hasOwnProperty.call(message, "timestamp"))
                writer.uint32(/* id 3, wireType 0 =*/24).int64(message.timestamp);
            return writer;
        };

        /**
         * Encodes the specified ChatResponse message, length delimited. Does not implicitly {@link chatbot.ChatResponse.verify|verify} messages.
         * @function encodeDelimited
         * @memberof chatbot.ChatResponse
         * @static
         * @param {chatbot.IChatResponse} message ChatResponse message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChatResponse.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ChatResponse message from the specified reader or buffer.
         * @function decode
         * @memberof chatbot.ChatResponse
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {chatbot.ChatResponse} ChatResponse
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChatResponse.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.chatbot.ChatResponse();
            while (reader.pos < end) {
                var tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.messageId = reader.string();
                        break;
                    }
                case 2: {
                        message.content = reader.string();
                        break;
                    }
                case 3: {
                        message.timestamp = reader.int64();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ChatResponse message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof chatbot.ChatResponse
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {chatbot.ChatResponse} ChatResponse
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChatResponse.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ChatResponse message.
         * @function verify
         * @memberof chatbot.ChatResponse
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ChatResponse.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.messageId != null && message.hasOwnProperty("messageId"))
                if (!$util.isString(message.messageId))
                    return "messageId: string expected";
            if (message.content != null && message.hasOwnProperty("content"))
                if (!$util.isString(message.content))
                    return "content: string expected";
            if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                if (!$util.isInteger(message.timestamp) && !(message.timestamp && $util.isInteger(message.timestamp.low) && $util.isInteger(message.timestamp.high)))
                    return "timestamp: integer|Long expected";
            return null;
        };

        /**
         * Creates a ChatResponse message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof chatbot.ChatResponse
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {chatbot.ChatResponse} ChatResponse
         */
        ChatResponse.fromObject = function fromObject(object) {
            if (object instanceof $root.chatbot.ChatResponse)
                return object;
            var message = new $root.chatbot.ChatResponse();
            if (object.messageId != null)
                message.messageId = String(object.messageId);
            if (object.content != null)
                message.content = String(object.content);
            if (object.timestamp != null)
                if ($util.Long)
                    (message.timestamp = $util.Long.fromValue(object.timestamp)).unsigned = false;
                else if (typeof object.timestamp === "string")
                    message.timestamp = parseInt(object.timestamp, 10);
                else if (typeof object.timestamp === "number")
                    message.timestamp = object.timestamp;
                else if (typeof object.timestamp === "object")
                    message.timestamp = new $util.LongBits(object.timestamp.low >>> 0, object.timestamp.high >>> 0).toNumber();
            return message;
        };

        /**
         * Creates a plain object from a ChatResponse message. Also converts values to other types if specified.
         * @function toObject
         * @memberof chatbot.ChatResponse
         * @static
         * @param {chatbot.ChatResponse} message ChatResponse
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ChatResponse.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults) {
                object.messageId = "";
                object.content = "";
                if ($util.Long) {
                    var long = new $util.Long(0, 0, false);
                    object.timestamp = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.timestamp = options.longs === String ? "0" : 0;
            }
            if (message.messageId != null && message.hasOwnProperty("messageId"))
                object.messageId = message.messageId;
            if (message.content != null && message.hasOwnProperty("content"))
                object.content = message.content;
            if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                if (typeof message.timestamp === "number")
                    object.timestamp = options.longs === String ? String(message.timestamp) : message.timestamp;
                else
                    object.timestamp = options.longs === String ? $util.Long.prototype.toString.call(message.timestamp) : options.longs === Number ? new $util.LongBits(message.timestamp.low >>> 0, message.timestamp.high >>> 0).toNumber() : message.timestamp;
            return object;
        };

        /**
         * Converts this ChatResponse to JSON.
         * @function toJSON
         * @memberof chatbot.ChatResponse
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ChatResponse.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ChatResponse
         * @function getTypeUrl
         * @memberof chatbot.ChatResponse
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ChatResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/chatbot.ChatResponse";
        };

        return ChatResponse;
    })();

    return chatbot;
})();

module.exports = $root;
