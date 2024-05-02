from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_email', 'limit_title', 'formatted_datetime')

    def user_name(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def user_id(self, obj):
        return obj.user.id

    # Format datetime field as DD/MM/YYYY HH:MM
    def formatted_datetime(self, obj):
        """Custom method to format datetime field"""
        return obj.date_time.strftime("%d/%m/%Y %I:%M %p")  

    def limit_title(self,obj):
        max_chars = 20
        if len(obj.title) > max_chars:
            return obj.title[:max_chars] + "..."
        return obj.title

    # Sort
    user_email.admin_order_field = 'user__email'
    user_name.admin_order_field = 'user'
    formatted_datetime.admin_order_field = 'datetime'
    limit_title.admin_order_field = 'title'

    # Set column header 
    user_email.short_description = 'Email'
    user_name.short_description = 'Name'
    formatted_datetime.short_description = 'Date and Time'
    limit_title.short_description = 'Title'
admin.site.register(Contact, ContactAdmin)