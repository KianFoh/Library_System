from django.contrib import admin
from .models import Timeslot, Booking

class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('timeslot_id','room', 'formatted_start_time', 'formatted_end_time', 'status')

    def timeslot_id(self,obj):
        return obj.id
    
    # Format datetime field as DD/MM/YYYY HH:MM
    def formatted_start_time(self, obj):
        """Custom method to format datetime field"""
        return obj.start_time.strftime("%I:%M %p")  
    
    def formatted_end_time(self, obj):
        """Custom method to format datetime field"""
        return obj.end_time.strftime("%I:%M %p")  
    
    # Sort
    timeslot_id.admin_order_field = 'id'
    formatted_start_time.admin_order_field = 'start_time'
    formatted_end_time.admin_order_field = 'end_time'

    # Set column header 
    formatted_start_time.short_description = 'Start Time'
    formatted_end_time.short_description = 'End Time'
    timeslot_id.short_description = 'Time Slot ID'

admin.site.register(Timeslot, TimeslotAdmin)


class BookingAdmin(admin.ModelAdmin):

    list_display = ('id', 'display_users', 'formatted_date_time', 'status')

    def display_users(self, obj):
        return ', '.join([user.username for user in obj.users.all()])
    
        # Format datetime field as DD/MM/YYYY HH:MM
    def formatted_date_time(self, obj):
        """Custom method to format datetime field"""
        return obj.date_time.strftime("%d/%m/%Y %I:%M %p")  

    # Sort
    formatted_date_time.admin_order_field = 'date_time'

    # Set column header
    formatted_date_time.short_description = 'Date and time'
    display_users.short_description = 'Users'

admin.site.register(Booking, BookingAdmin)