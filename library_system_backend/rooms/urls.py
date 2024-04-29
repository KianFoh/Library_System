from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('room/<int:room_id>/', views.room, name='room')
]