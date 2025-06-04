import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace company. */
export namespace company {
	/** Properties of a CompanyProto. */
	interface ICompanyProto {
		/** CompanyProto id */
		id?: string | null;

		/** CompanyProto name */
		name?: string | null;

		/** CompanyProto logoUrl */
		logoUrl?: string | null;

		/** CompanyProto description */
		description?: string | null;

		/** CompanyProto website */
		website?: string | null;

		/** CompanyProto address */
		address?: string | null;

		/** CompanyProto phone */
		phone?: string | null;

		/** CompanyProto email */
		email?: string | null;

		/** CompanyProto companyType */
		companyType?: string | null;

		/** CompanyProto size */
		size?: string | null;

		/** CompanyProto industry */
		industry?: string | null;

		/** CompanyProto isActive */
		isActive?: boolean | null;

		/** CompanyProto memberUserIds */
		memberUserIds?: string[] | null;

		/** CompanyProto createdAt */
		createdAt?: string | null;

		/** CompanyProto updatedAt */
		updatedAt?: string | null;
	}

	/** Represents a CompanyProto. */
	class CompanyProto implements ICompanyProto {
		/**
		 * Constructs a new CompanyProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: company.ICompanyProto);

		/** CompanyProto id. */
		public id: string;

		/** CompanyProto name. */
		public name: string;

		/** CompanyProto logoUrl. */
		public logoUrl: string;

		/** CompanyProto description. */
		public description: string;

		/** CompanyProto website. */
		public website: string;

		/** CompanyProto address. */
		public address: string;

		/** CompanyProto phone. */
		public phone: string;

		/** CompanyProto email. */
		public email: string;

		/** CompanyProto companyType. */
		public companyType: string;

		/** CompanyProto size. */
		public size: string;

		/** CompanyProto industry. */
		public industry: string;

		/** CompanyProto isActive. */
		public isActive: boolean;

		/** CompanyProto memberUserIds. */
		public memberUserIds: string[];

		/** CompanyProto createdAt. */
		public createdAt: string;

		/** CompanyProto updatedAt. */
		public updatedAt: string;

		/**
		 * Creates a new CompanyProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CompanyProto instance
		 */
		public static create(
			properties?: company.ICompanyProto,
		): company.CompanyProto;

		/**
		 * Encodes the specified CompanyProto message. Does not implicitly {@link company.CompanyProto.verify|verify} messages.
		 * @param message CompanyProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: company.ICompanyProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CompanyProto message, length delimited. Does not implicitly {@link company.CompanyProto.verify|verify} messages.
		 * @param message CompanyProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: company.ICompanyProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CompanyProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CompanyProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): company.CompanyProto;

		/**
		 * Decodes a CompanyProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CompanyProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): company.CompanyProto;

		/**
		 * Verifies a CompanyProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CompanyProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CompanyProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): company.CompanyProto;

		/**
		 * Creates a plain object from a CompanyProto message. Also converts values to other types if specified.
		 * @param message CompanyProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: company.CompanyProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CompanyProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CompanyProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CompanyMembershipProto. */
	interface ICompanyMembershipProto {
		/** CompanyMembershipProto id */
		id?: string | null;

		/** CompanyMembershipProto companyId */
		companyId?: string | null;

		/** CompanyMembershipProto userId */
		userId?: string | null;

		/** CompanyMembershipProto role */
		role?: string | null;

		/** CompanyMembershipProto department */
		department?: string | null;

		/** CompanyMembershipProto position */
		position?: string | null;

		/** CompanyMembershipProto dateJoined */
		dateJoined?: string | null;

		/** CompanyMembershipProto isPrimary */
		isPrimary?: boolean | null;
	}

	/** Represents a CompanyMembershipProto. */
	class CompanyMembershipProto implements ICompanyMembershipProto {
		/**
		 * Constructs a new CompanyMembershipProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: company.ICompanyMembershipProto);

		/** CompanyMembershipProto id. */
		public id: string;

		/** CompanyMembershipProto companyId. */
		public companyId: string;

		/** CompanyMembershipProto userId. */
		public userId: string;

		/** CompanyMembershipProto role. */
		public role: string;

		/** CompanyMembershipProto department. */
		public department: string;

		/** CompanyMembershipProto position. */
		public position: string;

		/** CompanyMembershipProto dateJoined. */
		public dateJoined: string;

		/** CompanyMembershipProto isPrimary. */
		public isPrimary: boolean;

		/**
		 * Creates a new CompanyMembershipProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CompanyMembershipProto instance
		 */
		public static create(
			properties?: company.ICompanyMembershipProto,
		): company.CompanyMembershipProto;

		/**
		 * Encodes the specified CompanyMembershipProto message. Does not implicitly {@link company.CompanyMembershipProto.verify|verify} messages.
		 * @param message CompanyMembershipProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: company.ICompanyMembershipProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CompanyMembershipProto message, length delimited. Does not implicitly {@link company.CompanyMembershipProto.verify|verify} messages.
		 * @param message CompanyMembershipProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: company.ICompanyMembershipProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CompanyMembershipProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CompanyMembershipProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): company.CompanyMembershipProto;

		/**
		 * Decodes a CompanyMembershipProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CompanyMembershipProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): company.CompanyMembershipProto;

		/**
		 * Verifies a CompanyMembershipProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CompanyMembershipProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CompanyMembershipProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): company.CompanyMembershipProto;

		/**
		 * Creates a plain object from a CompanyMembershipProto message. Also converts values to other types if specified.
		 * @param message CompanyMembershipProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: company.CompanyMembershipProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CompanyMembershipProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CompanyMembershipProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CompanyDocumentProto. */
	interface ICompanyDocumentProto {
		/** CompanyDocumentProto id */
		id?: string | null;

		/** CompanyDocumentProto companyId */
		companyId?: string | null;

		/** CompanyDocumentProto name */
		name?: string | null;

		/** CompanyDocumentProto description */
		description?: string | null;

		/** CompanyDocumentProto fileUrl */
		fileUrl?: string | null;

		/** CompanyDocumentProto documentType */
		documentType?: string | null;

		/** CompanyDocumentProto uploadedByUserId */
		uploadedByUserId?: string | null;

		/** CompanyDocumentProto uploadedAt */
		uploadedAt?: string | null;
	}

	/** Represents a CompanyDocumentProto. */
	class CompanyDocumentProto implements ICompanyDocumentProto {
		/**
		 * Constructs a new CompanyDocumentProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: company.ICompanyDocumentProto);

		/** CompanyDocumentProto id. */
		public id: string;

		/** CompanyDocumentProto companyId. */
		public companyId: string;

		/** CompanyDocumentProto name. */
		public name: string;

		/** CompanyDocumentProto description. */
		public description: string;

		/** CompanyDocumentProto fileUrl. */
		public fileUrl: string;

		/** CompanyDocumentProto documentType. */
		public documentType: string;

		/** CompanyDocumentProto uploadedByUserId. */
		public uploadedByUserId: string;

		/** CompanyDocumentProto uploadedAt. */
		public uploadedAt: string;

		/**
		 * Creates a new CompanyDocumentProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CompanyDocumentProto instance
		 */
		public static create(
			properties?: company.ICompanyDocumentProto,
		): company.CompanyDocumentProto;

		/**
		 * Encodes the specified CompanyDocumentProto message. Does not implicitly {@link company.CompanyDocumentProto.verify|verify} messages.
		 * @param message CompanyDocumentProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: company.ICompanyDocumentProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CompanyDocumentProto message, length delimited. Does not implicitly {@link company.CompanyDocumentProto.verify|verify} messages.
		 * @param message CompanyDocumentProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: company.ICompanyDocumentProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CompanyDocumentProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CompanyDocumentProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): company.CompanyDocumentProto;

		/**
		 * Decodes a CompanyDocumentProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CompanyDocumentProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): company.CompanyDocumentProto;

		/**
		 * Verifies a CompanyDocumentProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CompanyDocumentProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CompanyDocumentProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): company.CompanyDocumentProto;

		/**
		 * Creates a plain object from a CompanyDocumentProto message. Also converts values to other types if specified.
		 * @param message CompanyDocumentProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: company.CompanyDocumentProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CompanyDocumentProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CompanyDocumentProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CompanyCollection. */
	interface ICompanyCollection {
		/** CompanyCollection companies */
		companies?: company.ICompanyProto[] | null;
	}

	/** Represents a CompanyCollection. */
	class CompanyCollection implements ICompanyCollection {
		/**
		 * Constructs a new CompanyCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: company.ICompanyCollection);

		/** CompanyCollection companies. */
		public companies: company.ICompanyProto[];

		/**
		 * Creates a new CompanyCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CompanyCollection instance
		 */
		public static create(
			properties?: company.ICompanyCollection,
		): company.CompanyCollection;

		/**
		 * Encodes the specified CompanyCollection message. Does not implicitly {@link company.CompanyCollection.verify|verify} messages.
		 * @param message CompanyCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: company.ICompanyCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CompanyCollection message, length delimited. Does not implicitly {@link company.CompanyCollection.verify|verify} messages.
		 * @param message CompanyCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: company.ICompanyCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CompanyCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CompanyCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): company.CompanyCollection;

		/**
		 * Decodes a CompanyCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CompanyCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): company.CompanyCollection;

		/**
		 * Verifies a CompanyCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CompanyCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CompanyCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): company.CompanyCollection;

		/**
		 * Creates a plain object from a CompanyCollection message. Also converts values to other types if specified.
		 * @param message CompanyCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: company.CompanyCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CompanyCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CompanyCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CompanyMembershipCollection. */
	interface ICompanyMembershipCollection {
		/** CompanyMembershipCollection memberships */
		memberships?: company.ICompanyMembershipProto[] | null;
	}

	/** Represents a CompanyMembershipCollection. */
	class CompanyMembershipCollection implements ICompanyMembershipCollection {
		/**
		 * Constructs a new CompanyMembershipCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: company.ICompanyMembershipCollection);

		/** CompanyMembershipCollection memberships. */
		public memberships: company.ICompanyMembershipProto[];

		/**
		 * Creates a new CompanyMembershipCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CompanyMembershipCollection instance
		 */
		public static create(
			properties?: company.ICompanyMembershipCollection,
		): company.CompanyMembershipCollection;

		/**
		 * Encodes the specified CompanyMembershipCollection message. Does not implicitly {@link company.CompanyMembershipCollection.verify|verify} messages.
		 * @param message CompanyMembershipCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: company.ICompanyMembershipCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CompanyMembershipCollection message, length delimited. Does not implicitly {@link company.CompanyMembershipCollection.verify|verify} messages.
		 * @param message CompanyMembershipCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: company.ICompanyMembershipCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CompanyMembershipCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CompanyMembershipCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): company.CompanyMembershipCollection;

		/**
		 * Decodes a CompanyMembershipCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CompanyMembershipCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): company.CompanyMembershipCollection;

		/**
		 * Verifies a CompanyMembershipCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CompanyMembershipCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CompanyMembershipCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): company.CompanyMembershipCollection;

		/**
		 * Creates a plain object from a CompanyMembershipCollection message. Also converts values to other types if specified.
		 * @param message CompanyMembershipCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: company.CompanyMembershipCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CompanyMembershipCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CompanyMembershipCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CompanyDocumentCollection. */
	interface ICompanyDocumentCollection {
		/** CompanyDocumentCollection documents */
		documents?: company.ICompanyDocumentProto[] | null;
	}

