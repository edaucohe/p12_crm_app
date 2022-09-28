from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from contracts.serializers import ContractSerializer

from contracts.models import Contract
from users import services
from customers.models import Customer


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Contract.objects.all()

    def list(self, request, customers_pk=None, *args, **kwargs):
        current_user = request.user
        customer = Customer.objects.filter(pk=customers_pk).get()

        if not customer.user == current_user:
            return Response({'message': 'Customer is not assigned to you'}, status=status.HTTP_200_OK)

        contracts = [contract for contract in Contract.objects.filter(customer=customer, user=current_user)]
        contracts = sorted(contracts, key=lambda order_by: order_by.id)

        if not contracts:
            return Response({'message': 'Customer does not have contracts'}, status=status.HTTP_200_OK)

        return Response(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK)
