from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class SignupForm(UserCreationForm):
    # Define a form for user signup with email field required
    email = forms.EmailField(required=True)

    class Meta:
        # Associate the form with the User model and specify the fields
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        # Remove help text for certain fields
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        # Clean the email field and check if it's unique
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already associated with an existing account.")
        return email
    
class LoginForm(forms.Form):
    # Define a form for user login with username or email and password
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')
        if username_or_email and password:
            # Check if username_or_email exists as a username in auth_user
            user = User.objects.filter(username=username_or_email).first()
            
            if user is None:
                # Check if username_or_email exists as an email in the email column
                user = User.objects.filter(email=username_or_email).first()
                if user is not None:
                    username_or_email = user.username
            else:
                # If user exists as a username, authenticate using username
                username_or_email = user.username

            # Check if user is found and is active
            if user is not None and not user.is_active:
                raise ValidationError("Your account is inactive. Please check your email inbox for a verification link to activate your account.")

            # Authenticate the user
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                raise ValidationError("Invalid username/email or password.")

        return cleaned_data