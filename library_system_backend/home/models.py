from django.db import models
from django.utils import timezone
from handlers.models import save_image

class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=False)
    datetime = models.DateTimeField(default=timezone.now, editable=False)
    image = image = models.ImageField(null=False)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the original save method
        save_image(self)  # Call the save_image function passing the instance

    def __str__(self):
        return self.title