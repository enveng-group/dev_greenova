from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DashboardPreference(models.Model):
    """Store user-specific dashboard preferences."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dashboard_preferences',
    )
    show_completed = models.BooleanField(default=True)
    chart_type = models.CharField(
        max_length=10,
        choices=[('bar', 'Bar'), ('line', 'Line'), ('pie', 'Pie')],
        default='bar',
    )
    refresh_interval = models.PositiveIntegerField(
        default=30,
        validators=[
            MinValueValidator(
                10, message="Refresh interval must be at least 10 seconds"
            ),
            MaxValueValidator(
                300, message="Refresh interval cannot exceed 300 seconds"
            ),
        ],
    )

    class Meta:
        verbose_name = 'Dashboard Preference'
        verbose_name_plural = 'Dashboard Preferences'

    def __str__(self):
        return f"{self.user.username}'s Dashboard Preferences"
