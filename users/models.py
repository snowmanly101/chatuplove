from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    MARITAL_CHOICES = (
        ('single', 'Single'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
        ('widowed', 'Widowed'),
    )

    # Account Basics
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    looking_for = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(default=25)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Physical & Demographic Details
    height = models.CharField(max_length=20, blank=True, null=True)
    body_type = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, default='single')
    languages = models.CharField(max_length=100, blank=True, null=True)

    # Lifestyle & Values
    smoking = models.CharField(max_length=30, blank=True, null=True)
    drinking = models.CharField(max_length=30, blank=True, null=True)
    diet = models.CharField(max_length=50, blank=True, null=True)
    has_kids = models.CharField(max_length=30, blank=True, null=True)
    wants_kids = models.CharField(max_length=30, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    politics = models.CharField(max_length=50, blank=True, null=True)

    # Written Profile & Media
    bio = models.TextField(blank=True, null=True, verbose_name="About Me Essay")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username