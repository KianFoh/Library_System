from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_bytes
from django.core.mail import EmailMessage
from .token import account_activation_token


def activate(request,uidb64,token):
    return redirect('/')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("authentication/template_activate_account.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        message_content = mark_safe(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                        the activation link to complete the registration.')
        messages.success(request, message_content)
    else:
        message.error(request, f'Problem sending email to {to_email}, Please check if you typed it correctly.')

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
