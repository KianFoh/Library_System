from celery import shared_task


@shared_task
def reset_timeslots_status():
    from .models import Timeslot  # Import inside the function

    timeslots = Timeslot.objects.all()
    for timeslot in timeslots:
        timeslot.status = 'Empty'
        timeslot.save()
    print('Completed')

@shared_task
def reset_room_usage_hour():
    from user_data.models import User_data  # Import inside the function

    users = User_data.objects.all()
    for user in users:
        user.room_usage_hour = 0
        user.save()
    print('Completed')

from django.utils import timezone

@shared_task
def send_booking_reminder(booking_id, room_name, start_time, user_emails):
    from .models import Timeslot  # Import inside the function
    from django.contrib.auth.models import User
    from django.core.mail import EmailMessage

    # Prepare the email content
    subject = 'Reminder: Your Booking Timeslot is Approaching'

    for email in user_emails:
        user = User.objects.get(email=email)
        username = user.username

        # Format start_time to 12-hour format with AM/PM
        formatted_start_time = start_time.strftime("%I:%M %p")

        message = (
            f"Dear {username},\n\n"
            f"This is a reminder that your booked timeslot is approaching:\n"
            f"Booking ID: {booking_id}\n"
            f"Room Name: {room_name}\n"
            f"Booked Timeslot: {formatted_start_time}\n\n"
            f"Please be prepared to use the room and get the key to the room from the librarian.\n\n"
            f"Best regards,"
        )

        # Attempt to send the email
        email = EmailMessage(subject, message, to=[email])
        email.send()
        print('Completed')
