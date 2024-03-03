from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name='email_confirmation_sent'),
]