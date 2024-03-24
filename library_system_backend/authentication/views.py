from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignupForm
from verify_email.email_handler import send_verification_email

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is not active until email is confirmed
            user.save()
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})
