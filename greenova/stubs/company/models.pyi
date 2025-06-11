from _typeshed import Incomplete
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

logger: Incomplete

class Company(models.Model):
    logo: Incomplete
    description: Incomplete
    website: Incomplete
    phone: Incomplete
    email: Incomplete
    name: Incomplete
    address: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    users: Incomplete
    COMPANY_TYPES: Incomplete
    company_type: Incomplete
    COMPANY_SIZES: Incomplete
    size: Incomplete
    INDUSTRY_SECTORS: Incomplete
    industry: Incomplete
    is_active: Incomplete
    @staticmethod
    def get_default_company(): ...
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete
    def __str__(self) -> str: ...
    def get_member_count(self) -> int: ...
    def get_active_projects_count(self) -> int: ...
    def get_members_by_role(self, role: str) -> QuerySet: ...
    def add_member(self, user: User, role: str = 'member') -> None: ...
    def remove_member(self, user: User) -> None: ...
    def clean(self) -> None: ...

class CompanyMembership(models.Model):
    ROLE_CHOICES: Incomplete
    company: Incomplete
    user: Incomplete
    role: Incomplete
    department: Incomplete
    position: Incomplete
    date_joined: Incomplete
    is_primary: Incomplete
    class Meta:
        unique_together: Incomplete
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...
    def save(self, *args, **kwargs) -> None: ...
    def clean(self) -> None: ...

class CompanyDocument(models.Model):
    company: Incomplete
    name: Incomplete
    description: Incomplete
    file: Incomplete
    document_type: Incomplete
    uploaded_by: Incomplete
    uploaded_at: Incomplete
    class Meta:
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...

class Obligation(models.Model):
    company: Incomplete
    name: Incomplete
    description: Incomplete
    due_date: Incomplete
    status: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    class Meta:
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...
