from _typeshed import Incomplete
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from typing import TypeVar

logger: Incomplete
User: Incomplete
UserType = TypeVar('UserType', bound=models.Model)

class Project(models.Model):
    name: models.CharField
    description: models.TextField
    members: models.ManyToManyField
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete
    def __str__(self) -> str: ...
    def get_member_count(self) -> int: ...
    def get_user_role(self, user: AbstractUser) -> str: ...
    def has_member(self, user: AbstractUser) -> bool: ...
    def add_member(self, user: AbstractUser, role: str = ...) -> None: ...
    def remove_member(self, user: AbstractUser) -> None: ...
    def get_members_by_role(self, role: str) -> QuerySet[UserType]: ...
    @property
    def obligations(self): ...

class ProjectMembership(models.Model):
    user: models.ForeignKey
    project: models.ForeignKey
    role: models.CharField
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    class Meta:
        unique_together: Incomplete
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...

class ProjectObligation(models.Model):
    project: models.ForeignKey
    obligation: models.ForeignKey
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    class Meta:
        unique_together: Incomplete
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...