	/** Represents a CompanyDocumentCollection. */
	class CompanyDocumentCollection implements ICompanyDocumentCollection {
		/**
		 * Constructs a new CompanyDocumentCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: company.ICompanyDocumentCollection);

		/** CompanyDocumentCollection documents. */
		public documents: company.ICompanyDocumentProto[];

		/**
		 * Creates a new CompanyDocumentCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CompanyDocumentCollection instance
		 */
		public static create(
			properties?: company.ICompanyDocumentCollection,
		): company.CompanyDocumentCollection;

		/**
		 * Encodes the specified CompanyDocumentCollection message. Does not implicitly {@link company.CompanyDocumentCollection.verify|verify} messages.
		 * @param message CompanyDocumentCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: company.ICompanyDocumentCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CompanyDocumentCollection message, length delimited. Does not implicitly {@link company.CompanyDocumentCollection.verify|verify} messages.
		 * @param message CompanyDocumentCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: company.ICompanyDocumentCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CompanyDocumentCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CompanyDocumentCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): company.CompanyDocumentCollection;

		/**
		 * Decodes a CompanyDocumentCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CompanyDocumentCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): company.CompanyDocumentCollection;

		/**
		 * Verifies a CompanyDocumentCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CompanyDocumentCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CompanyDocumentCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): company.CompanyDocumentCollection;

		/**
		 * Creates a plain object from a CompanyDocumentCollection message. Also converts values to other types if specified.
		 * @param message CompanyDocumentCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: company.CompanyDocumentCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CompanyDocumentCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CompanyDocumentCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}

/** Namespace projects. */
export namespace projects {
	/** Properties of a ProjectProto. */
	interface IProjectProto {
		/** ProjectProto id */
		id?: string | null;

		/** ProjectProto name */
		name?: string | null;

		/** ProjectProto description */
		description?: string | null;

		/** ProjectProto memberUserIds */
		memberUserIds?: string[] | null;

		/** ProjectProto createdAt */
		createdAt?: string | null;

		/** ProjectProto updatedAt */
		updatedAt?: string | null;
	}

	/** Represents a ProjectProto. */
	class ProjectProto implements IProjectProto {
		/**
		 * Constructs a new ProjectProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: projects.IProjectProto);

		/** ProjectProto id. */
		public id: string;

		/** ProjectProto name. */
		public name: string;

		/** ProjectProto description. */
		public description: string;

		/** ProjectProto memberUserIds. */
		public memberUserIds: string[];

		/** ProjectProto createdAt. */
		public createdAt: string;

		/** ProjectProto updatedAt. */
		public updatedAt: string;

		/**
		 * Creates a new ProjectProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProjectProto instance
		 */
		public static create(
			properties?: projects.IProjectProto,
		): projects.ProjectProto;

		/**
		 * Encodes the specified ProjectProto message. Does not implicitly {@link projects.ProjectProto.verify|verify} messages.
		 * @param message ProjectProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: projects.IProjectProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProjectProto message, length delimited. Does not implicitly {@link projects.ProjectProto.verify|verify} messages.
		 * @param message ProjectProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: projects.IProjectProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProjectProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProjectProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): projects.ProjectProto;

		/**
		 * Decodes a ProjectProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProjectProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): projects.ProjectProto;

		/**
		 * Verifies a ProjectProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProjectProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProjectProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): projects.ProjectProto;

		/**
		 * Creates a plain object from a ProjectProto message. Also converts values to other types if specified.
		 * @param message ProjectProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: projects.ProjectProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProjectProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProjectProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProjectMembershipProto. */
	interface IProjectMembershipProto {
		/** ProjectMembershipProto id */
		id?: string | null;

		/** ProjectMembershipProto projectId */
		projectId?: string | null;

		/** ProjectMembershipProto userId */
		userId?: string | null;

		/** ProjectMembershipProto role */
		role?: string | null;

		/** ProjectMembershipProto createdAt */
		createdAt?: string | null;

		/** ProjectMembershipProto updatedAt */
		updatedAt?: string | null;
	}

	/** Represents a ProjectMembershipProto. */
	class ProjectMembershipProto implements IProjectMembershipProto {
		/**
		 * Constructs a new ProjectMembershipProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: projects.IProjectMembershipProto);

		/** ProjectMembershipProto id. */
		public id: string;

		/** ProjectMembershipProto projectId. */
		public projectId: string;

		/** ProjectMembershipProto userId. */
		public userId: string;

		/** ProjectMembershipProto role. */
		public role: string;

		/** ProjectMembershipProto createdAt. */
		public createdAt: string;

		/** ProjectMembershipProto updatedAt. */
		public updatedAt: string;

		/**
		 * Creates a new ProjectMembershipProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProjectMembershipProto instance
		 */
		public static create(
			properties?: projects.IProjectMembershipProto,
		): projects.ProjectMembershipProto;

		/**
		 * Encodes the specified ProjectMembershipProto message. Does not implicitly {@link projects.ProjectMembershipProto.verify|verify} messages.
		 * @param message ProjectMembershipProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: projects.IProjectMembershipProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProjectMembershipProto message, length delimited. Does not implicitly {@link projects.ProjectMembershipProto.verify|verify} messages.
		 * @param message ProjectMembershipProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: projects.IProjectMembershipProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProjectMembershipProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProjectMembershipProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): projects.ProjectMembershipProto;

		/**
		 * Decodes a ProjectMembershipProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProjectMembershipProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): projects.ProjectMembershipProto;

		/**
		 * Verifies a ProjectMembershipProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProjectMembershipProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProjectMembershipProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): projects.ProjectMembershipProto;

		/**
		 * Creates a plain object from a ProjectMembershipProto message. Also converts values to other types if specified.
		 * @param message ProjectMembershipProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: projects.ProjectMembershipProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProjectMembershipProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProjectMembershipProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProjectObligationProto. */
	interface IProjectObligationProto {
		/** ProjectObligationProto id */
		id?: string | null;

		/** ProjectObligationProto projectId */
		projectId?: string | null;

		/** ProjectObligationProto obligationId */
		obligationId?: string | null;

		/** ProjectObligationProto createdAt */
		createdAt?: string | null;

		/** ProjectObligationProto updatedAt */
		updatedAt?: string | null;
	}

	/** Represents a ProjectObligationProto. */
	class ProjectObligationProto implements IProjectObligationProto {
		/**
		 * Constructs a new ProjectObligationProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: projects.IProjectObligationProto);

		/** ProjectObligationProto id. */
		public id: string;

		/** ProjectObligationProto projectId. */
		public projectId: string;

		/** ProjectObligationProto obligationId. */
		public obligationId: string;

		/** ProjectObligationProto createdAt. */
		public createdAt: string;

		/** ProjectObligationProto updatedAt. */
		public updatedAt: string;

		/**
		 * Creates a new ProjectObligationProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProjectObligationProto instance
		 */
		public static create(
			properties?: projects.IProjectObligationProto,
		): projects.ProjectObligationProto;

		/**
		 * Encodes the specified ProjectObligationProto message. Does not implicitly {@link projects.ProjectObligationProto.verify|verify} messages.
		 * @param message ProjectObligationProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: projects.IProjectObligationProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProjectObligationProto message, length delimited. Does not implicitly {@link projects.ProjectObligationProto.verify|verify} messages.
		 * @param message ProjectObligationProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: projects.IProjectObligationProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProjectObligationProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProjectObligationProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): projects.ProjectObligationProto;

		/**
		 * Decodes a ProjectObligationProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProjectObligationProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): projects.ProjectObligationProto;

		/**
		 * Verifies a ProjectObligationProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProjectObligationProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProjectObligationProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): projects.ProjectObligationProto;

		/**
		 * Creates a plain object from a ProjectObligationProto message. Also converts values to other types if specified.
		 * @param message ProjectObligationProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: projects.ProjectObligationProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProjectObligationProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProjectObligationProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProjectCollection. */
	interface IProjectCollection {
		/** ProjectCollection projects */
		projects?: projects.IProjectProto[] | null;
	}

	/** Represents a ProjectCollection. */
	class ProjectCollection implements IProjectCollection {
		/**
		 * Constructs a new ProjectCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: projects.IProjectCollection);

		/** ProjectCollection projects. */
		public projects: projects.IProjectProto[];

		/**
		 * Creates a new ProjectCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProjectCollection instance
		 */
		public static create(
			properties?: projects.IProjectCollection,
		): projects.ProjectCollection;

		/**
		 * Encodes the specified ProjectCollection message. Does not implicitly {@link projects.ProjectCollection.verify|verify} messages.
		 * @param message ProjectCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: projects.IProjectCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProjectCollection message, length delimited. Does not implicitly {@link projects.ProjectCollection.verify|verify} messages.
		 * @param message ProjectCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: projects.IProjectCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProjectCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProjectCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): projects.ProjectCollection;

		/**
		 * Decodes a ProjectCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProjectCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): projects.ProjectCollection;

		/**
		 * Verifies a ProjectCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProjectCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProjectCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): projects.ProjectCollection;

		/**
		 * Creates a plain object from a ProjectCollection message. Also converts values to other types if specified.
		 * @param message ProjectCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: projects.ProjectCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProjectCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProjectCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProjectMembershipCollection. */
	interface IProjectMembershipCollection {
		/** ProjectMembershipCollection memberships */
		memberships?: projects.IProjectMembershipProto[] | null;
	}

	/** Represents a ProjectMembershipCollection. */
	class ProjectMembershipCollection implements IProjectMembershipCollection {
		/**
		 * Constructs a new ProjectMembershipCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: projects.IProjectMembershipCollection);

		/** ProjectMembershipCollection memberships. */
		public memberships: projects.IProjectMembershipProto[];

		/**
		 * Creates a new ProjectMembershipCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProjectMembershipCollection instance
		 */
		public static create(
			properties?: projects.IProjectMembershipCollection,
		): projects.ProjectMembershipCollection;

		/**
		 * Encodes the specified ProjectMembershipCollection message. Does not implicitly {@link projects.ProjectMembershipCollection.verify|verify} messages.
		 * @param message ProjectMembershipCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: projects.IProjectMembershipCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProjectMembershipCollection message, length delimited. Does not implicitly {@link projects.ProjectMembershipCollection.verify|verify} messages.
		 * @param message ProjectMembershipCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: projects.IProjectMembershipCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProjectMembershipCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProjectMembershipCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): projects.ProjectMembershipCollection;

		/**
		 * Decodes a ProjectMembershipCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProjectMembershipCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): projects.ProjectMembershipCollection;

		/**
		 * Verifies a ProjectMembershipCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProjectMembershipCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProjectMembershipCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): projects.ProjectMembershipCollection;

		/**
		 * Creates a plain object from a ProjectMembershipCollection message. Also converts values to other types if specified.
		 * @param message ProjectMembershipCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: projects.ProjectMembershipCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProjectMembershipCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProjectMembershipCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProjectObligationCollection. */
	interface IProjectObligationCollection {
		/** ProjectObligationCollection projectObligations */
		projectObligations?: projects.IProjectObligationProto[] | null;
	}

