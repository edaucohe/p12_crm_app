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
            return Response({'message': 'Customer is not assigned to you'}, status=status.HTTP_403_FORBIDDEN)

        contracts = [contract for contract in Contract.objects.filter(customer=customer, user=current_user)]
        contracts = sorted(contracts, key=lambda order_by: order_by.id)

        if not contracts:
            return Response({'message': 'Customer does not have contracts'}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, customers_pk=None, *args, **kwargs):
        current_user = request.user
        customer = Customer.objects.filter(pk=customers_pk).get()

        if not customer.user == current_user:
            return Response({'message': 'Customer is not assigned to you'}, status=status.HTTP_403_FORBIDDEN)

        user_can_create_contract = services.is_sale_team_user(user=current_user)
        if user_can_create_contract:
            data = {
                "amount": request.POST.get('amount', None),
                "payment_due": request.POST.get('payment_due', None),
                "status": request.POST.get('status', None),
                "customer": customer.pk,
                "user": current_user.pk,
            }
            serializer = self.serializer_class(data=data, context={'user': current_user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'You are not part of sales team'},
                            status=status.HTTP_403_FORBIDDEN)
