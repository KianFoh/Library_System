from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('send_contact_email/', views.send_contact_email, name='send_contact_email'),

]