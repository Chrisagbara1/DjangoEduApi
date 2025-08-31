
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom user with an is_teacher flag.
    Only signed-up users are allowed; they can be teachers or learners.
    """
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username
