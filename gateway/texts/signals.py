from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Text


@receiver(pre_save, sender=Text)
def pre_save_handler(sender, instance, **kwargs):
    """ Signal receiver for calling full_clean method before saving a Text model """

    instance.full_clean()
