from django.shortcuts import render
from django.http import HttpResponse

def bookings(request):
    return render(request, 'bookings/bookings.html')