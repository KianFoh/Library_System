from django.contrib import admin
from .models import User_data

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('get_user_id', 'user_name', 'user_email', 'room_usage_hour')  # Include user's email, id, and room usage hour
    
    def user_name(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def get_user_id(self, obj):
        return obj.user.id

    # Email Sorting
    user_email.admin_order_field = 'user__email'
    get_user_id.admin_order_field = 'user__id'
    user_name.admin_order_field = 'user'

    # Set column header 
    get_user_id.short_description = 'ID'
    user_email.short_description = 'Email'
    user_name.short_description = 'Name'

admin.site.register(User_data, UserDataAdmin)