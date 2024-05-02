from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Room 
from bookings.models import Timeslot 
from datetime import datetime

def rooms(request):
    rooms_data = Room.objects.order_by('-id')
    template = loader.get_template('rooms/rooms.html')

    current_datetime = datetime.now()
    current_hour = current_datetime.hour
    timeslots_available_now = Timeslot.objects.filter(start_time__hour=current_hour, status='Empty')
    available_rooms_id = timeslots_available_now.values_list('room_id', flat=True)

    context = {
        'rooms' : rooms_data,
        'available_rooms': available_rooms_id
    }

    return HttpResponse(template.render(context, request))

def room(request, room_id):
    room_data = get_object_or_404(Room, pk=room_id)
    room_timeslot = Timeslot.objects.filter(room_id=room_id)
    return render(request, 'rooms/room.html', {'room': room_data, 'timeslots':room_timeslot})