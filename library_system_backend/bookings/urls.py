from django.urls import path
from . import views

urlpatterns = [
    path('', views.bookings, name='bookings'),
    path('approve_booking/', views.approve_booking, name='approve_booking'),
    path('reject_booking/', views.reject_booking, name='reject_booking'),
]