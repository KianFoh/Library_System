from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from user_data.models import User_data
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.core.mail import EmailMessage

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

    def send_booking_email(self, request, subject, message, user_emails):
        try:
            email = EmailMessage(subject, message, to=user_emails)
            email.send()
        except Exception as e:
            message_content = f'Failed to send booking notification email to {", ".join(user_emails)}: {str(e)}'
            messages.warning(request, message_content)

    def update_status(self, request):
        current_user = request.user
        booking_user = self.bookinguser_set.filter(user=current_user).first()
        timeslots = self.time_slot.all()
        booking_users = self.bookinguser_set.all()
        user_emails = [booking_user.user.email for booking_user in booking_users]

        if self._all_booking_users_approved():
            if self._timeslots_already_booked(timeslots, request, user_emails, booking_user):
                return redirect('bookings')

            for booking_user in booking_users:
                if self._user_exceeds_booking_limit(booking_user, request, len(timeslots), user_emails):
                    return redirect('bookings')

            self._finalize_booking(timeslots, booking_users, request, user_emails)
        elif self._any_booking_user_rejected():
            self._cancel_booking(request, booking_user, user_emails)
        elif booking_user.status == 'Approved':
            message_content = mark_safe(f'Approved Booking ID {self.id} request.')
            messages.success(request, message_content)

    def _all_booking_users_approved(self):
        return not self.bookinguser_set.exclude(status='Approved').exists()

    def _any_booking_user_rejected(self):
        return self.bookinguser_set.filter(status='Rejected').exists()

    def _timeslots_already_booked(self, timeslots, request, user_emails, booking_user):
        for timeslot in timeslots:
            if timeslot.status == 'Booked':
                self._notify_already_booked(request, timeslot, booking_user, user_emails)
                return True
        return False

    def _notify_already_booked(self, request, timeslot, booking_user, user_emails):
        room_name = timeslot.room.name
        start_time = timeslot.start_time.strftime('%I:%M %p')
        end_time = timeslot.end_time.strftime('%I:%M %p')
        message_content = mark_safe(f'The timeslot {start_time} - {end_time} for {room_name} is already booked.')
        messages.warning(request, message_content)
        reason = f'The timeslot for Room: {room_name} from {start_time} to {end_time} has already been booked.'
        self._reject_booking_user(request, booking_user, reason, user_emails)

    def _user_exceeds_booking_limit(self, booking_user, request, num_timeslots, user_emails):
        user_data = User_data.objects.get(user=booking_user.user)
        total_usage = user_data.room_usage_hour + num_timeslots

        if total_usage > 2:
            remaining_hours = 2 - user_data.room_usage_hour
            reason = f'{booking_user.user.username} has only {remaining_hours} hours remaining. Maximum daily booking limit is 2 hours.'
            self._reject_booking_user(request, booking_user, reason, user_emails)
            return True
        return False

    def _reject_booking_user(self, request, booking_user, reason, user_emails):
        messages.warning(request, mark_safe(reason))
        booking_user.status = 'Rejected'
        booking_user.save()
        self.status = 'Canceled'
        self.save()

        subject = f'Booking Canceled: ID {self.id}'
        message = (
            f'Booking Canceled for Booking ID {self.id}\n\n'
            f'Dear Student,\n\n'
            f'The booking has been canceled due to:\n'
            f'{reason} \n\n'
            f'Thank you for your understanding.\n\n'
            f'Best regards,\n'
        )

        self.send_booking_email(request, subject, message, user_emails)

    def _finalize_booking(self, timeslots, booking_users, request, user_emails):
        for booking_user in booking_users:
            user_data = User_data.objects.get(user=booking_user.user)
            user_data.room_usage_hour += len(timeslots)
            user_data.save()

        timeslots.update(status='Booked')
        self.status = 'Completed'
        self.save()

        message_content = mark_safe(f'Booking ID {self.id} has been successfully completed. ')
        messages.success(request, message_content)

        subject = f'Booking Completed: ID {self.id}'
        message = (
            f'Booking Completed for Booking ID {self.id}\n\n'
            f'Dear Students,\n\n'
            f'The booking process has been completed.\n\n'
            f'Thank you for using INTI Penang Library Room Booking System.\n\n'
            f'Best regards,\n'
        )

        self.send_booking_email(request, subject, message, user_emails)
        

    def _cancel_booking(self, request, booking_user, user_emails):
        username = request.user.username
        reason = f'{username} has rejected the booking.'
        self._reject_booking_user(request, booking_user, reason, user_emails)
