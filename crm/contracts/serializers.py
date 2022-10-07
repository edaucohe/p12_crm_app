from rest_framework.serializers import ModelSerializer

from contracts.models import Contract


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = [
            'id',
            'amount',
            'payment_due',
            'status',
            'customer',
            'user',
        ]

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)
