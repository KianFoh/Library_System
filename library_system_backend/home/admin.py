from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'formatted_datetime', 'image')
    
    # Format datetime field as DD/MM/YYYY HH:MM
    def formatted_datetime(self, obj):
        """Custom method to format datetime field"""
        return obj.datetime.strftime("%d/%m/%Y %I:%M %p")  

    # Sort
    formatted_datetime.admin_order_field = 'datetime'

    # Set column header 
    formatted_datetime.short_description = 'Date and Time' 

admin.site.register(Announcement, AnnouncementAdmin)