from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGEMENT = ("MANAGEMENT", "Management")
        SALE = ("SALE", "Sales")
        SUPPORT = ("SUPPORT", "Support")

    role = models.CharField(max_length=25, choices=Role.choices, verbose_name='role')
