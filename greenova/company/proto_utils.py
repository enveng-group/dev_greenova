# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the company app.

This module provides serialization and deserialization helpers for converting
between Django Company models and Protocol Buffer messages in the company app.

Features:
    - Safe import and fallback stubs for protobufs
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serialization/deserialization helpers for Company and CompanyCollection

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any

from beartype import beartype

from .models import Company

logger = logging.getLogger(__name__)

try:
    from .proto import company_pb2
except ImportError:
    company_pb2 = None
    logger.warning("company_pb2 not found. Ensure .proto files are compiled.")

    class CompanyProto:
        """Stub CompanyProto for missing protobufs."""

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy company proto to bytes.

            Returns:
                Empty bytes object.

            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy company proto from bytes.

            Args:
                data: Bytes to parse (ignored).

            """

    class CompanyCollection:
        """Stub CompanyCollection for missing protobufs."""

        companies: list[Any] = []

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy company collection to bytes.

            Returns:
                Empty bytes object.

            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy company collection from bytes.

            Args:
                data: Bytes to parse (ignored).

            """

    company_pb2 = type(
        "company_pb2",
        (),
        {
            "CompanyProto": CompanyProto,
            "CompanyCollection": CompanyCollection,
        },
    )


@beartype
def serialize_company(company: Company) -> bytes | None:
    """Serialize a Company instance to a Protocol Buffer message.

    Args:
        company: The Company instance to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.

    """
    try:
        proto = company.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize company: %s", str(e))
        return None


@beartype
def deserialize_company(data: bytes) -> Company | None:
    """Deserialize Protocol Buffer data to a Company instance.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        Company instance, or None if deserialization failed.

    Raises:
        Exception: For any deserialization error.

    """
    try:
        proto = company_pb2.CompanyProto()
        proto.ParseFromString(data)
        return Company().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize company: %s", str(e))
        return None


@beartype
def serialize_companies(companies: list[Company]) -> bytes | None:
    """Serialize a list of Company instances to a Protocol Buffer collection.

    Args:
        companies: List of Company instances to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.

    """
    try:
        collection = company_pb2.CompanyCollection()
        for company in companies:
            proto = company.to_pb()  # type: ignore[attr-defined]
            collection.companies.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize companies collection: %s", str(e))
        return None


@beartype
def deserialize_companies(data: bytes) -> list[Company]:
    """Deserialize Protocol Buffer data to a list of Company instances.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        List of Company instances, or empty list if deserialization failed.

    Raises:
        Exception: For any deserialization error.

    """
    try:
        collection = company_pb2.CompanyCollection()
        collection.ParseFromString(data)
        companies: list[Company] = []
        for proto in getattr(collection, "companies", []):
            company = Company().from_pb(proto)  # type: ignore[attr-defined]
            if company:
                companies.append(company)
        return companies
    except Exception as e:
        logger.exception("Failed to deserialize companies collection: %s", str(e))
        return []
