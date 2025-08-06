from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    # date_joined is already included in AbstractUser

    def __str__(self):
        return self.username
