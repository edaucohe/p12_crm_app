import logging

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from contracts.serializers import ContractSerializer

from contracts.models import Contract
from customers.models import Customer

from contracts.filters import ContractFilterSet

from users.permissions import EditContractPermission

logging.basicConfig(level=logging.INFO)


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated, EditContractPermission)
    http_method_names = ['get', 'post', 'put', 'delete']

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContractFilterSet

    def get_queryset(self):
        return Contract.objects.all()

    def list(self, request, customers_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            if not Contract.objects.filter(customer=customers_pk):
                logging.info(f"There is no contracts for user {current_user}")
                return Response({'message': 'There is no contracts'}, status=status.HTTP_403_FORBIDDEN)

            contracts = list(self.filter_queryset(self.get_queryset()))
            own_contracts = [contract for contract in contracts if contract.customer == customer]
            return Response(self.serializer_class(own_contracts, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, customers_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()

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

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, customers_pk=None, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=pk).get()

            if not contract.customer == customer:
                logging.info(f"Contract '{contract}' is not assigned to current {customer}")
                return Response({'message': 'Contract is not assigned to current customer'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = self.serializer_class(
                instance=contract,
                data=request.data,
                context={'user': current_user},
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, customers_pk=None, *args, **kwargs):
        try:
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=pk).get()
            if not contract.customer == customer:
                logging.info(f"Contract '{contract}' is not assigned to current {customer}")
                return Response({'message': 'Contract is not assigned to current customer'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            return super(ContractViewSet, self).destroy(request, customers_pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract do not exist'}, status=status.HTTP_404_NOT_FOUND)

