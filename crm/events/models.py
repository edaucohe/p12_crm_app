from django.conf import settings
from django.db import models

from users.models import User
from customers.models import Customer


class Event(models.Model):
    class EventStatus(models.TextChoices):
        OPEN = ("OPEN", "Open")
        IN_PROGRESS = ("IN_PROGRESS", "In progress")
        CLOSED = ("CLOSED", "Closed")

    attendees = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    notes = models.TextField()

    status = models.CharField(max_length=25,
                              default=EventStatus.OPEN,
                              choices=EventStatus.choices,
                              verbose_name="Event status")
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_user_assigned(self, user: User) -> bool:
        return self.user == user
