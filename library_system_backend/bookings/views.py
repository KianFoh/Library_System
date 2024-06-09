from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from .models import Booking, BookingUser
from django.contrib import messages
from datetime import datetime, date

def bookings(request):
    if not request.user.is_authenticated:
        messages.warning(request, mark_safe('Please login before accessing the Booking page'))
        return redirect('login')

    # Get today's date
    today_date = date.today()

    # Filter bookings made today
    bookings_user = BookingUser.objects.filter(user=request.user, booking__date_time__date=today_date).order_by('-id')
    bookings = Booking.objects.filter(bookinguser__in=bookings_user).order_by('-id')
    pending_booking_ids = bookings_user.filter(status='Pending').values_list('booking_id', flat=True)

    return render(request, 'bookings/bookings.html', {
        'bookings': bookings,
        'pending_booking_ids': pending_booking_ids,
    })

def approve_booking(request):
    if request.method == 'POST':
        return handle_booking_update(request, 'Approved')
    return redirect('bookings')

def reject_booking(request):
    if request.method == 'POST':
        return handle_booking_update(request, 'Rejected')
    return redirect('bookings')

def handle_booking_update(request, new_status):
    booking_id = request.POST.get('booking_id')
    user_id = request.POST.get('user_id')
    try:
        booking_user = BookingUser.objects.get(booking_id=booking_id, user_id=user_id)
        if booking_user.status == 'Pending':
            booking_user.status = new_status
            booking_user.save()
            booking = Booking.objects.get(id=booking_id)
            booking.update_status(request)
        else:
            messages.warning(request, mark_safe('You have already approved or rejected this booking.'))
    except BookingUser.DoesNotExist:
        messages.error(request, 'Invalid booking or user.')
    return redirect('bookings')
