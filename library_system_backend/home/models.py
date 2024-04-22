from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=False)
    datetime = models.DateTimeField(null=False)
    image = models.BinaryField(null=False)

    def __str__(self):
        return self.title