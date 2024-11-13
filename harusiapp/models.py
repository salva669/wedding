# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    user_type = models.ForeignKey(UserType, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    # REQUIRED_FIELDS tells Django which fields are required when creating a superuser
    REQUIRED_FIELDS = ['user_type']
