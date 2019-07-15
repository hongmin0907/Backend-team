from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phoneNumber = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.username