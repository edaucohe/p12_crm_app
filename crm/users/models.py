from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGEMENT = ("MANAGEMENT", "Management")
        SALE = ("SALE", "Sales")
        SUPPORT = ("SUPPORT", "Support")

    role = models.CharField(max_length=25, choices=Role.choices, verbose_name='role')

    def is_management(self):
        return self.role == self.Role.MANAGEMENT

    def is_sales(self):
        return self.role == self.Role.SALE

    def is_support(self):
        return self.role == self.Role.SUPPORT
