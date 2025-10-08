from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Watchings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    watcher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="watchers"
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="authors"
    )
    joined_watch_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.watcher} joined watch on {self.author}"
