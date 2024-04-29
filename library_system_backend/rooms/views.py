from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Room 
from bookings.models import Timeslot 
from datetime import datetime
from .form import RoomForm

def rooms(request):
    rooms_data = Room.objects.order_by('id')
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
    room_timeslots = Timeslot.objects.filter(room_id=room_id)

    timeslot_choices = []

    for timeslot in room_timeslots:
        timeslot_display = f"{timeslot.start_time.strftime('%H:%M')} - {timeslot.end_time.strftime('%H:%M')}"
        if timeslot.status == 'Empty':
            timeslot_choices.append((timeslot.id, timeslot_display))
        else:
            timeslot_choices.append((timeslot.id, f"{timeslot_display} (Unavailable)"))

    form = RoomForm()
    form.fields['timeslots'].choices = timeslot_choices
    return render(request, 'rooms/room.html', {'room': room_data, 'timeslots':room_timeslots, 'form':form})