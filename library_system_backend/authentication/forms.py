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

