from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100, null=False)
    max_pax = models.IntegerField(null=False)
    min_pax = models.IntegerField(null=False)
    image = models.BinaryField(null=False)

    def __str__(self):
        return self.name