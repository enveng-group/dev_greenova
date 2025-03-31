<<<<<<< HEAD
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals  # Ensure the signal is connected
=======
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Create or update the user's profile when a user is saved."""
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