	/** Represents a ProjectObligationCollection. */
	class ProjectObligationCollection implements IProjectObligationCollection {
		/**
		 * Constructs a new ProjectObligationCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: projects.IProjectObligationCollection);

		/** ProjectObligationCollection projectObligations. */
		public projectObligations: projects.IProjectObligationProto[];

		/**
		 * Creates a new ProjectObligationCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProjectObligationCollection instance
		 */
		public static create(
			properties?: projects.IProjectObligationCollection,
		): projects.ProjectObligationCollection;

		/**
		 * Encodes the specified ProjectObligationCollection message. Does not implicitly {@link projects.ProjectObligationCollection.verify|verify} messages.
		 * @param message ProjectObligationCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: projects.IProjectObligationCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProjectObligationCollection message, length delimited. Does not implicitly {@link projects.ProjectObligationCollection.verify|verify} messages.
		 * @param message ProjectObligationCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: projects.IProjectObligationCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProjectObligationCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProjectObligationCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): projects.ProjectObligationCollection;

		/**
		 * Decodes a ProjectObligationCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProjectObligationCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): projects.ProjectObligationCollection;

		/**
		 * Verifies a ProjectObligationCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProjectObligationCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProjectObligationCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): projects.ProjectObligationCollection;

		/**
		 * Creates a plain object from a ProjectObligationCollection message. Also converts values to other types if specified.
		 * @param message ProjectObligationCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: projects.ProjectObligationCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProjectObligationCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProjectObligationCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}

/** Namespace users. */
export namespace users {
	/** Properties of a UserProto. */
	interface IUserProto {
		/** UserProto id */
		id?: string | null;

		/** UserProto username */
		username?: string | null;

		/** UserProto email */
		email?: string | null;

		/** UserProto firstName */
		firstName?: string | null;

		/** UserProto lastName */
		lastName?: string | null;

		/** UserProto isActive */
		isActive?: boolean | null;

		/** UserProto dateJoined */
		dateJoined?: string | null;
	}

	/** Represents a UserProto. */
	class UserProto implements IUserProto {
		/**
		 * Constructs a new UserProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: users.IUserProto);

		/** UserProto id. */
		public id: string;

		/** UserProto username. */
		public username: string;

		/** UserProto email. */
		public email: string;

		/** UserProto firstName. */
		public firstName: string;

		/** UserProto lastName. */
		public lastName: string;

		/** UserProto isActive. */
		public isActive: boolean;

		/** UserProto dateJoined. */
		public dateJoined: string;

		/**
		 * Creates a new UserProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns UserProto instance
		 */
		public static create(properties?: users.IUserProto): users.UserProto;

		/**
		 * Encodes the specified UserProto message. Does not implicitly {@link users.UserProto.verify|verify} messages.
		 * @param message UserProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: users.IUserProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified UserProto message, length delimited. Does not implicitly {@link users.UserProto.verify|verify} messages.
		 * @param message UserProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: users.IUserProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a UserProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns UserProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): users.UserProto;

		/**
		 * Decodes a UserProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns UserProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): users.UserProto;

		/**
		 * Verifies a UserProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a UserProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns UserProto
		 */
		public static fromObject(object: { [k: string]: any }): users.UserProto;

		/**
		 * Creates a plain object from a UserProto message. Also converts values to other types if specified.
		 * @param message UserProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: users.UserProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this UserProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for UserProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProfileProto. */
	interface IProfileProto {
		/** ProfileProto id */
		id?: string | null;

		/** ProfileProto userId */
		userId?: string | null;

		/** ProfileProto bio */
		bio?: string | null;

		/** ProfileProto position */
		position?: string | null;

		/** ProfileProto department */
		department?: string | null;

		/** ProfileProto phoneNumber */
		phoneNumber?: string | null;

		/** ProfileProto profileImageUrl */
		profileImageUrl?: string | null;

		/** ProfileProto createdAt */
		createdAt?: string | null;

		/** ProfileProto updatedAt */
		updatedAt?: string | null;
	}

	/** Represents a ProfileProto. */
	class ProfileProto implements IProfileProto {
		/**
		 * Constructs a new ProfileProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: users.IProfileProto);

		/** ProfileProto id. */
		public id: string;

		/** ProfileProto userId. */
		public userId: string;

		/** ProfileProto bio. */
		public bio: string;

		/** ProfileProto position. */
		public position: string;

		/** ProfileProto department. */
		public department: string;

		/** ProfileProto phoneNumber. */
		public phoneNumber: string;

		/** ProfileProto profileImageUrl. */
		public profileImageUrl: string;

		/** ProfileProto createdAt. */
		public createdAt: string;

		/** ProfileProto updatedAt. */
		public updatedAt: string;

		/**
		 * Creates a new ProfileProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProfileProto instance
		 */
		public static create(properties?: users.IProfileProto): users.ProfileProto;

		/**
		 * Encodes the specified ProfileProto message. Does not implicitly {@link users.ProfileProto.verify|verify} messages.
		 * @param message ProfileProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: users.IProfileProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProfileProto message, length delimited. Does not implicitly {@link users.ProfileProto.verify|verify} messages.
		 * @param message ProfileProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: users.IProfileProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProfileProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProfileProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): users.ProfileProto;

		/**
		 * Decodes a ProfileProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProfileProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): users.ProfileProto;

		/**
		 * Verifies a ProfileProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProfileProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProfileProto
		 */
		public static fromObject(object: { [k: string]: any }): users.ProfileProto;

		/**
		 * Creates a plain object from a ProfileProto message. Also converts values to other types if specified.
		 * @param message ProfileProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: users.ProfileProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProfileProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProfileProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a UserCollection. */
	interface IUserCollection {
		/** UserCollection users */
		users?: users.IUserProto[] | null;
	}

	/** Represents a UserCollection. */
	class UserCollection implements IUserCollection {
		/**
		 * Constructs a new UserCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: users.IUserCollection);

		/** UserCollection users. */
		public users: users.IUserProto[];

		/**
		 * Creates a new UserCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns UserCollection instance
		 */
		public static create(
			properties?: users.IUserCollection,
		): users.UserCollection;

		/**
		 * Encodes the specified UserCollection message. Does not implicitly {@link users.UserCollection.verify|verify} messages.
		 * @param message UserCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: users.IUserCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified UserCollection message, length delimited. Does not implicitly {@link users.UserCollection.verify|verify} messages.
		 * @param message UserCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: users.IUserCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a UserCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns UserCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): users.UserCollection;

		/**
		 * Decodes a UserCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns UserCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): users.UserCollection;

		/**
		 * Verifies a UserCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a UserCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns UserCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): users.UserCollection;

		/**
		 * Creates a plain object from a UserCollection message. Also converts values to other types if specified.
		 * @param message UserCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: users.UserCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this UserCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for UserCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ProfileCollection. */
	interface IProfileCollection {
		/** ProfileCollection profiles */
		profiles?: users.IProfileProto[] | null;
	}

	/** Represents a ProfileCollection. */
	class ProfileCollection implements IProfileCollection {
		/**
		 * Constructs a new ProfileCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: users.IProfileCollection);

		/** ProfileCollection profiles. */
		public profiles: users.IProfileProto[];

		/**
		 * Creates a new ProfileCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ProfileCollection instance
		 */
		public static create(
			properties?: users.IProfileCollection,
		): users.ProfileCollection;

		/**
		 * Encodes the specified ProfileCollection message. Does not implicitly {@link users.ProfileCollection.verify|verify} messages.
		 * @param message ProfileCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: users.IProfileCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ProfileCollection message, length delimited. Does not implicitly {@link users.ProfileCollection.verify|verify} messages.
		 * @param message ProfileCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: users.IProfileCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ProfileCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ProfileCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): users.ProfileCollection;

		/**
		 * Decodes a ProfileCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ProfileCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): users.ProfileCollection;

		/**
		 * Verifies a ProfileCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ProfileCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ProfileCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): users.ProfileCollection;

		/**
		 * Creates a plain object from a ProfileCollection message. Also converts values to other types if specified.
		 * @param message ProfileCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: users.ProfileCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ProfileCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ProfileCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}

/** Namespace auditing. */
export namespace auditing {
	/** Properties of a MitigationProto. */
	interface IMitigationProto {
		/** MitigationProto id */
		id?: string | null;

		/** MitigationProto auditEntryId */
		auditEntryId?: string | null;

		/** MitigationProto description */
		description?: string | null;

		/** MitigationProto status */
		status?: string | null;

		/** MitigationProto createdAt */
		createdAt?: string | null;
	}

	/** Represents a MitigationProto. */
	class MitigationProto implements IMitigationProto {
		/**
		 * Constructs a new MitigationProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IMitigationProto);

		/** MitigationProto id. */
		public id: string;

		/** MitigationProto auditEntryId. */
		public auditEntryId: string;

		/** MitigationProto description. */
		public description: string;

		/** MitigationProto status. */
		public status: string;

		/** MitigationProto createdAt. */
		public createdAt: string;

		/**
		 * Creates a new MitigationProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns MitigationProto instance
		 */
		public static create(
			properties?: auditing.IMitigationProto,
		): auditing.MitigationProto;

		/**
		 * Encodes the specified MitigationProto message. Does not implicitly {@link auditing.MitigationProto.verify|verify} messages.
		 * @param message MitigationProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IMitigationProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified MitigationProto message, length delimited. Does not implicitly {@link auditing.MitigationProto.verify|verify} messages.
		 * @param message MitigationProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IMitigationProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a MitigationProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns MitigationProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.MitigationProto;

		/**
		 * Decodes a MitigationProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns MitigationProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.MitigationProto;

		/**
		 * Verifies a MitigationProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a MitigationProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns MitigationProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.MitigationProto;

		/**
		 * Creates a plain object from a MitigationProto message. Also converts values to other types if specified.
		 * @param message MitigationProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.MitigationProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this MitigationProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for MitigationProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CorrectiveActionProto. */
	interface ICorrectiveActionProto {
		/** CorrectiveActionProto id */
		id?: string | null;

		/** CorrectiveActionProto mitigationId */
		mitigationId?: string | null;

		/** CorrectiveActionProto task */
		task?: string | null;

		/** CorrectiveActionProto status */
		status?: string | null;

		/** CorrectiveActionProto assignedToUserId */
		assignedToUserId?: string | null;

		/** CorrectiveActionProto createdAt */
		createdAt?: string | null;

		/** CorrectiveActionProto dueDate */
		dueDate?: string | null;
	}

	/** Represents a CorrectiveActionProto. */
	class CorrectiveActionProto implements ICorrectiveActionProto {
		/**
		 * Constructs a new CorrectiveActionProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.ICorrectiveActionProto);

		/** CorrectiveActionProto id. */
		public id: string;

		/** CorrectiveActionProto mitigationId. */
		public mitigationId: string;

