from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from datetime import date

from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    mobile_number = models.CharField(default='', max_length=10)
    gender = models.CharField(default='', max_length=10)
    date_of_birth = models.DateField(default='2000-01-01')
    country = models.CharField(default='India', max_length=20)
    modified_date = models.DateTimeField(default=timezone.now())
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Profile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='to_user', on_delete=models.CASCADE)
    status = models.CharField(default='', max_length=10)