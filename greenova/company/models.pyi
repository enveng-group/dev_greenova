# Stub file for company.models
from datetime import datetime
from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager, QuerySet

class Company(models.Model):
    name: str
    logo: str | None
    description: str
    website: str
    phone: str
    email: str
    address: str | None
    company_type: str
    size: str
    industry: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    users: Manager[User]

    COMPANY_TYPES: list[tuple[str, str]]
    COMPANY_SIZES: list[tuple[str, str]]
    INDUSTRY_SECTORS: list[tuple[str, str]]

    def __str__(self) -> str: ...
    def get_member_count(self) -> int: ...
    def get_active_projects_count(self) -> int: ...
    def get_members_by_role(self, role: str) -> QuerySet: ...
    def add_member(self, user: User, role: str = ...) -> None: ...
    def remove_member(self, user: User) -> None: ...
    def clean(self) -> None: ...
    @staticmethod
    def get_default_company() -> int: ...

class CompanyMembership(models.Model):
    company: Company
    user: User
    role: str
    department: str
    position: str
    date_joined: datetime
    is_primary: bool

    ROLE_CHOICES: list[tuple[str, str]]

    def __str__(self) -> str: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def clean(self) -> None: ...

class CompanyDocument(models.Model):
    company: Company
    name: str
    description: str
    file: str
    document_type: str
    uploaded_by: User | None
    uploaded_at: datetime

    def __str__(self) -> str: ...

class Obligation(models.Model):
    company: Company
    name: str
    description: str
    due_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
