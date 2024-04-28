from django.db import models
from django.utils import timezone
from PIL import Image

class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=False)
    datetime = models.DateTimeField(default=timezone.now, editable=False)
    image = image = models.ImageField(null=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        output_size = (500, 500)
        img.thumbnail(output_size)

        img.save(self.image.path)

    def __str__(self):
        return self.title