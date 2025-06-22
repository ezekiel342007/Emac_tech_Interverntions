from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="blogs_with_tag")
    image_url = models.URLField(blank=True, null=True)
    body = models.TextField()
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name="blogs")
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()
    posted_on = models.DateTimeField(auto_now=True, editable=False)
    updated_on = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.body[0:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    writer = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    made_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.body[0:50]


class Watchings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    watcher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="watchers")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="authors")
    joined_watch_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.watcher} joined watch on {self.author}"
