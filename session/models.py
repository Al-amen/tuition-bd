from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# Create your models here.


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),

    )
    CATEGORY = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )
    BLOOD_GROUP = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    address = models.CharField(max_length=13)
    phone = models.CharField(max_length=130)
    nationality = models.CharField(max_length=30)
    religion = models.CharField(max_length=50)
    biodata = models.TextField()
    profession = models.CharField(max_length=50, choices=CATEGORY, null=True)
    image = models.ImageField(default='default.jpg',
                              upload_to='session/images')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
