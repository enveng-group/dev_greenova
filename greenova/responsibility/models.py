from django.db import models
from django.contrib.auth.models import User
from company.models import Company, CompanyMembership


class ResponsibilityRole(models.Model):
    """
    Model representing a responsibility role that can be assigned to users
    for specific obligations.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='responsibility_roles'
    )
    company_role = models.CharField(
        max_length=20,
        choices=CompanyMembership.ROLE_CHOICES,
        null=True,
        blank=True,
        help_text="Corresponding company role, if any"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'company']
        ordering = ['company', 'name']
        verbose_name = 'Responsibility Role'
        verbose_name_plural = 'Responsibility Roles'

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class ResponsibilityAssignment(models.Model):
    """
    Model representing an assignment of responsibility for an obligation
    to a user with a specific role.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='responsibility_assignments'
    )
    obligation = models.ForeignKey(
        'obligations.Obligation',
        on_delete=models.CASCADE,
        related_name='responsibility_assignments'
    )
    role = models.ForeignKey(
        ResponsibilityRole,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignments'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'obligation', 'role']
        ordering = ['-created_at']
        verbose_name = 'Responsibility Assignment'
        verbose_name_plural = 'Responsibility Assignments'

    def __str__(self):
        role_name = self.role.name if self.role else "Unknown role"
        return f"{self.user.username} - {self.obligation.obligation_number} - {role_name}"
