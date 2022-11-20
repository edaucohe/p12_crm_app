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
            'contract',
        ]

    def create(self, validated_data):
        return Event.objects.create(**validated_data)
