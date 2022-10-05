from django_filters import rest_framework as filters

from contracts.models import Contract


class ContractFilterSet(filters.FilterSet):
    customer_id = filters.CharFilter(field_name="customer_id", lookup_expr='exact')
    # email = filters.CharFilter(field_name="email", lookup_expr='icontains')
    # amount = filters.NumberFilter(field_name="amount", lookup_expr='icontains')
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    payment_due = filters.DateFilter(field_name="payment_due", lookup_expr='icontains')

    class Meta:
        model = Contract
        fields = ['customer_id', 'min_amount', 'max_amount', 'payment_due']
