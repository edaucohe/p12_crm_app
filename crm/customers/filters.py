from django_filters import rest_framework as filters

from customers.models import Customer


class CustomerFilterSet(filters.FilterSet):
    company_name = filters.CharFilter(field_name="company_name", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['company_name', 'email']
