from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_data.models import User_data
from authentication.views import reset_password_email, reset_password_authenticate


def profile_redirect(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect('profile', username=username)
    else:
        messages.warning(request, mark_safe('Please login before accessing the Profile page'))
        return redirect('login')

@login_required
def profile_(request, username):
    if request.user.username != username:
        messages.warning(request, "You cannot access other users' profiles.")
        return redirect('profile', username=request.user.username)
    
    user = get_object_or_404(User, username=username)
    user_data = get_object_or_404(User_data, user=user)
    booking_hours_left = 2 - user_data.room_usage_hour
    context = {'user': user, 'user_data': user_data, 'booking_hours_left': booking_hours_left}
    return render(request, 'profile_/profile_.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        if not username:
            messages.warning(request, "Username cannot be empty. Please enter a valid username.")
            return redirect('profile', username=request.user.username)
        
        if username == request.user.username:
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile', username=request.user.username)
        
        if User.objects.filter(username=username).exists():
            messages.warning(request, f"{username} has already been taken. Please enter another username.")
            return redirect('profile', username=request.user.username)
        
        request.user.username = username
        request.user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile', username=request.user.username)

    return redirect('profile', username=request.user.username)

@login_required
def request_password_change(request):
    if request.method == 'POST':
        user = request.user

        reset_password_email(request, user, user.email)
        return reset_password_authenticate(request)

    return redirect('profile', username=request.user.username)