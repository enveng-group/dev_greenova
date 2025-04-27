import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

logger = logging.getLogger(__name__)


class Company(models.Model):
    """Model representing a company or organization."""
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    # Company type choices
    COMPANY_TYPES = [
        ('client', 'Client'),
        ('contractor', 'Contractor'),
        ('consultant', 'Consultant'),
        ('regulator', 'Regulator'),
        ('internal', 'Internal Department'),
        ('other', 'Other'),
    ]
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES, default='client')

    # Company size choices
    COMPANY_SIZES = [
        ('small', 'Small (1-49 employees)'),
        ('medium', 'Medium (50-249 employees)'),
        ('large', 'Large (250+ employees)'),
    ]
    size = models.CharField(max_length=10, choices=COMPANY_SIZES, blank=True)

    # Industry sector choices
    INDUSTRY_SECTORS = [
        ('manufacturing', 'Manufacturing'),
        ('construction', 'Construction'),
        ('mining', 'Mining'),
        ('energy', 'Energy'),
        ('transportation', 'Transportation'),
        ('government', 'Government'),
        ('consulting', 'Consulting'),
        ('other', 'Other'),
    ]
    industry = models.CharField(max_length=20, choices=INDUSTRY_SECTORS, blank=True)

    # Company status
    is_active = models.BooleanField(default=True)

    # Many-to-many relationship with users
    members = models.ManyToManyField(
        User,
        through='CompanyMembership',
        related_name='companies'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_default_company():
        """
        Return the ID of the default 'TBA' company.
        Used as default for foreign keys to ensure data integrity.
        """
        return 1

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_member_count(self) -> int:
        """Get count of company members."""
        return self.members.count()

    def get_active_projects_count(self) -> int:
        """Get count of active projects associated with this company."""
        from django.db import connection

        # Check if is_active field exists in projects_project table
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM pragma_table_info('projects_project')
                    WHERE name = 'is_active'
                    """
                )
                is_active_exists = cursor.fetchone()[0] > 0

            if is_active_exists:
                return self.projects.filter(is_active=True).count()
            else:
                # If is_active doesn't exist yet, count all projects
                return self.projects.count()
        except Exception as e:
            logger.error(f'Error counting active projects: {str(e)}')
            return 0

    def get_members_by_role(self, role: str) -> QuerySet:
        """Get all users with the specified role in this company."""
        return User.objects.filter(
            companymembership__company=self,
            companymembership__role=role
        )

    def add_member(self, user: User, role: str = 'member') -> None:
        """Add a user to the company with the specified role."""
        if not CompanyMembership.objects.filter(company=self, user=user).exists():
            CompanyMembership.objects.create(
                company=self,
                user=user,
                role=role
            )
            logger.info(f'Added user {user.username} to company {self.name} with role {role}')

    def remove_member(self, user: User) -> None:
        """Remove a user from the company."""
        CompanyMembership.objects.filter(company=self, user=user).delete()
        logger.info(f'Removed user {user.username} from company {self.name}')


class CompanyMembership(models.Model):
    """Through model for company memberships."""
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('member', 'Member'),
        ('client_contact', 'Client Contact'),
        ('contractor', 'Contractor'),
        ('view_only', 'View Only'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='company_memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_primary = models.BooleanField(
        default=False,
        help_text="Designates if this is the user's primary company."
    )

    class Meta:
        unique_together = ['user', 'company']
        ordering = ['company', 'user']
        verbose_name = 'Company Membership'
        verbose_name_plural = 'Company Memberships'

    def __str__(self) -> str:
        return f'{self.user.username} - {self.company.name} ({self.role})'

    def save(self, *args, **kwargs):
        """Override save to ensure only one company is primary."""
        if self.is_primary:
            # Set all other memberships for this user as not primary
            CompanyMembership.objects.filter(
                user=self.user,
                is_primary=True
            ).exclude(id=self.id if self.id else 0).update(is_primary=False)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate that a company can only have one owner."""
        if self.role == 'owner':
            existing_owner = CompanyMembership.objects.filter(
                company=self.company,
                role='owner'
            ).exclude(id=self.id if self.id else 0).exists()

            if existing_owner:
                raise ValidationError({'role': 'A company can only have one owner.'})


class CompanyDocument(models.Model):
    """Model for storing company documents."""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='company_documents/')
    document_type = models.CharField(max_length=100, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_company_documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Company Document'
        verbose_name_plural = 'Company Documents'

    def __str__(self) -> str:
        return f'{self.name} ({self.company.name})'