		/** CorrectiveActionProto task. */
		public task: string;

		/** CorrectiveActionProto status. */
		public status: string;

		/** CorrectiveActionProto assignedToUserId. */
		public assignedToUserId: string;

		/** CorrectiveActionProto createdAt. */
		public createdAt: string;

		/** CorrectiveActionProto dueDate. */
		public dueDate: string;

		/**
		 * Creates a new CorrectiveActionProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CorrectiveActionProto instance
		 */
		public static create(
			properties?: auditing.ICorrectiveActionProto,
		): auditing.CorrectiveActionProto;

		/**
		 * Encodes the specified CorrectiveActionProto message. Does not implicitly {@link auditing.CorrectiveActionProto.verify|verify} messages.
		 * @param message CorrectiveActionProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.ICorrectiveActionProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CorrectiveActionProto message, length delimited. Does not implicitly {@link auditing.CorrectiveActionProto.verify|verify} messages.
		 * @param message CorrectiveActionProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.ICorrectiveActionProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CorrectiveActionProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CorrectiveActionProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.CorrectiveActionProto;

		/**
		 * Decodes a CorrectiveActionProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CorrectiveActionProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.CorrectiveActionProto;

		/**
		 * Verifies a CorrectiveActionProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CorrectiveActionProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CorrectiveActionProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.CorrectiveActionProto;

		/**
		 * Creates a plain object from a CorrectiveActionProto message. Also converts values to other types if specified.
		 * @param message CorrectiveActionProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.CorrectiveActionProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CorrectiveActionProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CorrectiveActionProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of an AuditProto. */
	interface IAuditProto {
		/** AuditProto id */
		id?: string | null;

		/** AuditProto name */
		name?: string | null;

		/** AuditProto createdAt */
		createdAt?: string | null;

		/** AuditProto mechanismIds */
		mechanismIds?: string[] | null;
	}

	/** Represents an AuditProto. */
	class AuditProto implements IAuditProto {
		/**
		 * Constructs a new AuditProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IAuditProto);

		/** AuditProto id. */
		public id: string;

		/** AuditProto name. */
		public name: string;

		/** AuditProto createdAt. */
		public createdAt: string;

		/** AuditProto mechanismIds. */
		public mechanismIds: string[];

		/**
		 * Creates a new AuditProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns AuditProto instance
		 */
		public static create(
			properties?: auditing.IAuditProto,
		): auditing.AuditProto;

		/**
		 * Encodes the specified AuditProto message. Does not implicitly {@link auditing.AuditProto.verify|verify} messages.
		 * @param message AuditProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IAuditProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified AuditProto message, length delimited. Does not implicitly {@link auditing.AuditProto.verify|verify} messages.
		 * @param message AuditProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IAuditProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes an AuditProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns AuditProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.AuditProto;

		/**
		 * Decodes an AuditProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns AuditProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.AuditProto;

		/**
		 * Verifies an AuditProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates an AuditProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns AuditProto
		 */
		public static fromObject(object: { [k: string]: any }): auditing.AuditProto;

		/**
		 * Creates a plain object from an AuditProto message. Also converts values to other types if specified.
		 * @param message AuditProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.AuditProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this AuditProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for AuditProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of an AuditEntryProto. */
	interface IAuditEntryProto {
		/** AuditEntryProto id */
		id?: string | null;

		/** AuditEntryProto auditId */
		auditId?: string | null;

		/** AuditEntryProto obligationId */
		obligationId?: string | null;

		/** AuditEntryProto status */
		status?: string | null;

		/** AuditEntryProto finding */
		finding?: string | null;
	}

	/** Represents an AuditEntryProto. */
	class AuditEntryProto implements IAuditEntryProto {
		/**
		 * Constructs a new AuditEntryProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IAuditEntryProto);

		/** AuditEntryProto id. */
		public id: string;

		/** AuditEntryProto auditId. */
		public auditId: string;

		/** AuditEntryProto obligationId. */
		public obligationId: string;

		/** AuditEntryProto status. */
		public status: string;

		/** AuditEntryProto finding. */
		public finding: string;

		/**
		 * Creates a new AuditEntryProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns AuditEntryProto instance
		 */
		public static create(
			properties?: auditing.IAuditEntryProto,
		): auditing.AuditEntryProto;

		/**
		 * Encodes the specified AuditEntryProto message. Does not implicitly {@link auditing.AuditEntryProto.verify|verify} messages.
		 * @param message AuditEntryProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IAuditEntryProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified AuditEntryProto message, length delimited. Does not implicitly {@link auditing.AuditEntryProto.verify|verify} messages.
		 * @param message AuditEntryProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IAuditEntryProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes an AuditEntryProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns AuditEntryProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.AuditEntryProto;

		/**
		 * Decodes an AuditEntryProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns AuditEntryProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.AuditEntryProto;

		/**
		 * Verifies an AuditEntryProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates an AuditEntryProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns AuditEntryProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.AuditEntryProto;

		/**
		 * Creates a plain object from an AuditEntryProto message. Also converts values to other types if specified.
		 * @param message AuditEntryProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.AuditEntryProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this AuditEntryProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for AuditEntryProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ComplianceCommentProto. */
	interface IComplianceCommentProto {
		/** ComplianceCommentProto id */
		id?: string | null;

		/** ComplianceCommentProto obligationId */
		obligationId?: string | null;

		/** ComplianceCommentProto text */
		text?: string | null;

		/** ComplianceCommentProto createdAt */
		createdAt?: string | null;
	}

	/** Represents a ComplianceCommentProto. */
	class ComplianceCommentProto implements IComplianceCommentProto {
		/**
		 * Constructs a new ComplianceCommentProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IComplianceCommentProto);

		/** ComplianceCommentProto id. */
		public id: string;

		/** ComplianceCommentProto obligationId. */
		public obligationId: string;

		/** ComplianceCommentProto text. */
		public text: string;

		/** ComplianceCommentProto createdAt. */
		public createdAt: string;

		/**
		 * Creates a new ComplianceCommentProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ComplianceCommentProto instance
		 */
		public static create(
			properties?: auditing.IComplianceCommentProto,
		): auditing.ComplianceCommentProto;

		/**
		 * Encodes the specified ComplianceCommentProto message. Does not implicitly {@link auditing.ComplianceCommentProto.verify|verify} messages.
		 * @param message ComplianceCommentProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IComplianceCommentProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ComplianceCommentProto message, length delimited. Does not implicitly {@link auditing.ComplianceCommentProto.verify|verify} messages.
		 * @param message ComplianceCommentProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IComplianceCommentProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ComplianceCommentProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ComplianceCommentProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.ComplianceCommentProto;

		/**
		 * Decodes a ComplianceCommentProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ComplianceCommentProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.ComplianceCommentProto;

		/**
		 * Verifies a ComplianceCommentProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ComplianceCommentProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ComplianceCommentProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.ComplianceCommentProto;

		/**
		 * Creates a plain object from a ComplianceCommentProto message. Also converts values to other types if specified.
		 * @param message ComplianceCommentProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.ComplianceCommentProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ComplianceCommentProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ComplianceCommentProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a NonConformanceCommentProto. */
	interface INonConformanceCommentProto {
		/** NonConformanceCommentProto id */
		id?: string | null;

		/** NonConformanceCommentProto obligationId */
		obligationId?: string | null;

		/** NonConformanceCommentProto text */
		text?: string | null;

		/** NonConformanceCommentProto createdAt */
		createdAt?: string | null;
	}

	/** Represents a NonConformanceCommentProto. */
	class NonConformanceCommentProto implements INonConformanceCommentProto {
		/**
		 * Constructs a new NonConformanceCommentProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.INonConformanceCommentProto);

		/** NonConformanceCommentProto id. */
		public id: string;

		/** NonConformanceCommentProto obligationId. */
		public obligationId: string;

		/** NonConformanceCommentProto text. */
		public text: string;

		/** NonConformanceCommentProto createdAt. */
		public createdAt: string;

		/**
		 * Creates a new NonConformanceCommentProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns NonConformanceCommentProto instance
		 */
		public static create(
			properties?: auditing.INonConformanceCommentProto,
		): auditing.NonConformanceCommentProto;

		/**
		 * Encodes the specified NonConformanceCommentProto message. Does not implicitly {@link auditing.NonConformanceCommentProto.verify|verify} messages.
		 * @param message NonConformanceCommentProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.INonConformanceCommentProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified NonConformanceCommentProto message, length delimited. Does not implicitly {@link auditing.NonConformanceCommentProto.verify|verify} messages.
		 * @param message NonConformanceCommentProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.INonConformanceCommentProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a NonConformanceCommentProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns NonConformanceCommentProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.NonConformanceCommentProto;

		/**
		 * Decodes a NonConformanceCommentProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns NonConformanceCommentProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.NonConformanceCommentProto;

		/**
		 * Verifies a NonConformanceCommentProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a NonConformanceCommentProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns NonConformanceCommentProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.NonConformanceCommentProto;

		/**
		 * Creates a plain object from a NonConformanceCommentProto message. Also converts values to other types if specified.
		 * @param message NonConformanceCommentProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.NonConformanceCommentProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this NonConformanceCommentProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for NonConformanceCommentProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a MitigationCollection. */
	interface IMitigationCollection {
		/** MitigationCollection mitigations */
		mitigations?: auditing.IMitigationProto[] | null;
	}

	/** Represents a MitigationCollection. */
	class MitigationCollection implements IMitigationCollection {
		/**
		 * Constructs a new MitigationCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IMitigationCollection);

		/** MitigationCollection mitigations. */
		public mitigations: auditing.IMitigationProto[];

		/**
		 * Creates a new MitigationCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns MitigationCollection instance
		 */
		public static create(
			properties?: auditing.IMitigationCollection,
		): auditing.MitigationCollection;

		/**
		 * Encodes the specified MitigationCollection message. Does not implicitly {@link auditing.MitigationCollection.verify|verify} messages.
		 * @param message MitigationCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IMitigationCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified MitigationCollection message, length delimited. Does not implicitly {@link auditing.MitigationCollection.verify|verify} messages.
		 * @param message MitigationCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IMitigationCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a MitigationCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns MitigationCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.MitigationCollection;

		/**
		 * Decodes a MitigationCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns MitigationCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.MitigationCollection;

		/**
		 * Verifies a MitigationCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a MitigationCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns MitigationCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.MitigationCollection;

		/**
		 * Creates a plain object from a MitigationCollection message. Also converts values to other types if specified.
		 * @param message MitigationCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.MitigationCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this MitigationCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for MitigationCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a CorrectiveActionCollection. */
	interface ICorrectiveActionCollection {
		/** CorrectiveActionCollection correctiveActions */
		correctiveActions?: auditing.ICorrectiveActionProto[] | null;
	}

	/** Represents a CorrectiveActionCollection. */
	class CorrectiveActionCollection implements ICorrectiveActionCollection {
		/**
		 * Constructs a new CorrectiveActionCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.ICorrectiveActionCollection);

		/** CorrectiveActionCollection correctiveActions. */
		public correctiveActions: auditing.ICorrectiveActionProto[];

