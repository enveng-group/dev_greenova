# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the company app."""

import logging

from beartype import beartype

from .models import Company

logger = logging.getLogger(__name__)

try:
    from .proto import company_pb2
except ImportError:
    company_pb2 = None
    logger.warning("company_pb2 not found. Ensure .proto files are compiled.")

    class CompanyProto:
        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    class CompanyCollection:
        companies = []

        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

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
    try:
        proto = company.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize company: %s", str(e))
        return None


@beartype
def deserialize_company(data: bytes) -> Company | None:
    try:
        proto = company_pb2.CompanyProto()
        proto.ParseFromString(data)
        return Company().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize company: %s", str(e))
        return None


@beartype
def serialize_companies(companies: list[Company]) -> bytes | None:
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
    try:
        collection = company_pb2.CompanyCollection()
        collection.ParseFromString(data)
        companies = []
        for proto in getattr(collection, "companies", []):
            company = Company().from_pb(proto)  # type: ignore[attr-defined]
            if company:
                companies.append(company)
        return companies
    except Exception as e:
        logger.exception("Failed to deserialize companies collection: %s", str(e))
        return []
