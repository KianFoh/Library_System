from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import SignupForm, LoginForm, ResetPasswordAuthenticate  # Importing forms from local module
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token  # Importing custom token for account activation
from django.contrib.auth.models import User
from .forms import CustomSetPasswordForm
from .token import account_activation_token, reset_password_token

def activate(request, uidb64, token):
    User = get_user_model()  # Get the user model
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the user ID
        user = User.objects.get(pk=uid)  # Get the user with the decoded ID
    except:
        user = None

    # Check if the user exists and if the activation token is valid
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # Activate the user
        user.save()

        # Display success message after activation
        messages.success(request, "Thank you for your email confirmation. Now you can login to your account.")
    else:
        messages.warning(request, "Activation failed. The activation link is either invalid or expired.")
    return redirect('/')


def activateEmail(request, user, to_email):
    # Compose the activation email
    mail_subject = "Activate your user account - INTI Penang College Library System"
    message = render_to_string("authentication/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    # Send the activation email
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        # Display success message if email is sent successfully
        message_content = mark_safe(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                        the activation link to complete the registration.')
        messages.success(request, message_content)
    else:
        # Display error message if email sending fails
        message.warning(request, f'Problem sending email to {to_email}, Please check if you typed it correctly.')


def signup_view(request):
    # Redirect to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until email is verified
            user.save()

            # Send activation email
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

            # Email
            if '@' in    username_or_email:
                try:
                    user = None
                    user_temp = User.objects.get(email=username_or_email)
                    print(user_temp.password)
                    print(password)
                    user = authenticate(request, username=user_temp.username, password=password)
                    if user_temp.check_password(password):
                        if not user_temp.is_active:
                            activateEmail(request, user_temp, user_temp.email)
                            form.add_error(None, "Your account is inactive. A new verification link has been sent to your email. Please check your inbox to activate your account.")
                    else:           
                        form.add_error(None, "Invalid username/email or password.")
                except User.DoesNotExist:   
                    form.add_error(None, "Invalid username/email or password.")


            # Username    
            else:
                user = authenticate(request, username=username_or_email, password=password)
                if user is None:
                    try:
                        print('hello')
                        user_temp = User.objects.get(username=username_or_email)
                        if user_temp.check_password(password):
                            if not user_temp.is_active:
                                activateEmail(request, user_temp, user_temp.email)
                                form.add_error(None, "Your account is inactive.")
                        else:
                            form.add_error(None, "Invalid username/email or password.")
                    except User.DoesNotExist:
                        form.add_error(None, "Invalid username/email or password.")

            # If user authentication is successful, log them in
            if user:
                login(request, user)
                message_content = f'Welcome to Vision Library, {user.username}!'
                messages.success(request, message_content)
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    # Log out the user and redirect to home page
    logout(request)
    return redirect('home')

def login_cancelled(request):
    return redirect('home')

def reset_password_email(request, user, to_email):
    # Compose the reset password email
    mail_subject = "Reset Your Password - INTI Penang College Library System"
    message = render_to_string("authentication/reset_password_email.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': reset_password_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    # Send the reset password email
    email = EmailMessage(mail_subject, message, to=[to_email])
    try:
        email.send()
        # Display success message if email is sent successfully
        message_content = mark_safe(f'A password reset email has been sent to <b>{to_email}</b>. \
                        Please check your email and follow the instructions to reset your password.')
        messages.success(request, message_content)
    except:
        # Display error message if email sending fails
        message_content = mark_safe(f'Problem sending email to <b>{to_email}</b>. \
                        Please check if you typed it correctly.')
        messages.error(request, message_content)

def reset_password_authenticate(request):
    if request.user.is_authenticated:
     return redirect('home')
    if request.method == 'POST':
        form = ResetPasswordAuthenticate(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email = email).first()
            if user:
                reset_password_email(request, user, user.email)
            else:
                form.add_error(None, "Invalid Email")
    else:
        form = ResetPasswordAuthenticate()
    return render(request, 'authentication/reset_password_authenticate.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and reset_password_token.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset.')
                return redirect('login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'authentication/reset_password.html', {'form': form})
    else:
        messages.warning(request, 'The password reset link is invalid or expired.')
        return redirect('/resetpassword/authentication')