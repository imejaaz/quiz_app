from django.db import models
from django.contrib.auth.models import User
from quiz.utility import generate_random_id


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100, blank=True, null=True)
    user_rid = models.CharField(
        max_length=5, unique=True, default=generate_random_id)

    def __str__(self):
        return f"{self.user.username}'s Profile"
