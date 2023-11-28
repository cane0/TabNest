from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
import random
import string
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default_dp.png', upload_to='profile_pics')
    # pin = models.CharField(max_length=15, )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    # def save(self, )

@receiver(post_save, sender=User)
def create_unique_auth_number(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
