from django.db import models
from handlers.models import save_image

class Room(models.Model):
    name = models.CharField(max_length=100, null=False)
    min_pax = models.IntegerField(null=False)
    max_pax = models.IntegerField(null=False)
    image = image = models.ImageField(null=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the original save method
        save_image(self)  # Call the save_image function passing the instance

    def __str__(self):
        return self.name
