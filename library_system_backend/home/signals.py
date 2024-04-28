from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Announcement
from handlers.signals import delete_file_on_post_delete

@receiver(post_delete, sender=Announcement)
def Announcement_deleted(sender, instance, **kwargs):
    delete_file_on_post_delete(sender, instance, 'image')

@receiver(pre_save, sender=Announcement)
def delete_previous_image(sender, instance, **kwargs):
    if instance.pk:  # If instance already exists (i.e., it's being updated)
        try:
            old_instance = Announcement.objects.get(pk=instance.pk)
            if old_instance.image != instance.image:  # If image has changed
                delete_file_on_post_delete(sender, old_instance, 'image')
        except Announcement.DoesNotExist:
            pass