import * as $protobuf from "protobufjs";
import Long = require("long");
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
            STATUS_OVERDUE = 4
        }

        /** Properties of an ObligationInsight. */
        interface IObligationInsight {

            /** ObligationInsight obligationNumber */
            obligationNumber?: (string|null);

            /** ObligationInsight dueDate */
            dueDate?: (string|null);

            /** ObligationInsight closeOutDate */
            closeOutDate?: (string|null);
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
            public static create(properties?: greenova.mechanisms.IObligationInsight): greenova.mechanisms.ObligationInsight;

            /**
             * Encodes the specified ObligationInsight message. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
             * @param message ObligationInsight message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: greenova.mechanisms.IObligationInsight, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ObligationInsight message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsight.verify|verify} messages.
             * @param message ObligationInsight message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: greenova.mechanisms.IObligationInsight, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes an ObligationInsight message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ObligationInsight
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): greenova.mechanisms.ObligationInsight;

            /**
             * Decodes an ObligationInsight message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ObligationInsight
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): greenova.mechanisms.ObligationInsight;

            /**
             * Verifies an ObligationInsight message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates an ObligationInsight message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ObligationInsight
             */
            public static fromObject(object: { [k: string]: any }): greenova.mechanisms.ObligationInsight;

            /**
             * Creates a plain object from an ObligationInsight message. Also converts values to other types if specified.
             * @param message ObligationInsight
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: greenova.mechanisms.ObligationInsight, options?: $protobuf.IConversionOptions): { [k: string]: any };

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
            mechanismId?: (number|null);

            /** ObligationInsightResponse status */
            status?: (string|null);

            /** ObligationInsightResponse statusKey */
            statusKey?: (string|null);

            /** ObligationInsightResponse count */
            count?: (number|null);

            /** ObligationInsightResponse totalCount */
            totalCount?: (number|null);

            /** ObligationInsightResponse obligations */
            obligations?: (greenova.mechanisms.IObligationInsight[]|null);

            /** ObligationInsightResponse error */
            error?: (string|null);
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
            public static create(properties?: greenova.mechanisms.IObligationInsightResponse): greenova.mechanisms.ObligationInsightResponse;

            /**
             * Encodes the specified ObligationInsightResponse message. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
             * @param message ObligationInsightResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: greenova.mechanisms.IObligationInsightResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ObligationInsightResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ObligationInsightResponse.verify|verify} messages.
             * @param message ObligationInsightResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: greenova.mechanisms.IObligationInsightResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes an ObligationInsightResponse message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ObligationInsightResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): greenova.mechanisms.ObligationInsightResponse;

            /**
             * Decodes an ObligationInsightResponse message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ObligationInsightResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): greenova.mechanisms.ObligationInsightResponse;

            /**
             * Verifies an ObligationInsightResponse message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates an ObligationInsightResponse message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ObligationInsightResponse
             */
            public static fromObject(object: { [k: string]: any }): greenova.mechanisms.ObligationInsightResponse;

            /**
             * Creates a plain object from an ObligationInsightResponse message. Also converts values to other types if specified.
             * @param message ObligationInsightResponse
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: greenova.mechanisms.ObligationInsightResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

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
            label?: (string|null);

            /** ChartSegment value */
            value?: (number|null);

            /** ChartSegment color */
            color?: (string|null);
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
            public static create(properties?: greenova.mechanisms.IChartSegment): greenova.mechanisms.ChartSegment;

            /**
             * Encodes the specified ChartSegment message. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
             * @param message ChartSegment message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: greenova.mechanisms.IChartSegment, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ChartSegment message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartSegment.verify|verify} messages.
             * @param message ChartSegment message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: greenova.mechanisms.IChartSegment, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a ChartSegment message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ChartSegment
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): greenova.mechanisms.ChartSegment;

            /**
             * Decodes a ChartSegment message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ChartSegment
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): greenova.mechanisms.ChartSegment;

            /**
             * Verifies a ChartSegment message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a ChartSegment message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ChartSegment
             */
            public static fromObject(object: { [k: string]: any }): greenova.mechanisms.ChartSegment;

            /**
             * Creates a plain object from a ChartSegment message. Also converts values to other types if specified.
             * @param message ChartSegment
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: greenova.mechanisms.ChartSegment, options?: $protobuf.IConversionOptions): { [k: string]: any };

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
            segments?: (greenova.mechanisms.IChartSegment[]|null);

            /** ChartData mechanismId */
            mechanismId?: (number|null);

            /** ChartData mechanismName */
            mechanismName?: (string|null);
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
            public static create(properties?: greenova.mechanisms.IChartData): greenova.mechanisms.ChartData;

            /**
             * Encodes the specified ChartData message. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
             * @param message ChartData message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: greenova.mechanisms.IChartData, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ChartData message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartData.verify|verify} messages.
             * @param message ChartData message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: greenova.mechanisms.IChartData, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a ChartData message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ChartData
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): greenova.mechanisms.ChartData;

            /**
             * Decodes a ChartData message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ChartData
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): greenova.mechanisms.ChartData;

            /**
             * Verifies a ChartData message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a ChartData message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ChartData
             */
            public static fromObject(object: { [k: string]: any }): greenova.mechanisms.ChartData;

            /**
             * Creates a plain object from a ChartData message. Also converts values to other types if specified.
             * @param message ChartData
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: greenova.mechanisms.ChartData, options?: $protobuf.IConversionOptions): { [k: string]: any };

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
            charts?: (greenova.mechanisms.IChartData[]|null);

            /** ChartResponse error */
            error?: (string|null);
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
            public static create(properties?: greenova.mechanisms.IChartResponse): greenova.mechanisms.ChartResponse;

            /**
             * Encodes the specified ChartResponse message. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
             * @param message ChartResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: greenova.mechanisms.IChartResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ChartResponse message, length delimited. Does not implicitly {@link greenova.mechanisms.ChartResponse.verify|verify} messages.
             * @param message ChartResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: greenova.mechanisms.IChartResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a ChartResponse message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ChartResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): greenova.mechanisms.ChartResponse;

            /**
             * Decodes a ChartResponse message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ChartResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): greenova.mechanisms.ChartResponse;

            /**
             * Verifies a ChartResponse message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a ChartResponse message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ChartResponse
             */
            public static fromObject(object: { [k: string]: any }): greenova.mechanisms.ChartResponse;

            /**
             * Creates a plain object from a ChartResponse message. Also converts values to other types if specified.
             * @param message ChartResponse
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: greenova.mechanisms.ChartResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

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
