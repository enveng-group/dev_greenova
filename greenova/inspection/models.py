from django.db import models
from obligations.models import Obligation
from datetime import date, timedelta

class RecurringFrequency(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    frequency_type = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    interval = models.PositiveIntegerField(help_text="Repeat every n units (e.g., every 2 weeks)")

    def __str__(self):
        return f"{self.interval} × {self.get_frequency_type_display()}"

class Inspection(models.Model):
    obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE, related_name="inspections")
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('overdue', 'Overdue'),
        ],
        default='scheduled'
    )
    notes = models.TextField(blank=True)
    frequency = models.ForeignKey(RecurringFrequency, on_delete=models.SET_NULL, null=True, blank=True)
    
    next_inspection_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Inspection on {self.date} for {self.obligation}"

    def calculate_next_date(self):
        if not self.frequency:
            return None

        base_date = self.date or date.today()
        if self.frequency.frequency_type == 'daily':
            delta = timedelta(days=self.frequency.interval)
        elif self.frequency.frequency_type == 'weekly':
            delta = timedelta(weeks=self.frequency.interval)
        elif self.frequency.frequency_type == 'monthly':
            delta = timedelta(days=30 * self.frequency.interval)  
        else:
            return None

        return base_date + delta

    def save(self, *args, **kwargs):
        self.next_inspection_date = self.calculate_next_date()
        super().save(*args, **kwargs)
