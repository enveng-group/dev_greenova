from _typeshed import Incomplete
from django.db import models

class Profile(models.Model):
    user: models.OneToOneField
    bio: models.TextField
    position: models.CharField
    department: models.CharField
    phone_number: models.CharField
    profile_image: Incomplete
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    def __str__(self) -> str: ...
