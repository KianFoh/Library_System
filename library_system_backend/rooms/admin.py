from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'min_pax', 'max_pax', 'image')

admin.site.register(Room, RoomAdmin)