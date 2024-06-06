from django.urls import path
from . import views

urlpatterns = [
    path('request-password-change/', views.request_password_change, name='request_password_change'),
    path('update/', views.profile_update, name='profile_update'),
    path('<str:username>/', views.profile_, name='profile'),
    path('', views.profile_redirect, name='profile_redirect'),
]