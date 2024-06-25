from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .models import Contact

@receiver(post_save, sender=Contact)
def send_email_on_contact_creation(sender, instance, created, **kwargs):
    if created:
        # Access fields from the instance
        title = instance.title
        message = instance.message

        sender_id = instance.user.id
        sender_name = instance.user.username
        sender_email = instance.user.email

        # Construct email subject and body
        mail_subject = f'New Enquiry: {title}'
        mail_body = f'Message: {message}\n\nSender ID: {sender_id}\nSender Name: {sender_name}\nSender Email: {sender_email}'

        # Get all superusers
        superusers = User.objects.filter(is_staff=True)

        # Send email to each superuser
        for superuser in superusers:
            superuser_email = superuser.email
            # Create and send the email
            email = EmailMessage(mail_subject, mail_body, to=[superuser_email])
            email.send()