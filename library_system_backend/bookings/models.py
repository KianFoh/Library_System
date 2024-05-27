from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class Timeslot(models.Model):
    TIMESLOT_STATUS_CHOICES = [
        ('Booked', _('Booked')),
        ('Empty', _('Empty')),
        ('Maintenance', _('Maintenance')),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    status = models.CharField(max_length=20, choices=TIMESLOT_STATUS_CHOICES, default='Empty', null=False)
    
def __str__(self):
        return f"Timeslot for {self.room} from {self.start_time} to {self.end_time} ({self.status})"

class BookingUser(models.Model):
    USER_STATUS_CHOICES = [
        ('Pending', _('Pending')),
        ('Approved', _('Approved')),
        ('Rejected', _('Rejected')),
    ]

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('booking', 'user')

    def __str__(self):
        return f"{self.user.username}: {self.status}"

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('Completed', _('Completed')),
        ('Pending', _('Pending')),
        ('Canceled', _('Canceled')),
    ]

    time_slot = models.ManyToManyField(Timeslot)
    date_time = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking for {self.get_time_slots()} ({self.status})"

    def get_time_slots(self):
        return ", ".join([str(ts) for ts in self.time_slot.all()])

    def update_status(self):
        if all(booking_user.status == 'Approved' for booking_user in self.bookinguser_set.all()):
            self.status = 'Completed'
            self.save()