from rest_framework.serializers import ModelSerializer, CharField

from customers.models import Customer


class CustomerSerializer(ModelSerializer):
    employee_assigned = CharField(source='user.username')
    employee_role = CharField(source='user.get_role_display')
    status = CharField(source='get_status_display')

    class Meta:
        model = Customer
        fields = [
            'id',
            'first_name',
            'email',
            'company_name',
            'created_date',
            'status',
            'employee_assigned',
            'employee_role'
        ]
