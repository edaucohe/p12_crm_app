from rest_framework.serializers import ModelSerializer

from customers.models import Customer


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id',
            'first_name',
            'email',
            'company_name',
            'created_date',
            'status',
            'user',
        ]

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)
