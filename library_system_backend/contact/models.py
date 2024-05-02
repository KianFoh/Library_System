from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=300)
    date_time = models.DateTimeField(default=timezone.now, editable=False)


    def __str__(self):
        return self.title