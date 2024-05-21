from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.utils.text import slugify

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Customize behavior before a social login occurs.
        """
        if sociallogin.is_existing:
            return
        
        user = sociallogin.user

        if user.email:
            try:
                existing_user = User.objects.get(email=user.email)
                if not existing_user.is_active:
                    # Activate the user account
                    existing_user.is_active = True
                    existing_user.save()

                # Connect the social account to the existing user
                sociallogin.connect(request, existing_user)

                # Check if the EmailAddress exists, create if not
                email = existing_user.email
                email_address = EmailAddress.objects.filter(email=email).first()
                if email_address is None:
                    email_address = EmailAddress.objects.create(user=existing_user, email=email, verified=True, primary=True)
            except User.DoesNotExist:
                pass
        
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # Use email without domain as username
        email = user.email
        username = email.split('@')[0]
        user.username = slugify(username)  # Convert username to slug
        # Do not set first name and last name
        user.first_name = ''
        user.last_name = ''
        return user