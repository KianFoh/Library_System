from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=False)
    datetime = models.DateTimeField(default=timezone.now, editable=False)
    image = image = models.ImageField(upload_to='home/announcement_images')

    def __str__(self):
        return self.title