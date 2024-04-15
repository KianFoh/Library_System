from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import SignupForm, LoginForm
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.auth.models import User


def activate(request,uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
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
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/login')
    else:
        form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username_or_email, password=password)

            if user is None:
                try:
                    user = User.objects.get(email=username_or_email)
                    user = authenticate(username=user.username, password=password)
                except User.DoesNotExist:
                    pass
            if user:
                login(request, user)
                message_content = f'Welcome to Vision Library, {user.username}!'
                messages.success(request, message_content)
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')