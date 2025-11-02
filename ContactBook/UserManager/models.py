from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MySuperUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, default=None)
    address = models.CharField(max_length=750, null=True, default=None)
    profile_picture = models.TextField(null=True, default=None)
    
    def __str__(self):
        return f"{self.get_full_name()}: {self.phone_number}"
    