from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already associated with an existing account.")
        return email
    
class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
            temp_user = None
            if user is None:
                try:
                    temp_user = User.objects.get(email=username_or_email)
                    user = authenticate(username=temp_user.username, password=password)

                except User.DoesNotExist:
                    pass
            if user is None:
                if temp_user is not None and not temp_user.is_active:
                    raise ValidationError("Your account is inactive. Please check your email inbox for a verification link to activate your account.")
                else:
                    raise ValidationError("Invalid username/email or password.")
        return cleaned_data