from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from user_data.models import User_data
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from .tasks import send_booking_reminder
from celery import shared_task

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
        timeslots = self.time_slot.all().order_by('start_time')
        booking_users = self.bookinguser_set.all()
        user_emails = [booking_user.user.email for booking_user in booking_users]

        if self._all_booking_users_approved():
            if self._timeslots_validation(timeslots, request, user_emails, booking_user):
                return redirect('bookings')

            for booking_user in booking_users:
                if self._user_exceeds_booking_limit(booking_user, request, len(timeslots), user_emails):
                    return redirect('bookings')

            self._finalize_booking(timeslots, booking_users, request, user_emails)
        elif self._any_booking_user_rejected():
            self._cancel_booking(request, booking_user, user_emails)
        elif booking_user.status == 'Approved':
            message_content = mark_safe(f'Approved Booking ID: {self.id} request.')
            messages.success(request, message_content)

    def _all_booking_users_approved(self):
        return not self.bookinguser_set.exclude(status='Approved').exists()

    def _any_booking_user_rejected(self):
        return self.bookinguser_set.filter(status='Rejected').exists()

    def _timeslots_validation(self, timeslots, request, user_emails, booking_user):
        for timeslot in timeslots:
            current_time = datetime.now().time()
            if timeslot.status == 'Booked':
                self._notify_already_booked(request, timeslot, booking_user, user_emails)
                return True
            if current_time > timeslot.end_time.time():
                self._notify_passed_currenttime(request, timeslot, booking_user, user_emails)
                return True
        return False
    
    def _notify_passed_currenttime(self, request, timeslot, booking_user, user_emails):
        room_name = timeslot.room.name
        start_time = timeslot.start_time.strftime('%I:%M %p')
        end_time = timeslot.end_time.strftime('%I:%M %p')
        reason = f'the timeslot for {room_name} from {start_time} to {end_time} has already passed the current time.'
        self._reject_booking_user(request, booking_user, reason, user_emails)

    def _notify_already_booked(self, request, timeslot, booking_user, user_emails):
        room_name = timeslot.room.name
        start_time = timeslot.start_time.strftime('%I:%M %p')
        end_time = timeslot.end_time.strftime('%I:%M %p')
        reason = f'the timeslot for {room_name} from {start_time} to {end_time} has already been booked.'
        self._reject_booking_user(request, booking_user, reason, user_emails)

    def _user_exceeds_booking_limit(self, booking_user, request, num_timeslots, user_emails):
        user_data = User_data.objects.get(user=booking_user.user)
        total_usage = user_data.room_usage_hour + num_timeslots

        if total_usage > 2:
            remaining_hours = 2 - user_data.room_usage_hour
            reason = f'{booking_user.user.username} does not have enough daily booking hours to complete the booking request.'
            self._reject_booking_user(request, booking_user, reason, user_emails)
            return True
        return False

    def _reject_booking_user(self, request, booking_user, reason, user_emails):
        messages.warning(request, mark_safe(f'Booking ID: {self.id} has been canceled due to {reason}'))
        booking_user.status = 'Rejected'
        booking_user.save()
        self.status = 'Canceled'
        self.save()

        subject = f'Booking Canceled: Booking ID: {self.id}'
        message = (
            f'Booking Canceled for Booking ID: {self.id}\n\n'
            f'Dear Student,\n\n'
            f'The booking has been canceled due to:\n'
            f'{reason.capitalize()} \n\n'
            f'Thank you for your understanding.\n\n'
            f'Best regards,\n'
        )

        self.send_booking_email(request, subject, message, user_emails)

    def _finalize_booking(self, timeslots, booking_users, request, user_emails):
        for booking_user in booking_users:
            user_data = User_data.objects.get(user=booking_user.user)
            user_data.room_usage_hour += len(timeslots)
            user_data.save()
            room_name = timeslots[0].room.name

        timeslots.update(status='Booked')
        self.status = 'Completed'
        self.save()

        message_content = mark_safe(f'Booking ID: {self.id} has been successfully completed. ')
        messages.success(request, message_content)

        subject = f'Booking Completed: Booking ID: {self.id}'
        message = (
            f'Booking Completed for Booking ID: {self.id}\n\n'
            f'Dear Students,\n\n'
            f'The booking process has been completed.\n\n'
            f'Thank you for using INTI Penang Library Room Booking System.\n\n'
            f'Best regards,\n'
        )

        self.send_booking_email(request, subject, message, user_emails)

        # Variables to track heads of chains for timeslots
        chain_heads = []

        current_time = datetime.now().time()

        previous_end_time = None
        for timeslot in timeslots:
            if previous_end_time and timeslot.start_time.time() != previous_end_time:
                if current_time < timeslot.start_time.time():
                    chain_heads.append(timeslot)
            
            # Update previous_end_time
            previous_end_time = timeslot.end_time.time()

        # Add the head of the first chain if it exists
        if current_time < timeslots[0].start_time.time():
            chain_heads.insert(0, timeslots[0])

        for head in chain_heads:
            start_time = head.start_time.time()  # Extract time component
            
            # Calculate time difference
            time_difference_seconds = (datetime.combine(datetime.today(), start_time) - datetime.combine(datetime.today(), current_time)).total_seconds()

            # Calculate countdown time in seconds
            if time_difference_seconds <= 15 * 60:  # 15 minutes in seconds
                countdown_time = 1  # Send email ASAP
            else:
                countdown_time = time_difference_seconds - 15 * 60  # 15 minutes in seconds
            # Schedule the reminder email
            send_booking_reminder.apply_async(
                args=[self.id, room_name, start_time, user_emails],
                countdown=countdown_time
            )
            
    def _cancel_booking(self, request, booking_user, user_emails):
        username = request.user.username
        reason = f'{username} rejecting the request.'
        self._reject_booking_user(request, booking_user, reason, user_emails)
