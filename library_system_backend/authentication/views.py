from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm
from django.utils.safestring import mark_safe


def activateEmail(request, user, to_email):
    message_content = mark_safe(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                     the activation link to complete the registration.')
    messages.success(request, message_content)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})
