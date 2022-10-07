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

logging.basicConfig(level=logging.INFO)


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContractFilterSet

    def get_queryset(self):
        return Contract.objects.all()

    def list(self, request, customers_pk=None, *args, **kwargs):
        current_user = request.user
        customer = Customer.objects.filter(pk=customers_pk).get()

        if not (customer.is_user_assigned(current_user) or current_user.is_management()):
            logging.info(f"There is no contracts for '{customer}' ")
            return Response({'message': 'You are not authorize to see contracts'}, status=status.HTTP_403_FORBIDDEN)

        contracts = self.filter_queryset(self.get_queryset())
        return Response(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, customers_pk=None, *args, **kwargs):
        current_user = request.user
        customer = Customer.objects.filter(pk=customers_pk).get()

        if not customer.is_user_assigned(current_user):
            logging.info(f"User '{current_user}' is not authorize to create a contract for '{customer}' ")
            return Response({'message': 'You are not authorize to create contracts'}, status=status.HTTP_403_FORBIDDEN)

        if current_user.is_sales():
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
            logging.info(f"User '{current_user}' is not authorize to create a contract")
            return Response({'message': 'You are not part of sales team'},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, customers_pk=None, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=pk).get()

            if not contract.customer == customer:
                logging.info(f"Contract '{contract}' is not assigned to current {customer}")
                return Response({'message': 'Contract is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            can_edit = \
                current_user.is_management() or (current_user.is_sales() and customer.is_user_assigned(current_user))
            if not can_edit:
                logging.info(f"User '{current_user}' is not authorize to create a contract")
                return Response({'message': 'You are not authorize to edit this customer'},
                                status=status.HTTP_403_FORBIDDEN)

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
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=pk).get()

            if not contract.customer == customer:
                logging.info(f"Contract '{contract}' is not assigned to current {customer}")
                return Response({'message': 'Contract is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            can_edit = \
                current_user.is_management() or (current_user.is_sales() and customer.is_user_assigned(current_user))
            if not can_edit:
                logging.info(f"User '{current_user}' is not authorize to delete this contract")
                return Response({'message': 'You are not authorize to delete this contract'},
                                status=status.HTTP_403_FORBIDDEN)

            return super(ContractViewSet, self).destroy(request, customers_pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract do not exist'}, status=status.HTTP_404_NOT_FOUND)

