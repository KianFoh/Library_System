from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Announcement 

def home(request):
    annoucements_data = Announcement.objects.order_by('-datetime')
    template = loader.get_template('home/home.html')
    context = {
        'annoucements': annoucements_data
    }

    return HttpResponse(template.render(context, request))

def announcement(request, announcement_id):
    announcement_data = get_object_or_404(Announcement, pk=announcement_id)
    return render(request, 'home/announcement.html', {'announcement': announcement_data})