from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from clinic.models import Appointment, SiteBlock
from clinic.services.notifications import notify_new_appointment


@receiver(post_save, sender=Appointment)
def appointment_created(sender, instance, created, **kwargs):
    if created:
        notify_new_appointment(instance)


@receiver(post_save, sender=SiteBlock)
@receiver(post_delete, sender=SiteBlock)
def invalidate_site_blocks_cache(sender, **kwargs):
    cache.delete(settings.SITE_BLOCKS_CACHE_KEY)
