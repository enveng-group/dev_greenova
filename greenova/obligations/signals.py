import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

from .models import Obligation

logger = logging.getLogger('greenova.obligations')

@receiver(post_save, sender=Obligation)
def obligation_saved_handler(sender, instance, created, **kwargs):
    """Handle obligation creation and updates by logging the event."""
    action = 'created' if created else 'updated'
    logger.info(f'Obligation {instance.obligation_number} {action}')

    # Clear related caches
    cache_keys = [
        'obligation_stats',
        f'obligation_details_{instance.obligation_number}',
        f'project_obligations_{instance.project_name}'
    ]
    cache.delete_many(cache_keys)

    # Create audit entry if audit app is installed
    if 'core' in settings.INSTALLED_APPS:
        from core.models import Audit

        Audit.objects.create(
            action='CREATE' if created else 'UPDATE',
            user=instance.created_by if created else instance.updated_by,
            details={
                'obligation_number': instance.obligation_number,
                'project_name': instance.project_name,
                'status': instance.status,
                'action': 'created' if created else 'updated'
            },
            timestamp=timezone.now()
        )

@receiver(pre_delete, sender=Obligation)
def obligation_delete_handler(sender, instance, **kwargs):
    """Handle obligation deletion by logging the event."""
    logger.info(f'Obligation deletion initiated: {instance.obligation_number}')

    # Clear related caches
    cache_keys = [
        'obligation_stats',
        f'obligation_details_{instance.obligation_number}',
        f'project_obligations_{instance.project_name}'
    ]
    cache.delete_many(cache_keys)

    # Create audit entry if audit app is installed
    if 'core' in settings.INSTALLED_APPS:
        from core.models import Audit

        Audit.objects.create(
            action='DELETE',
            user=instance.updated_by,
            details={
                'obligation_number': instance.obligation_number,
                'project_name': instance.project_name,
                'status': instance.status,
                'action': 'deleted'
            },
            timestamp=timezone.now()
        )

def connect_signals():
    """Explicitly connect signals."""
    logger.info('Connecting Obligation signals')
