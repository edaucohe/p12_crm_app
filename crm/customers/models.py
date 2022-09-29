from django.conf import settings
from django.db import models

from users.models import User


class Customer(models.Model):
    class CustomerStatus(models.TextChoices):
        POTENTIAL_CUSTOMER = ("POTENTIAL", "Potential customer")
        EXISTING_CUSTOMER = ("EXISTING", "Existing customer")

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)

    company_name = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=25,
                              default=CustomerStatus.POTENTIAL_CUSTOMER,
                              choices=CustomerStatus.choices,
                              verbose_name="Customer status")

    def is_user_assigned(self, user: User) -> bool:
        return self.user == user
