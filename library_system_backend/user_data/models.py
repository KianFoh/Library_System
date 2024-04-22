from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class user_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_usage_hour = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)])

def __str__(self):
    return self.user.username