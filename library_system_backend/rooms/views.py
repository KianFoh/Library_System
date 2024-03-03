from django.shortcuts import render
from django.http import HttpResponse

def rooms(request):
    return render(request, 'rooms/rooms.html')