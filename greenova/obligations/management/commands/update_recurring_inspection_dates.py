"""Management command to update all recurring forecasted inspection dates."""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django management command to update recurring forecasted inspection dates."""
    help = "Update all recurring forecasted dates"
