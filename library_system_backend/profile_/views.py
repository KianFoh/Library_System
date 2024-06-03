from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

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
    context = {'user': user}
    return render(request, 'profile_/profile_.html', context)
