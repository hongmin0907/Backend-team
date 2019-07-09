from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.username