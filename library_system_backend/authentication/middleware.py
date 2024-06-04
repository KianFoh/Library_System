from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy

class RestrictAllauthAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('account_login'):
            return redirect(reverse('login'))  # Redirect to custom login page
        elif request.path == reverse('account_signup'):
            return redirect(reverse('signup'))  # Redirect to custom signup page
        response = self.get_response(request)
        if request.path == '/accounts/google/login/callback/' and request.GET.get('error') == 'access_denied':
            return redirect(reverse_lazy('home'))  # Redirect to the home page
        return response