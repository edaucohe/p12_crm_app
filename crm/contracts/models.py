from django.conf import settings
from django.db import models

from customers.models import Customer


class Contract(models.Model):
    amount = models.FloatField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    payment_due = models.DateTimeField()

    status = models.BooleanField(max_length=25, verbose_name="Contract signed")
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
