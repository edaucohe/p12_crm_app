from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from events.models import Event


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'attendees',
            'created_date',
            'event_date',
            'status',
            'notes',
            'customer',
            'user',
        ]