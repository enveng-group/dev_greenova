from django.db import models
from responsibility.models import Responsibility

class Obligation(models.Model):
    # ...existing code...
    responsibility = models.ForeignKey(Responsibility, on_delete=models.SET_NULL, null=True)
    # ...existing code...
