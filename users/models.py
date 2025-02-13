from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=190, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to="profile/", default="profile/user-default.png"
    )
    social_github = models.CharField(max_length=40, null=True, blank=True)
    social_twitter = models.CharField(max_length=40, null=True, blank=True)
    social_linkedin = models.CharField(max_length=40, null=True, blank=True)
    social_youtube = models.CharField(max_length=40, null=True, blank=True)
    social_website = models.CharField(max_length=40, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    email = models.EmailField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    lastRead = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ["is_read", "-created"]
