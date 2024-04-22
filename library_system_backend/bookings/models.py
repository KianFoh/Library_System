from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Timeslot(models.Model):
    TIMESLOT_STATUS_CHOICES = [
        ('Booked', _('Booked')),
        ('Empty', _('Empty')),
        ('Maintenance', _('Maintenance')),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=TIMESLOT_STATUS_CHOICES)

def __str__(self):
        return f"Timeslot for {self.room} from {self.start_time} to {self.end_time} ({self.status})"

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('Completed', _('Completed')),
        ('Pending', _('Pending')),
        ('Canceled', _('Canceled')),
    ]

    time_slot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES)

def __str__(self):
        return f"Booking for {self.time_slot.room} from {self.time_slot.start_time} to {self.time_slot.end_time} ({self.status})"