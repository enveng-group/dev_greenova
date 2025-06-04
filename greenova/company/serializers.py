# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the company app."""

from django.core.exceptions import ValidationError

from .models import Company

try:
    from .proto_utils import (
        deserialize_companies,
        deserialize_company,
        serialize_companies,
        serialize_company,
    )
except ImportError:

    def serialize_company(obj) -> bytes:
        return b""

    def deserialize_company(data) -> None:
        return None

    def serialize_companies(objs) -> bytes:
        return b""

    def deserialize_companies(data):
        return []


class CompanyProtoSerializer:
    """Serializer for Company using protobuf3 binary format."""

    def __init__(
        self,
        instance: Company | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: Company | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        company = deserialize_company(self.initial_data)
        if company is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = company
        return True

    def save(self) -> Company:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_company(self.instance)


class CompanyCollectionProtoSerializer:
    """Serializer for a collection of Company instances using protobuf3."""

    def __init__(
        self,
        instances: list[Company] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[Company] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        companies = deserialize_companies(self.initial_data)
        if not companies:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = companies
        return True

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_companies(self.instances)
