from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
