from django_filters import rest_framework as filters

from events.models import Event


class EventFilterSet(filters.FilterSet):
    company_name = filters.CharFilter(field_name="customer", lookup_expr='company_name')
    email = filters.CharFilter(field_name="customer", lookup_expr='email')
    event_date = filters.DateFilter(field_name="event_date", lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['company_name', 'email', 'event_date']
