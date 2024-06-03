from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_, name='profile'),
    path('', views.profile_redirect, name='profile_redirect'),
]