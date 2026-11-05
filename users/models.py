from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(default=25)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    looking_for = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username