		/**
		 * Creates a new CorrectiveActionCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns CorrectiveActionCollection instance
		 */
		public static create(
			properties?: auditing.ICorrectiveActionCollection,
		): auditing.CorrectiveActionCollection;

		/**
		 * Encodes the specified CorrectiveActionCollection message. Does not implicitly {@link auditing.CorrectiveActionCollection.verify|verify} messages.
		 * @param message CorrectiveActionCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.ICorrectiveActionCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified CorrectiveActionCollection message, length delimited. Does not implicitly {@link auditing.CorrectiveActionCollection.verify|verify} messages.
		 * @param message CorrectiveActionCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.ICorrectiveActionCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a CorrectiveActionCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns CorrectiveActionCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.CorrectiveActionCollection;

		/**
		 * Decodes a CorrectiveActionCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns CorrectiveActionCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.CorrectiveActionCollection;

		/**
		 * Verifies a CorrectiveActionCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a CorrectiveActionCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns CorrectiveActionCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.CorrectiveActionCollection;

		/**
		 * Creates a plain object from a CorrectiveActionCollection message. Also converts values to other types if specified.
		 * @param message CorrectiveActionCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.CorrectiveActionCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this CorrectiveActionCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for CorrectiveActionCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of an AuditCollection. */
	interface IAuditCollection {
		/** AuditCollection audits */
		audits?: auditing.IAuditProto[] | null;
	}

	/** Represents an AuditCollection. */
	class AuditCollection implements IAuditCollection {
		/**
		 * Constructs a new AuditCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IAuditCollection);

		/** AuditCollection audits. */
		public audits: auditing.IAuditProto[];

		/**
		 * Creates a new AuditCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns AuditCollection instance
		 */
		public static create(
			properties?: auditing.IAuditCollection,
		): auditing.AuditCollection;

		/**
		 * Encodes the specified AuditCollection message. Does not implicitly {@link auditing.AuditCollection.verify|verify} messages.
		 * @param message AuditCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IAuditCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified AuditCollection message, length delimited. Does not implicitly {@link auditing.AuditCollection.verify|verify} messages.
		 * @param message AuditCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IAuditCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes an AuditCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns AuditCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.AuditCollection;

		/**
		 * Decodes an AuditCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns AuditCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.AuditCollection;

		/**
		 * Verifies an AuditCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates an AuditCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns AuditCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.AuditCollection;

		/**
		 * Creates a plain object from an AuditCollection message. Also converts values to other types if specified.
		 * @param message AuditCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.AuditCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this AuditCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for AuditCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of an AuditEntryCollection. */
	interface IAuditEntryCollection {
		/** AuditEntryCollection auditEntries */
		auditEntries?: auditing.IAuditEntryProto[] | null;
	}

	/** Represents an AuditEntryCollection. */
	class AuditEntryCollection implements IAuditEntryCollection {
		/**
		 * Constructs a new AuditEntryCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IAuditEntryCollection);

		/** AuditEntryCollection auditEntries. */
		public auditEntries: auditing.IAuditEntryProto[];

		/**
		 * Creates a new AuditEntryCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns AuditEntryCollection instance
		 */
		public static create(
			properties?: auditing.IAuditEntryCollection,
		): auditing.AuditEntryCollection;

		/**
		 * Encodes the specified AuditEntryCollection message. Does not implicitly {@link auditing.AuditEntryCollection.verify|verify} messages.
		 * @param message AuditEntryCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IAuditEntryCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified AuditEntryCollection message, length delimited. Does not implicitly {@link auditing.AuditEntryCollection.verify|verify} messages.
		 * @param message AuditEntryCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IAuditEntryCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes an AuditEntryCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns AuditEntryCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.AuditEntryCollection;

		/**
		 * Decodes an AuditEntryCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns AuditEntryCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.AuditEntryCollection;

		/**
		 * Verifies an AuditEntryCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates an AuditEntryCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns AuditEntryCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.AuditEntryCollection;

		/**
		 * Creates a plain object from an AuditEntryCollection message. Also converts values to other types if specified.
		 * @param message AuditEntryCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.AuditEntryCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this AuditEntryCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for AuditEntryCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a ComplianceCommentCollection. */
	interface IComplianceCommentCollection {
		/** ComplianceCommentCollection complianceComments */
		complianceComments?: auditing.IComplianceCommentProto[] | null;
	}

	/** Represents a ComplianceCommentCollection. */
	class ComplianceCommentCollection implements IComplianceCommentCollection {
		/**
		 * Constructs a new ComplianceCommentCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.IComplianceCommentCollection);

		/** ComplianceCommentCollection complianceComments. */
		public complianceComments: auditing.IComplianceCommentProto[];

		/**
		 * Creates a new ComplianceCommentCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ComplianceCommentCollection instance
		 */
		public static create(
			properties?: auditing.IComplianceCommentCollection,
		): auditing.ComplianceCommentCollection;

		/**
		 * Encodes the specified ComplianceCommentCollection message. Does not implicitly {@link auditing.ComplianceCommentCollection.verify|verify} messages.
		 * @param message ComplianceCommentCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.IComplianceCommentCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ComplianceCommentCollection message, length delimited. Does not implicitly {@link auditing.ComplianceCommentCollection.verify|verify} messages.
		 * @param message ComplianceCommentCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.IComplianceCommentCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ComplianceCommentCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ComplianceCommentCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.ComplianceCommentCollection;

		/**
		 * Decodes a ComplianceCommentCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ComplianceCommentCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.ComplianceCommentCollection;

		/**
		 * Verifies a ComplianceCommentCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ComplianceCommentCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ComplianceCommentCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.ComplianceCommentCollection;

		/**
		 * Creates a plain object from a ComplianceCommentCollection message. Also converts values to other types if specified.
		 * @param message ComplianceCommentCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.ComplianceCommentCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ComplianceCommentCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ComplianceCommentCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of a NonConformanceCommentCollection. */
	interface INonConformanceCommentCollection {
		/** NonConformanceCommentCollection nonConformanceComments */
		nonConformanceComments?: auditing.INonConformanceCommentProto[] | null;
	}

