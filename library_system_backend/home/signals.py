from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Announcement
from handlers.signals import delete_file_on_post_delete

@receiver(post_delete, sender=Announcement)
def Announcement_deleted(sender, instance, **kwargs):
    delete_file_on_post_delete(sender, instance, 'image')