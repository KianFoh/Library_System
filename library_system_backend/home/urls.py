from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('announcement/<int:announcement_id>/', views.announcement, name='announcement')
]