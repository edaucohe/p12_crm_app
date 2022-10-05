from django_filters import rest_framework as filters

from contracts.models import Contract


class ContractFilterSet(filters.FilterSet):
    company_name = filters.CharFilter(field_name="customer", lookup_expr='company_name')
    email = filters.CharFilter(field_name="customer", lookup_expr='email')
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    payment_due = filters.DateFilter(field_name="payment_due", lookup_expr='icontains')

    class Meta:
        model = Contract
        fields = ['company_name', 'email', 'min_amount', 'max_amount', 'payment_due']
