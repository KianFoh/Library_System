from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignupForm
from django.core.mail import send_mail
from django.conf import settings

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is not active until email is confirmed
            user.save()

            # Send confirmation email
            subject = 'Confirm Your Email'
            message = 'Please click the link below to confirm your email address.\n\n'
            message += f'{settings.BASE_URL}/confirm-email/{user.id}/'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            return redirect('email_confirmation_sent')  # Redirect to email confirmation sent page
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})

def email_confirmation_sent(request):
    return render(request, 'authentication/email_confirmation_sent.html')