from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import SignupForm, LoginForm  # Importing forms from local module
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token  # Importing custom token for account activation
from django.contrib.auth.models import User
from user_data.models import User_data  # Importing the user_data model from the user_data app

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
    mail_subject = "Activate your user account."
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

            # Create a corresponding user_data object
            User_data.objects.create(user=user)

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