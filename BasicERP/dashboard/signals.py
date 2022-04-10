import os
import environ
from django.db import models
from django.dispatch import receiver
from dashboard.models import Order, OrderImage, OrderDocument
from dashboard.notifications import email_order_groups
from django.contrib.auth.models import Group


@receiver(models.signals.post_delete, sender=OrderImage)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem when
    model instance is deleted.
    """
    if instance.image_location:
        if os.path.isfile(instance.image_location.path):
            os.remove(instance.image_location.path)


@receiver(models.signals.post_delete, sender=OrderDocument)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when
    model instance is deleted.
    """
    if instance.file_location:
        if os.path.isfile(instance.file_location.path):
            os.remove(instance.file_location.path)


@receiver(models.signals.m2m_changed, sender=Order.order_tags.through)
def order_group_changed(sender, instance, action, **kwargs):
    """
    Check if order group has changed and handle event
    """
    if action == "post_add":
        env = environ.Env()
        hostname = env("HOST_NAME")
        email_order_groups(instance, hostname)
