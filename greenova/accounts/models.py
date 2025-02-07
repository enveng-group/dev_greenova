from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Extended User model to include project-specific fields"""

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserProfile(models.Model):
    """Extended profile for users with project-specific fields"""

    user = models.OneToOneField(
        'accounts.User',  # Change this to use string reference
        on_delete=models.CASCADE,
        related_name='profile',
    )
    project_name = models.CharField(max_length=255, blank=True)
    primary_environmental_mechanism = models.TextField(blank=True)
    responsibility = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def email(self):
        """Return user's email from base User model"""
        return self.user.email


class ProjectRole(models.Model):
    """Project-specific roles that extend Django's Group model"""

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    environmental_mechanism = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Project Role'
        verbose_name_plural = 'Project Roles'
        unique_together = ['group', 'project_name']

    def __str__(self):
        return f"{self.group.name} - {self.project_name}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when User is created/updated"""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
