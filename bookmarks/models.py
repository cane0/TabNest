from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets


MAX_ATTEMPTS = 1000

class UniqueAuth(models.Model):
    value = models.CharField(max_length=6, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='unique_auth')
    user_pin = models.CharField(
        default='000000',
        max_length=6,
        validators=[
            RegexValidator(
                r'^\d{4,6}$',
                message='Enter a valid 4 to 6 digit PIN',
                code='invalid_format',
            )
            
        ]
    )

    def __str__(self):
        return f"{self.user.username}'s UniqueAuth"

@receiver(post_save, sender=User)
def create_unique_auth_number(sender, instance, created, **kwargs):
    if created:
        for _ in range(MAX_ATTEMPTS):
            # Generate a 6-digit random value
            value = secrets.token_hex(3)[:6]

            # Checking if the generated value already exists
            if not UniqueAuth.objects.filter(value=value).exists():
                UniqueAuth.objects.create(user=instance, value=value)
                break
        
        else:
            # If we couldn't find a unique value after MAX_ATTEMPTS attempts
            raise RuntimeError("Unable to generate a unique authentication number.")
      

class Session(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    unique_auth = models.ForeignKey(UniqueAuth, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Tab(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='tabs')
    url = models.URLField(max_length=2048)
    logo = models.URLField(max_length=2048)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title}'