from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    """Model representing a project in the system."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        
    def __str__(self):
        return self.name

    def get_active_obligations(self):
        """Returns obligations that are not completed."""
        return self.obligations.exclude(status='completed')

    def get_completed_obligations(self):
        """Returns completed obligations."""
        return self.obligations.filter(status='completed')

    def get_overdue_obligations(self):
        """Returns overdue obligations."""
        from django.utils import timezone
        return self.obligations.filter(
            action_due_date__lt=timezone.now().date(),
            status__in=['not started', 'in progress']
        )

class Obligation(models.Model):
    """Model representing an environmental obligation."""
    STATUS_CHOICES = [
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    
    SITE_DESKTOP_CHOICES = [
        ('Site', 'Site'),
        ('Desktop', 'Desktop')
    ]

    obligation_number = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='obligations')
    primary_environmental_mechanism = models.TextField()
    procedure = models.TextField(blank=True, null=True)
    environmental_aspect = models.TextField()
    obligation = models.TextField()
    accountability = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=255)
    project_phase = models.TextField(blank=True, null=True)
    action_due_date = models.DateField(null=True, blank=True)
    close_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not started')
    supporting_information = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    compliance_comments = models.TextField(blank=True, null=True)
    non_conformance_comments = models.TextField(blank=True, null=True)
    evidence = models.TextField(blank=True, null=True)
    person_email = models.EmailField(blank=True, null=True)
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=50, blank=True, null=True)
    recurring_status = models.CharField(max_length=50, blank=True, null=True)
    recurring_forcasted_date = models.DateField(null=True, blank=True)
    inspection = models.BooleanField(default=False)
    inspection_frequency = models.CharField(max_length=50, blank=True, null=True)
    site_or_desktop = models.CharField(
        max_length=50, 
        choices=SITE_DESKTOP_CHOICES,
        blank=True, 
        null=True
    )
    new_control_action_required = models.BooleanField(default=False)
    obligation_type = models.CharField(max_length=50, blank=True, null=True)
    gap_analysis = models.TextField(blank=True, null=True)
    notes_for_gap_analysis = models.TextField(blank=True, null=True)
    covered_in_which_inspection_checklist = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['obligation_number']
        verbose_name = 'Obligation'
        verbose_name_plural = 'Obligations'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['status']),
            models.Index(fields=['action_due_date']),
            models.Index(fields=['project_phase']),
        ]
        
    def __str__(self):
        return f"{self.obligation_number} - {self.project.name}"