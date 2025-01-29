from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from audit.models import AuditLog

class Obligation(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'), 
        ('completed', 'Completed'),
        ('overdue', 'Overdue')
    ]
    
    SITE_CHOICES = [
        ('site', 'Site'),
        ('desktop', 'Desktop')
    ]
    
    PROJECT_CHOICES = [
        ('Portside', 'Portside'),
        ('WA6946', 'WA6946'),
        ('MS1180', 'MS1180')
    ]

    # Primary Fields
    obligation_number = models.CharField(max_length=20, primary_key=True)
    project_name = models.CharField(max_length=255, choices=PROJECT_CHOICES)
    primary_environmental_mechanism = models.TextField(null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    environmental_aspect = models.TextField(null=True, blank=True)
    obligation = models.TextField()
    accountability = models.CharField(max_length=255)
    responsibility = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='obligations')
    project_phase = models.TextField(null=True, blank=True)
    action_due_date = models.DateField(null=True, blank=True)
    close_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_started')
    
    # Comments and Additional Info
    supporting_information = models.TextField(null=True, blank=True)
    general_comments = models.TextField(null=True, blank=True)
    compliance_comments = models.TextField(null=True, blank=True)
    non_conformance_comments = models.TextField(null=True, blank=True)
    evidence = models.TextField(null=True, blank=True)
    person_email = models.EmailField(null=True, blank=True)
    
    # Recurrence Fields
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=50, null=True, blank=True)
    recurring_status = models.CharField(max_length=50, null=True, blank=True)
    recurring_forcasted_date = models.DateField(null=True, blank=True)
    
    # Inspection Fields
    inspection = models.BooleanField(default=False)
    inspection_frequency = models.CharField(max_length=50, null=True, blank=True)
    site_or_desktop = models.CharField(max_length=50, choices=SITE_CHOICES, null=True, blank=True)
    
    # Control and Analysis
    new_control_action_required = models.BooleanField(default=False)
    obligation_type = models.CharField(max_length=50, null=True, blank=True)
    gap_analysis = models.TextField(null=True, blank=True)
    notes_for_gap_analysis = models.TextField(null=True, blank=True)
    covered_in_which_inspection_checklist = models.TextField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_obligations')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_obligations')

    class Meta:
        ordering = ['action_due_date', 'obligation_number']
        
    def __str__(self):
        return f"{self.obligation_number} - {self.project_name}"

    def save(self, *args, **kwargs):
        if self.action_due_date and self.status not in ['completed']:
            if self.action_due_date < timezone.now().date():
                self.status = 'overdue'
        super().save(*args, **kwargs)