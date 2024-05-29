from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from .models import Booking, BookingUser
from django.contrib import messages

def bookings(request):
    if request.user.is_authenticated:
        bookings_user = BookingUser.objects.filter(user=request.user).order_by('-id')
        bookings = Booking.objects.filter(bookinguser__in=bookings_user).order_by('-id')
        pending_booking_ids = bookings_user.filter(status='Pending').values_list('booking_id', flat=True)

        return render(request, 'bookings/bookings.html', {
            'bookings': bookings,
            'pending_booking_ids': pending_booking_ids,
        })
    
    else:
        message_content = mark_safe('Please login before accessing Booking page')
        messages.warning(request, message_content)
        return redirect('login') 

def approve_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        user_id = request.POST.get('user_id')
        booking_user = BookingUser.objects.get(booking_id=booking_id, user_id=user_id)
        if (booking_user.status == 'Pending'):
            booking = Booking.objects.get(id=booking_id)
            booking_user.status = 'Approved'
            booking_user.save()
            booking.update_status(request)
        else:
            message_content = mark_safe('You have already approved or rejected this booking.')
            messages.warning(request, message_content)
        return redirect('bookings')
    else:
        return redirect('bookings')

def reject_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        user_id = request.POST.get('user_id')
        booking_user = BookingUser.objects.get(booking_id=booking_id, user_id=user_id)
        if (booking_user.status == 'Pending'):
            booking = Booking.objects.get(id=booking_id)
            booking_user.status = 'Rejected'
            booking_user.save()
            booking.update_status(request)
        else:
            message_content = mark_safe('You have already approved or rejected this booking.')
            messages.warning(request, message_content)
        return redirect('bookings')
    else:
        return redirect('bookings')