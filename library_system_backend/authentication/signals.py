from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_data.models import User_data  # Import your User_data model

@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwargs):
    """
    Signal handler to create a User_data object whenever a new User is created.
    """
    if created:
        User_data.objects.create(user=instance)