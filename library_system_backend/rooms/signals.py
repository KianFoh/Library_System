from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Room
from bookings.models import Timeslot
from handlers.signals import delete_file_on_post_delete
from datetime import datetime, timedelta

@receiver(post_delete, sender=Room)
def room_deleted(sender, instance, **kwargs):
    delete_file_on_post_delete(sender, instance, 'image')

@receiver(post_save, sender=Room)
def room_add_timeslot(sender, instance, created, **kwargs):
    if created:
        # Get room id
        room_id = instance.id
        
    # Get today's date
    today_date = datetime.now().date()

    # Set start and end time with today's date
    start_time = datetime(year=today_date.year, month=today_date.month, day=today_date.day, hour=8, minute=0)
    end_time = datetime(year=today_date.year, month=today_date.month, day=today_date.day, hour=9, minute=0)

    # Number of time slots to create
    num_slots = 10

    # Loop to create time slots
    for _ in range(num_slots):
        # Create a time slot
        Timeslot.objects.create(room_id=room_id, start_time=start_time, end_time=end_time)
        
        # Increment start and end time by 1 hour
        start_time += timedelta(hours=1)
        end_time += timedelta(hours=1)
        
@receiver(pre_save, sender=Room)
def delete_previous_image(sender, instance, **kwargs):
    if instance.pk:  # If instance already exists (i.e., it's being updated)
        try:
            old_instance = Room.objects.get(pk=instance.pk)
            if old_instance.image != instance.image:  # If image has changed
                delete_file_on_post_delete(sender, old_instance, 'image')
        except Room.DoesNotExist:
            pass