	/** Represents a NonConformanceCommentCollection. */
	class NonConformanceCommentCollection
		implements INonConformanceCommentCollection
	{
		/**
		 * Constructs a new NonConformanceCommentCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: auditing.INonConformanceCommentCollection);

		/** NonConformanceCommentCollection nonConformanceComments. */
		public nonConformanceComments: auditing.INonConformanceCommentProto[];

		/**
		 * Creates a new NonConformanceCommentCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns NonConformanceCommentCollection instance
		 */
		public static create(
			properties?: auditing.INonConformanceCommentCollection,
		): auditing.NonConformanceCommentCollection;

		/**
		 * Encodes the specified NonConformanceCommentCollection message. Does not implicitly {@link auditing.NonConformanceCommentCollection.verify|verify} messages.
		 * @param message NonConformanceCommentCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: auditing.INonConformanceCommentCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified NonConformanceCommentCollection message, length delimited. Does not implicitly {@link auditing.NonConformanceCommentCollection.verify|verify} messages.
		 * @param message NonConformanceCommentCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: auditing.INonConformanceCommentCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a NonConformanceCommentCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns NonConformanceCommentCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): auditing.NonConformanceCommentCollection;

		/**
		 * Decodes a NonConformanceCommentCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns NonConformanceCommentCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): auditing.NonConformanceCommentCollection;

		/**
		 * Verifies a NonConformanceCommentCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a NonConformanceCommentCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns NonConformanceCommentCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): auditing.NonConformanceCommentCollection;

		/**
		 * Creates a plain object from a NonConformanceCommentCollection message. Also converts values to other types if specified.
		 * @param message NonConformanceCommentCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: auditing.NonConformanceCommentCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this NonConformanceCommentCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for NonConformanceCommentCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}

/** Namespace obligations. */
export namespace obligations {
	/** Properties of an ObligationProto. */
	interface IObligationProto {
		/** ObligationProto obligationNumber */
		obligationNumber?: string | null;

		/** ObligationProto projectId */
		projectId?: string | null;

		/** ObligationProto primaryEnvironmentalMechanismId */
		primaryEnvironmentalMechanismId?: string | null;

		/** ObligationProto procedure */
		procedure?: string | null;

		/** ObligationProto environmentalAspect */
		environmentalAspect?: string | null;

		/** ObligationProto customEnvironmentalAspect */
		customEnvironmentalAspect?: string | null;

		/** ObligationProto obligation */
		obligation?: string | null;

		/** ObligationProto accountability */
		accountability?: string | null;

		/** ObligationProto responsibleUserIds */
		responsibleUserIds?: string[] | null;

		/** ObligationProto projectPhase */
		projectPhase?: string | null;

		/** ObligationProto actionDueDate */
		actionDueDate?: string | null;

		/** ObligationProto closeOutDate */
		closeOutDate?: string | null;

		/** ObligationProto status */
		status?: string | null;

		/** ObligationProto supportingInformation */
		supportingInformation?: string | null;

		/** ObligationProto generalComments */
		generalComments?: string | null;

		/** ObligationProto evidenceNotes */
		evidenceNotes?: string | null;

		/** ObligationProto recurringObligation */
		recurringObligation?: boolean | null;

		/** ObligationProto recurringFrequency */
		recurringFrequency?: string | null;

		/** ObligationProto recurringStatus */
		recurringStatus?: string | null;

		/** ObligationProto recurringForecastedDate */
		recurringForecastedDate?: string | null;

		/** ObligationProto inspection */
		inspection?: boolean | null;

		/** ObligationProto inspectionFrequency */
		inspectionFrequency?: string | null;

		/** ObligationProto siteOrDesktop */
		siteOrDesktop?: string | null;

		/** ObligationProto newControlActionRequired */
		newControlActionRequired?: boolean | null;

		/** ObligationProto obligationType */
		obligationType?: string | null;

		/** ObligationProto gapAnalysis */
		gapAnalysis?: boolean | null;

		/** ObligationProto notesForGapAnalysis */
		notesForGapAnalysis?: string | null;

		/** ObligationProto createdAt */
		createdAt?: string | null;

		/** ObligationProto updatedAt */
		updatedAt?: string | null;
	}

	/** Represents an ObligationProto. */
	class ObligationProto implements IObligationProto {
		/**
		 * Constructs a new ObligationProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: obligations.IObligationProto);

		/** ObligationProto obligationNumber. */
		public obligationNumber: string;

		/** ObligationProto projectId. */
		public projectId: string;

		/** ObligationProto primaryEnvironmentalMechanismId. */
		public primaryEnvironmentalMechanismId: string;

		/** ObligationProto procedure. */
		public procedure: string;

		/** ObligationProto environmentalAspect. */
		public environmentalAspect: string;

		/** ObligationProto customEnvironmentalAspect. */
		public customEnvironmentalAspect: string;

		/** ObligationProto obligation. */
		public obligation: string;

		/** ObligationProto accountability. */
		public accountability: string;

		/** ObligationProto responsibleUserIds. */
		public responsibleUserIds: string[];

		/** ObligationProto projectPhase. */
		public projectPhase: string;

		/** ObligationProto actionDueDate. */
		public actionDueDate: string;

		/** ObligationProto closeOutDate. */
		public closeOutDate: string;

		/** ObligationProto status. */
		public status: string;

		/** ObligationProto supportingInformation. */
		public supportingInformation: string;

		/** ObligationProto generalComments. */
		public generalComments: string;

		/** ObligationProto evidenceNotes. */
		public evidenceNotes: string;

		/** ObligationProto recurringObligation. */
		public recurringObligation: boolean;

		/** ObligationProto recurringFrequency. */
		public recurringFrequency: string;

		/** ObligationProto recurringStatus. */
		public recurringStatus: string;

		/** ObligationProto recurringForecastedDate. */
		public recurringForecastedDate: string;

		/** ObligationProto inspection. */
		public inspection: boolean;

		/** ObligationProto inspectionFrequency. */
		public inspectionFrequency: string;

		/** ObligationProto siteOrDesktop. */
		public siteOrDesktop: string;

		/** ObligationProto newControlActionRequired. */
		public newControlActionRequired: boolean;

		/** ObligationProto obligationType. */
		public obligationType: string;

		/** ObligationProto gapAnalysis. */
		public gapAnalysis: boolean;

		/** ObligationProto notesForGapAnalysis. */
		public notesForGapAnalysis: string;

		/** ObligationProto createdAt. */
		public createdAt: string;

		/** ObligationProto updatedAt. */
		public updatedAt: string;

		/**
		 * Creates a new ObligationProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ObligationProto instance
		 */
		public static create(
			properties?: obligations.IObligationProto,
		): obligations.ObligationProto;

		/**
		 * Encodes the specified ObligationProto message. Does not implicitly {@link obligations.ObligationProto.verify|verify} messages.
		 * @param message ObligationProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: obligations.IObligationProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ObligationProto message, length delimited. Does not implicitly {@link obligations.ObligationProto.verify|verify} messages.
		 * @param message ObligationProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: obligations.IObligationProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes an ObligationProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ObligationProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): obligations.ObligationProto;

		/**
		 * Decodes an ObligationProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ObligationProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): obligations.ObligationProto;

		/**
		 * Verifies an ObligationProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates an ObligationProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ObligationProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): obligations.ObligationProto;

		/**
		 * Creates a plain object from an ObligationProto message. Also converts values to other types if specified.
		 * @param message ObligationProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: obligations.ObligationProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ObligationProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ObligationProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	/** Properties of an ObligationCollection. */
	interface IObligationCollection {
		/** ObligationCollection obligations */
		obligations?: obligations.IObligationProto[] | null;
	}

	/** Represents an ObligationCollection. */
	class ObligationCollection implements IObligationCollection {
		/**
		 * Constructs a new ObligationCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: obligations.IObligationCollection);

		/** ObligationCollection obligations. */
		public obligations: obligations.IObligationProto[];

		/**
		 * Creates a new ObligationCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ObligationCollection instance
		 */
		public static create(
			properties?: obligations.IObligationCollection,
		): obligations.ObligationCollection;

		/**
		 * Encodes the specified ObligationCollection message. Does not implicitly {@link obligations.ObligationCollection.verify|verify} messages.
		 * @param message ObligationCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: obligations.IObligationCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ObligationCollection message, length delimited. Does not implicitly {@link obligations.ObligationCollection.verify|verify} messages.
		 * @param message ObligationCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: obligations.IObligationCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes an ObligationCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ObligationCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): obligations.ObligationCollection;

		/**
		 * Decodes an ObligationCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ObligationCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): obligations.ObligationCollection;

		/**
		 * Verifies an ObligationCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates an ObligationCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ObligationCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): obligations.ObligationCollection;

		/**
		 * Creates a plain object from an ObligationCollection message. Also converts values to other types if specified.
		 * @param message ObligationCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: obligations.ObligationCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ObligationCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ObligationCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}

/** Namespace greenova. */
export namespace greenova {
	/** Namespace mechanisms. */
	namespace mechanisms {
		/** ObligationStatus enum. */
		enum ObligationStatus {
			STATUS_UNKNOWN = 0,
			STATUS_NOT_STARTED = 1,
			STATUS_IN_PROGRESS = 2,
			STATUS_COMPLETED = 3,
			STATUS_OVERDUE = 4,
		}

		/** Properties of an ObligationInsight. */
		interface IObligationInsight {
			/** ObligationInsight obligationNumber */
			obligationNumber?: string | null;

			/** ObligationInsight dueDate */
			dueDate?: string | null;

			/** ObligationInsight closeOutDate */
			closeOutDate?: string | null;
		}

		/** Represents an ObligationInsight. */
		class ObligationInsight implements IObligationInsight {
			/**
			 * Constructs a new ObligationInsight.
			 * @param [properties] Properties to set
			 */
			constructor(properties?: greenova.mechanisms.IObligationInsight);

			/** ObligationInsight obligationNumber. */
			public obligationNumber: string;

			/** ObligationInsight dueDate. */
			public dueDate: string;

			/** ObligationInsight closeOutDate. */
			public closeOutDate: string;

			/**
			 * Creates a new ObligationInsight instance using the specified properties.
			 * @param [properties] Properties to set
			 * @returns ObligationInsight instance
			 */
			public static create(
				properties?: greenova.mechanisms.IObligationInsight,
			): greenova.mechanisms.ObligationInsight;

			/**
			 * Encodes the specified ObligationInsight message. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
			 * @param message ObligationInsight message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encode(
				message: greenova.mechanisms.IObligationInsight,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Encodes the specified ObligationInsight message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
			 * @param message ObligationInsight message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encodeDelimited(
				message: greenova.mechanisms.IObligationInsight,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Decodes an ObligationInsight message from the specified reader or buffer.
			 * @param reader Reader or buffer to decode from
			 * @param [length] Message length if known beforehand
			 * @returns ObligationInsight
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decode(
				reader: $protobuf.Reader | Uint8Array,
				length?: number,
			): greenova.mechanisms.ObligationInsight;

			/**
			 * Decodes an ObligationInsight message from the specified reader or buffer, length delimited.
			 * @param reader Reader or buffer to decode from
			 * @returns ObligationInsight
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decodeDelimited(
				reader: $protobuf.Reader | Uint8Array,
			): greenova.mechanisms.ObligationInsight;

			/**
			 * Verifies an ObligationInsight message.
			 * @param message Plain object to verify
			 * @returns `null` if valid, otherwise the reason why it is not
			 */
			public static verify(message: { [k: string]: any }): string | null;

			/**
			 * Creates an ObligationInsight message from a plain object. Also converts values to their respective internal types.
			 * @param object Plain object
			 * @returns ObligationInsight
			 */
			public static fromObject(object: {
				[k: string]: any;
			}): greenova.mechanisms.ObligationInsight;

			/**
			 * Creates a plain object from an ObligationInsight message. Also converts values to other types if specified.
			 * @param message ObligationInsight
			 * @param [options] Conversion options
			 * @returns Plain object
			 */
			public static toObject(
				message: greenova.mechanisms.ObligationInsight,
				options?: $protobuf.IConversionOptions,
			): { [k: string]: any };

			/**
			 * Converts this ObligationInsight to JSON.
			 * @returns JSON object
			 */
			public toJSON(): { [k: string]: any };

			/**
			 * Gets the default type url for ObligationInsight
			 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
			 * @returns The default type url
			 */
			public static getTypeUrl(typeUrlPrefix?: string): string;
		}

		/** Properties of an ObligationInsightResponse. */
		interface IObligationInsightResponse {
			/** ObligationInsightResponse mechanismId */
			mechanismId?: number | null;

			/** ObligationInsightResponse status */
			status?: string | null;

			/** ObligationInsightResponse statusKey */
			statusKey?: string | null;

			/** ObligationInsightResponse count */
			count?: number | null;

			/** ObligationInsightResponse totalCount */
			totalCount?: number | null;

			/** ObligationInsightResponse obligations */
			obligations?: greenova.mechanisms.IObligationInsight[] | null;

			/** ObligationInsightResponse error */
			error?: string | null;
		}

		/** Represents an ObligationInsightResponse. */
		class ObligationInsightResponse implements IObligationInsightResponse {
			/**
			 * Constructs a new ObligationInsightResponse.
			 * @param [properties] Properties to set
			 */
			constructor(properties?: greenova.mechanisms.IObligationInsightResponse);

			/** ObligationInsightResponse mechanismId. */
			public mechanismId: number;

			/** ObligationInsightResponse status. */
			public status: string;

			/** ObligationInsightResponse statusKey. */
			public statusKey: string;

			/** ObligationInsightResponse count. */
			public count: number;

			/** ObligationInsightResponse totalCount. */
			public totalCount: number;

			/** ObligationInsightResponse obligations. */
			public obligations: greenova.mechanisms.IObligationInsight[];

			/** ObligationInsightResponse error. */
			public error: string;

			/**
			 * Creates a new ObligationInsightResponse instance using the specified properties.
			 * @param [properties] Properties to set
			 * @returns ObligationInsightResponse instance
			 */
			public static create(
				properties?: greenova.mechanisms.IObligationInsightResponse,
			): greenova.mechanisms.ObligationInsightResponse;

			/**
			 * Encodes the specified ObligationInsightResponse message. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
			 * @param message ObligationInsightResponse message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encode(
				message: greenova.mechanisms.IObligationInsightResponse,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Encodes the specified ObligationInsightResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
			 * @param message ObligationInsightResponse message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encodeDelimited(
				message: greenova.mechanisms.IObligationInsightResponse,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Decodes an ObligationInsightResponse message from the specified reader or buffer.
			 * @param reader Reader or buffer to decode from
			 * @param [length] Message length if known beforehand
			 * @returns ObligationInsightResponse
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decode(
				reader: $protobuf.Reader | Uint8Array,
				length?: number,
			): greenova.mechanisms.ObligationInsightResponse;

			/**
			 * Decodes an ObligationInsightResponse message from the specified reader or buffer, length delimited.
			 * @param reader Reader or buffer to decode from
			 * @returns ObligationInsightResponse
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decodeDelimited(
				reader: $protobuf.Reader | Uint8Array,
			): greenova.mechanisms.ObligationInsightResponse;

			/**
			 * Verifies an ObligationInsightResponse message.
			 * @param message Plain object to verify
			 * @returns `null` if valid, otherwise the reason why it is not
			 */
			public static verify(message: { [k: string]: any }): string | null;

			/**
			 * Creates an ObligationInsightResponse message from a plain object. Also converts values to their respective internal types.
			 * @param object Plain object
			 * @returns ObligationInsightResponse
			 */
			public static fromObject(object: {
				[k: string]: any;
			}): greenova.mechanisms.ObligationInsightResponse;

			/**
			 * Creates a plain object from an ObligationInsightResponse message. Also converts values to other types if specified.
			 * @param message ObligationInsightResponse
			 * @param [options] Conversion options
			 * @returns Plain object
			 */
			public static toObject(
				message: greenova.mechanisms.ObligationInsightResponse,
				options?: $protobuf.IConversionOptions,
			): { [k: string]: any };

			/**
			 * Converts this ObligationInsightResponse to JSON.
			 * @returns JSON object
			 */
			public toJSON(): { [k: string]: any };

			/**
			 * Gets the default type url for ObligationInsightResponse
			 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
			 * @returns The default type url
			 */
			public static getTypeUrl(typeUrlPrefix?: string): string;
		}

		/** Properties of a ChartSegment. */
		interface IChartSegment {
			/** ChartSegment label */
			label?: string | null;

			/** ChartSegment value */
			value?: number | null;

			/** ChartSegment color */
			color?: string | null;
		}

		/** Represents a ChartSegment. */
		class ChartSegment implements IChartSegment {
			/**
			 * Constructs a new ChartSegment.
			 * @param [properties] Properties to set
			 */
			constructor(properties?: greenova.mechanisms.IChartSegment);

			/** ChartSegment label. */
			public label: string;

			/** ChartSegment value. */
			public value: number;

			/** ChartSegment color. */
			public color: string;

			/**
			 * Creates a new ChartSegment instance using the specified properties.
			 * @param [properties] Properties to set
			 * @returns ChartSegment instance
			 */
			public static create(
				properties?: greenova.mechanisms.IChartSegment,
			): greenova.mechanisms.ChartSegment;

			/**
			 * Encodes the specified ChartSegment message. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
			 * @param message ChartSegment message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encode(
				message: greenova.mechanisms.IChartSegment,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Encodes the specified ChartSegment message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
			 * @param message ChartSegment message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encodeDelimited(
				message: greenova.mechanisms.IChartSegment,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Decodes a ChartSegment message from the specified reader or buffer.
			 * @param reader Reader or buffer to decode from
			 * @param [length] Message length if known beforehand
			 * @returns ChartSegment
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decode(
				reader: $protobuf.Reader | Uint8Array,
				length?: number,
			): greenova.mechanisms.ChartSegment;

			/**
			 * Decodes a ChartSegment message from the specified reader or buffer, length delimited.
			 * @param reader Reader or buffer to decode from
			 * @returns ChartSegment
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decodeDelimited(
				reader: $protobuf.Reader | Uint8Array,
			): greenova.mechanisms.ChartSegment;

			/**
			 * Verifies a ChartSegment message.
			 * @param message Plain object to verify
			 * @returns `null` if valid, otherwise the reason why it is not
			 */
			public static verify(message: { [k: string]: any }): string | null;

			/**
			 * Creates a ChartSegment message from a plain object. Also converts values to their respective internal types.
			 * @param object Plain object
			 * @returns ChartSegment
			 */
			public static fromObject(object: {
				[k: string]: any;
			}): greenova.mechanisms.ChartSegment;

			/**
			 * Creates a plain object from a ChartSegment message. Also converts values to other types if specified.
			 * @param message ChartSegment
			 * @param [options] Conversion options
			 * @returns Plain object
			 */
			public static toObject(
				message: greenova.mechanisms.ChartSegment,
				options?: $protobuf.IConversionOptions,
			): { [k: string]: any };

			/**
			 * Converts this ChartSegment to JSON.
			 * @returns JSON object
			 */
			public toJSON(): { [k: string]: any };

			/**
			 * Gets the default type url for ChartSegment
			 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
			 * @returns The default type url
			 */
			public static getTypeUrl(typeUrlPrefix?: string): string;
		}

		/** Properties of a ChartData. */
		interface IChartData {
			/** ChartData segments */
			segments?: greenova.mechanisms.IChartSegment[] | null;

			/** ChartData mechanismId */
			mechanismId?: number | null;

			/** ChartData mechanismName */
			mechanismName?: string | null;
		}

		/** Represents a ChartData. */
		class ChartData implements IChartData {
			/**
			 * Constructs a new ChartData.
			 * @param [properties] Properties to set
			 */
			constructor(properties?: greenova.mechanisms.IChartData);

			/** ChartData segments. */
			public segments: greenova.mechanisms.IChartSegment[];

			/** ChartData mechanismId. */
			public mechanismId: number;

			/** ChartData mechanismName. */
			public mechanismName: string;

			/**
			 * Creates a new ChartData instance using the specified properties.
			 * @param [properties] Properties to set
			 * @returns ChartData instance
			 */
			public static create(
				properties?: greenova.mechanisms.IChartData,
			): greenova.mechanisms.ChartData;

			/**
			 * Encodes the specified ChartData message. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
			 * @param message ChartData message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encode(
				message: greenova.mechanisms.IChartData,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Encodes the specified ChartData message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
			 * @param message ChartData message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encodeDelimited(
				message: greenova.mechanisms.IChartData,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Decodes a ChartData message from the specified reader or buffer.
			 * @param reader Reader or buffer to decode from
			 * @param [length] Message length if known beforehand
			 * @returns ChartData
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decode(
				reader: $protobuf.Reader | Uint8Array,
				length?: number,
			): greenova.mechanisms.ChartData;

			/**
			 * Decodes a ChartData message from the specified reader or buffer, length delimited.
			 * @param reader Reader or buffer to decode from
			 * @returns ChartData
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decodeDelimited(
				reader: $protobuf.Reader | Uint8Array,
			): greenova.mechanisms.ChartData;

			/**
			 * Verifies a ChartData message.
			 * @param message Plain object to verify
			 * @returns `null` if valid, otherwise the reason why it is not
			 */
			public static verify(message: { [k: string]: any }): string | null;

			/**
			 * Creates a ChartData message from a plain object. Also converts values to their respective internal types.
			 * @param object Plain object
			 * @returns ChartData
			 */
			public static fromObject(object: {
				[k: string]: any;
			}): greenova.mechanisms.ChartData;

			/**
			 * Creates a plain object from a ChartData message. Also converts values to other types if specified.
			 * @param message ChartData
			 * @param [options] Conversion options
			 * @returns Plain object
			 */
			public static toObject(
				message: greenova.mechanisms.ChartData,
				options?: $protobuf.IConversionOptions,
			): { [k: string]: any };

			/**
			 * Converts this ChartData to JSON.
			 * @returns JSON object
			 */
			public toJSON(): { [k: string]: any };

			/**
			 * Gets the default type url for ChartData
			 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
			 * @returns The default type url
			 */
			public static getTypeUrl(typeUrlPrefix?: string): string;
		}

		/** Properties of a ChartResponse. */
		interface IChartResponse {
			/** ChartResponse charts */
			charts?: greenova.mechanisms.IChartData[] | null;

			/** ChartResponse error */
			error?: string | null;
		}

		/** Represents a ChartResponse. */
		class ChartResponse implements IChartResponse {
			/**
			 * Constructs a new ChartResponse.
			 * @param [properties] Properties to set
			 */
			constructor(properties?: greenova.mechanisms.IChartResponse);

			/** ChartResponse charts. */
			public charts: greenova.mechanisms.IChartData[];

			/** ChartResponse error. */
			public error: string;

			/**
			 * Creates a new ChartResponse instance using the specified properties.
			 * @param [properties] Properties to set
			 * @returns ChartResponse instance
			 */
			public static create(
				properties?: greenova.mechanisms.IChartResponse,
			): greenova.mechanisms.ChartResponse;

			/**
			 * Encodes the specified ChartResponse message. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
			 * @param message ChartResponse message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encode(
				message: greenova.mechanisms.IChartResponse,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Encodes the specified ChartResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
			 * @param message ChartResponse message or plain object to encode
			 * @param [writer] Writer to encode to
			 * @returns Writer
			 */
			public static encodeDelimited(
				message: greenova.mechanisms.IChartResponse,
				writer?: $protobuf.Writer,
			): $protobuf.Writer;

			/**
			 * Decodes a ChartResponse message from the specified reader or buffer.
			 * @param reader Reader or buffer to decode from
			 * @param [length] Message length if known beforehand
			 * @returns ChartResponse
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decode(
				reader: $protobuf.Reader | Uint8Array,
				length?: number,
			): greenova.mechanisms.ChartResponse;

			/**
			 * Decodes a ChartResponse message from the specified reader or buffer, length delimited.
			 * @param reader Reader or buffer to decode from
			 * @returns ChartResponse
			 * @throws {Error} If the payload is not a reader or valid buffer
			 * @throws {$protobuf.util.ProtocolError} If required fields are missing
			 */
			public static decodeDelimited(
				reader: $protobuf.Reader | Uint8Array,
			): greenova.mechanisms.ChartResponse;

			/**
			 * Verifies a ChartResponse message.
			 * @param message Plain object to verify
			 * @returns `null` if valid, otherwise the reason why it is not
			 */
			public static verify(message: { [k: string]: any }): string | null;

			/**
			 * Creates a ChartResponse message from a plain object. Also converts values to their respective internal types.
			 * @param object Plain object
			 * @returns ChartResponse
			 */
			public static fromObject(object: {
				[k: string]: any;
			}): greenova.mechanisms.ChartResponse;

			/**
			 * Creates a plain object from a ChartResponse message. Also converts values to other types if specified.
			 * @param message ChartResponse
			 * @param [options] Conversion options
			 * @returns Plain object
			 */
			public static toObject(
				message: greenova.mechanisms.ChartResponse,
				options?: $protobuf.IConversionOptions,
			): { [k: string]: any };

			/**
			 * Converts this ChartResponse to JSON.
			 * @returns JSON object
			 */
			public toJSON(): { [k: string]: any };

			/**
			 * Gets the default type url for ChartResponse
			 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
			 * @returns The default type url
			 */
			public static getTypeUrl(typeUrlPrefix?: string): string;
		}
	}
}

/** Namespace feedback. */
export namespace feedback {
	/** Properties of a BugReportProto. */
	interface IBugReportProto {
		/** BugReportProto id */
		id?: number | null;

		/** BugReportProto title */
		title?: string | null;

		/** BugReportProto description */
		description?: string | null;

		/** BugReportProto applicationVersion */
		applicationVersion?: string | null;

		/** BugReportProto operatingSystem */
		operatingSystem?: string | null;

		/** BugReportProto browser */
		browser?: string | null;

		/** BugReportProto deviceType */
		deviceType?: string | null;

		/** BugReportProto stepsToReproduce */
		stepsToReproduce?: string | null;

		/** BugReportProto expectedBehavior */
		expectedBehavior?: string | null;

		/** BugReportProto actualBehavior */
		actualBehavior?: string | null;

		/** BugReportProto errorMessages */
		errorMessages?: string | null;

		/** BugReportProto traceReport */
		traceReport?: string | null;

		/** BugReportProto frequency */
		frequency?: feedback.BugReportProto.Frequency | null;

		/** BugReportProto impactSeverity */
		impactSeverity?: feedback.BugReportProto.Severity | null;

		/** BugReportProto adminSeverity */
		adminSeverity?: feedback.BugReportProto.Severity | null;

		/** BugReportProto userImpact */
		userImpact?: string | null;

		/** BugReportProto workarounds */
		workarounds?: string | null;

		/** BugReportProto additionalComments */
		additionalComments?: string | null;

		/** BugReportProto userId */
		userId?: number | null;

		/** BugReportProto username */
		username?: string | null;

		/** BugReportProto createdAt */
		createdAt?: number | Long | null;

		/** BugReportProto updatedAt */
		updatedAt?: number | Long | null;

		/** BugReportProto githubIssueUrl */
		githubIssueUrl?: string | null;

		/** BugReportProto status */
		status?: feedback.BugReportProto.Status | null;

		/** BugReportProto adminComment */
		adminComment?: string | null;
	}

	/** Represents a BugReportProto. */
	class BugReportProto implements IBugReportProto {
		/**
		 * Constructs a new BugReportProto.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: feedback.IBugReportProto);

		/** BugReportProto id. */
		public id: number;

		/** BugReportProto title. */
		public title: string;

		/** BugReportProto description. */
		public description: string;

		/** BugReportProto applicationVersion. */
		public applicationVersion: string;

		/** BugReportProto operatingSystem. */
		public operatingSystem: string;

		/** BugReportProto browser. */
		public browser: string;

		/** BugReportProto deviceType. */
		public deviceType: string;

		/** BugReportProto stepsToReproduce. */
		public stepsToReproduce: string;

		/** BugReportProto expectedBehavior. */
		public expectedBehavior: string;

		/** BugReportProto actualBehavior. */
		public actualBehavior: string;

		/** BugReportProto errorMessages. */
		public errorMessages: string;

		/** BugReportProto traceReport. */
		public traceReport: string;

		/** BugReportProto frequency. */
		public frequency: feedback.BugReportProto.Frequency;

		/** BugReportProto impactSeverity. */
		public impactSeverity: feedback.BugReportProto.Severity;

		/** BugReportProto adminSeverity. */
		public adminSeverity: feedback.BugReportProto.Severity;

		/** BugReportProto userImpact. */
		public userImpact: string;

		/** BugReportProto workarounds. */
		public workarounds: string;

		/** BugReportProto additionalComments. */
		public additionalComments: string;

		/** BugReportProto userId. */
		public userId: number;

		/** BugReportProto username. */
		public username: string;

		/** BugReportProto createdAt. */
		public createdAt: number | Long;

		/** BugReportProto updatedAt. */
		public updatedAt: number | Long;

		/** BugReportProto githubIssueUrl. */
		public githubIssueUrl: string;

		/** BugReportProto status. */
		public status: feedback.BugReportProto.Status;

		/** BugReportProto adminComment. */
		public adminComment: string;

		/**
		 * Creates a new BugReportProto instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns BugReportProto instance
		 */
		public static create(
			properties?: feedback.IBugReportProto,
		): feedback.BugReportProto;

		/**
		 * Encodes the specified BugReportProto message. Does not implicitly {@link feedback.BugReportProto.verify|verify} messages.
		 * @param message BugReportProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: feedback.IBugReportProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified BugReportProto message, length delimited. Does not implicitly {@link feedback.BugReportProto.verify|verify} messages.
		 * @param message BugReportProto message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: feedback.IBugReportProto,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a BugReportProto message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns BugReportProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): feedback.BugReportProto;

		/**
		 * Decodes a BugReportProto message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns BugReportProto
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): feedback.BugReportProto;

		/**
		 * Verifies a BugReportProto message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a BugReportProto message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns BugReportProto
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): feedback.BugReportProto;

		/**
		 * Creates a plain object from a BugReportProto message. Also converts values to other types if specified.
		 * @param message BugReportProto
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: feedback.BugReportProto,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this BugReportProto to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for BugReportProto
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	namespace BugReportProto {
		/** Frequency enum. */
		enum Frequency {
			FREQUENCY_UNKNOWN_UNSPECIFIED = 0,
			FREQUENCY_ALWAYS = 1,
			FREQUENCY_FREQUENTLY = 2,
			FREQUENCY_OCCASIONALLY = 3,
			FREQUENCY_RARELY = 4,
		}

		/** Severity enum. */
		enum Severity {
			SEVERITY_UNDEFINED_UNSPECIFIED = 0,
			SEVERITY_LOW = 1,
			SEVERITY_MEDIUM = 2,
			SEVERITY_HIGH = 3,
			SEVERITY_CRITICAL = 4,
		}

		/** Status enum. */
		enum Status {
			STATUS_UNSPECIFIED = 0,
			STATUS_OPEN = 1,
			STATUS_IN_PROGRESS = 2,
			STATUS_RESOLVED = 3,
			STATUS_CLOSED = 4,
			STATUS_REJECTED = 5,
		}
	}

	/** Properties of a BugReportCollection. */
	interface IBugReportCollection {
		/** BugReportCollection reports */
		reports?: feedback.IBugReportProto[] | null;
	}

	/** Represents a BugReportCollection. */
	class BugReportCollection implements IBugReportCollection {
		/**
		 * Constructs a new BugReportCollection.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: feedback.IBugReportCollection);

		/** BugReportCollection reports. */
		public reports: feedback.IBugReportProto[];

		/**
		 * Creates a new BugReportCollection instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns BugReportCollection instance
		 */
		public static create(
			properties?: feedback.IBugReportCollection,
		): feedback.BugReportCollection;

		/**
		 * Encodes the specified BugReportCollection message. Does not implicitly {@link feedback.BugReportCollection.verify|verify} messages.
		 * @param message BugReportCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: feedback.IBugReportCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified BugReportCollection message, length delimited. Does not implicitly {@link feedback.BugReportCollection.verify|verify} messages.
		 * @param message BugReportCollection message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: feedback.IBugReportCollection,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a BugReportCollection message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns BugReportCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): feedback.BugReportCollection;

		/**
		 * Decodes a BugReportCollection message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns BugReportCollection
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): feedback.BugReportCollection;

		/**
		 * Verifies a BugReportCollection message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a BugReportCollection message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns BugReportCollection
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): feedback.BugReportCollection;

		/**
		 * Creates a plain object from a BugReportCollection message. Also converts values to other types if specified.
		 * @param message BugReportCollection
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: feedback.BugReportCollection,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this BugReportCollection to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for BugReportCollection
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}

/** Namespace chatbot. */
export namespace chatbot {
	/** Properties of a ChatMessage. */
	interface IChatMessage {
		/** ChatMessage userId */
		userId?: string | null;

		/** ChatMessage content */
		content?: string | null;

		/** ChatMessage timestamp */
		timestamp?: number | Long | null;

		/** ChatMessage type */
		type?: chatbot.ChatMessage.MessageType | null;
	}

	/** Represents a ChatMessage. */
	class ChatMessage implements IChatMessage {
		/**
		 * Constructs a new ChatMessage.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: chatbot.IChatMessage);

		/** ChatMessage userId. */
		public userId: string;

		/** ChatMessage content. */
		public content: string;

		/** ChatMessage timestamp. */
		public timestamp: number | Long;

		/** ChatMessage type. */
		public type: chatbot.ChatMessage.MessageType;

		/**
		 * Creates a new ChatMessage instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ChatMessage instance
		 */
		public static create(
			properties?: chatbot.IChatMessage,
		): chatbot.ChatMessage;

		/**
		 * Encodes the specified ChatMessage message. Does not implicitly {@link chatbot.ChatMessage.verify|verify} messages.
		 * @param message ChatMessage message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: chatbot.IChatMessage,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ChatMessage message, length delimited. Does not implicitly {@link chatbot.ChatMessage.verify|verify} messages.
		 * @param message ChatMessage message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: chatbot.IChatMessage,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ChatMessage message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ChatMessage
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): chatbot.ChatMessage;

		/**
		 * Decodes a ChatMessage message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ChatMessage
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): chatbot.ChatMessage;

		/**
		 * Verifies a ChatMessage message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ChatMessage message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ChatMessage
		 */
		public static fromObject(object: { [k: string]: any }): chatbot.ChatMessage;

		/**
		 * Creates a plain object from a ChatMessage message. Also converts values to other types if specified.
		 * @param message ChatMessage
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: chatbot.ChatMessage,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ChatMessage to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ChatMessage
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}

	namespace ChatMessage {
		/** MessageType enum. */
		enum MessageType {
			MESSAGE_TYPE_TEXT_UNSPECIFIED = 0,
			MESSAGE_TYPE_IMAGE = 1,
			MESSAGE_TYPE_AUDIO = 2,
		}
	}

	/** Properties of a ChatResponse. */
	interface IChatResponse {
		/** ChatResponse messageId */
		messageId?: string | null;

		/** ChatResponse content */
		content?: string | null;

		/** ChatResponse timestamp */
		timestamp?: number | Long | null;
	}

	/** Represents a ChatResponse. */
	class ChatResponse implements IChatResponse {
		/**
		 * Constructs a new ChatResponse.
		 * @param [properties] Properties to set
		 */
		constructor(properties?: chatbot.IChatResponse);

		/** ChatResponse messageId. */
		public messageId: string;

		/** ChatResponse content. */
		public content: string;

		/** ChatResponse timestamp. */
		public timestamp: number | Long;

		/**
		 * Creates a new ChatResponse instance using the specified properties.
		 * @param [properties] Properties to set
		 * @returns ChatResponse instance
		 */
		public static create(
			properties?: chatbot.IChatResponse,
		): chatbot.ChatResponse;

		/**
		 * Encodes the specified ChatResponse message. Does not implicitly {@link chatbot.ChatResponse.verify|verify} messages.
		 * @param message ChatResponse message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encode(
			message: chatbot.IChatResponse,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Encodes the specified ChatResponse message, length delimited. Does not implicitly {@link chatbot.ChatResponse.verify|verify} messages.
		 * @param message ChatResponse message or plain object to encode
		 * @param [writer] Writer to encode to
		 * @returns Writer
		 */
		public static encodeDelimited(
			message: chatbot.IChatResponse,
			writer?: $protobuf.Writer,
		): $protobuf.Writer;

		/**
		 * Decodes a ChatResponse message from the specified reader or buffer.
		 * @param reader Reader or buffer to decode from
		 * @param [length] Message length if known beforehand
		 * @returns ChatResponse
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decode(
			reader: $protobuf.Reader | Uint8Array,
			length?: number,
		): chatbot.ChatResponse;

		/**
		 * Decodes a ChatResponse message from the specified reader or buffer, length delimited.
		 * @param reader Reader or buffer to decode from
		 * @returns ChatResponse
		 * @throws {Error} If the payload is not a reader or valid buffer
		 * @throws {$protobuf.util.ProtocolError} If required fields are missing
		 */
		public static decodeDelimited(
			reader: $protobuf.Reader | Uint8Array,
		): chatbot.ChatResponse;

		/**
		 * Verifies a ChatResponse message.
		 * @param message Plain object to verify
		 * @returns `null` if valid, otherwise the reason why it is not
		 */
		public static verify(message: { [k: string]: any }): string | null;

		/**
		 * Creates a ChatResponse message from a plain object. Also converts values to their respective internal types.
		 * @param object Plain object
		 * @returns ChatResponse
		 */
		public static fromObject(object: {
			[k: string]: any;
		}): chatbot.ChatResponse;

		/**
		 * Creates a plain object from a ChatResponse message. Also converts values to other types if specified.
		 * @param message ChatResponse
		 * @param [options] Conversion options
		 * @returns Plain object
		 */
		public static toObject(
			message: chatbot.ChatResponse,
			options?: $protobuf.IConversionOptions,
		): { [k: string]: any };

		/**
		 * Converts this ChatResponse to JSON.
		 * @returns JSON object
		 */
		public toJSON(): { [k: string]: any };

		/**
		 * Gets the default type url for ChatResponse
		 * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
		 * @returns The default type url
		 */
		public static getTypeUrl(typeUrlPrefix?: string): string;
	}
}
