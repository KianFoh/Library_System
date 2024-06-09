from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Room
from bookings.models import Timeslot, Booking, BookingUser
from datetime import datetime, time
from .forms import RoomForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from user_data.models import User_data 
from django.core.mail import EmailMessage

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

# Function to send booking confirmation email
def send_booking_email(booking_id, users, initiator, room, room_timeslots, request):
    recipients = [user.email for user in users]

    # Construct the URL for the website
    website_url = "http://127.0.0.1:8000/"

    subject = f'Booking Approval Request: ID {booking_id}'
    message = (
         f'Booking Approval Request for Booking ID {booking_id}\n\n'
        f'Hello,\n\n'
        f'You have a pending booking confirmation.\n\n'
        f'Room: {room.name}\n\n'
        f'Timeslot:\n'
    )

    for timeslot in room_timeslots:
        message += f'{timeslot.start_time.strftime("%I:%M %p")} - {timeslot.end_time.strftime("%I:%M %p")}\n'

    # Construct the students' names string
    students_names = ", ".join(user.username for user in users)
    
    # Add (Initiator) after the initiator's name if it's a student
    students_names_list = students_names.split(", ")
    if initiator.username in students_names_list:
        students_names_list[students_names_list.index(initiator.username)] += " (Initiator)"
        students_names = ", ".join(students_names_list)

    message += (
        f'\nStudents: {students_names}.\n'
        f'Please go to the booking page on the library room booking website to approve the booking:\n'
        f'{website_url}\n\n'
        'If you don\'t approve, please disregard this email.\n\n'  # Adjusted to "don't approve"
        'Thank you.\n'
    )

    try:
        email = EmailMessage(subject, message, to=recipients)
        email.send()
        message_content = 'Booking has been added. Please go to the booking page to approve.'
        messages.success(request, message_content)
    except Exception as e:
        message_content = f'Failed to send booking confirmation email to {", ".join(recipients)}: {str(e)}'
        messages.warning(request, message_content)

def room(request, room_id):
    room_data = get_object_or_404(Room, pk=room_id)
    room_timeslots = Timeslot.objects.filter(room_id=room_id)
    timeslot_choices = []
    current_time = datetime.now().time()
    start_time = time(8, 0, 0)
    end_time = time(18, 0, 0)

    if start_time <= current_time <= end_time:
        for timeslot in room_timeslots:
            timeslot_display = f"{timeslot.start_time.strftime('%I:%M %p')} - {timeslot.end_time.strftime('%I:%M %p')}"
            if timeslot.status == 'Empty' and current_time < timeslot.end_time.time():
                timeslot_choices.append((timeslot.id, timeslot_display))
    
    if timeslot_choices:
        if request.method == 'POST':
            form = RoomForm(request.POST, min_users=room_data.min_pax, max_users=room_data.max_pax)
            form.fields['timeslots'].choices = timeslot_choices
            if form.is_valid():
                # Process form data
                usernames = form.cleaned_data['usernames']
                selected_timeslots_id = form.cleaned_data['timeslots']
                num_timeslots = len(selected_timeslots_id)
                
                if not request.user.is_authenticated:
                    message_content = mark_safe('Please log in to your account before adding a booking.')
                    messages.warning(request, message_content)                    
                elif not num_timeslots:
                    message_content = mark_safe('Please select a timeslot from the available options.')
                    messages.warning(request, message_content)
                elif request.user.username not in usernames:
                    message_content = mark_safe('Your username must be included in the usernames.')
                    messages.warning(request, message_content)
                elif len(usernames) != len(set(usernames)):
                    message_content = mark_safe('Usernames must be unique. Please ensure there are no duplicate entries.')
                    messages.warning(request, message_content)
                else:
                    users_data = []
                    time_slots_data = []

                    for username in usernames:
                        try:
                            user_temp = User.objects.get(username=username)
                            user_addit_data = User_data.objects.get(user=user_temp)
                            users_data.append(user_temp)          
                            
                            if user_addit_data.room_usage_hour == 2:
                                message_content = mark_safe(f'{username} has reached the maximum daily booking limit of 2 hours.')
                                messages.warning(request, message_content)
                                return redirect('room', room_id=room_id)  
                            
                            elif user_addit_data.room_usage_hour + num_timeslots > 2:
                                message_content = mark_safe(f'{username} does not have enough remaining booking hours. Maximum daily booking limit is 2 hours. {username} has {2-user_addit_data.room_usage_hour} hours left.')
                                messages.warning(request, message_content)
                                return redirect('room', room_id=room_id)  
                                
                        except User.DoesNotExist:   
                            message_content = mark_safe(f'{username} is not a valid username.')
                            messages.warning(request, message_content)
                            return redirect('room', room_id=room_id)     

                    for selected_timeslot_id in selected_timeslots_id:
                        time_slot_data = Timeslot.objects.get(id=selected_timeslot_id)
                        time_slots_data.append(time_slot_data)

                    new_booking = Booking.objects.create()
                    new_booking.time_slot.set(time_slots_data)

                    # Create BookingUser instances for each user in users_data
                    for user in users_data:
                        booking_user = BookingUser.objects.create(booking=new_booking, user=user)
                        booking_user.save()

                    new_booking.save()

                    #Send booking confirmation email to all users involve
                    send_booking_email(new_booking.id ,users_data, request.user, room_data, time_slots_data, request)

        else:
            form = RoomForm(min_users=room_data.min_pax, max_users=room_data.max_pax)
            form.fields['timeslots'].choices = timeslot_choices
    else:
        form = None  # If no empty timeslots, set form to None
    
    return render(request, 'rooms/room.html', {'room': room_data, 'timeslots':room_timeslots, 'form':form})