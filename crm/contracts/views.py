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

        # sale_user_can_see_contracts = services.is_a_customer_assigned(user=current_user, customer=customer)
        # if not sale_user_can_see_contracts:
        #     return Response({'message': 'Customer is not assigned to you'}, status=status.HTTP_403_FORBIDDEN)

        if not customer.is_user_assigned(current_user):
            return Response({'message': 'You are not authorize to see contracts'}, status=status.HTTP_403_FORBIDDEN)

        contracts = [contract for contract in Contract.objects.filter(customer=customer, user=current_user)]
        contracts = sorted(contracts, key=lambda order_by: order_by.id)

        if not contracts:
            return Response({'message': 'Customer does not have contracts'}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, customers_pk=None, *args, **kwargs):
        current_user = request.user
        customer = Customer.objects.filter(pk=customers_pk).get()

        if not customer.is_user_assigned(current_user):
            return Response({'message': 'You are not authorize to create contracts'}, status=status.HTTP_403_FORBIDDEN)

        # user_can_create_contract = services.is_sale_team_user(user=current_user)
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
            return Response({'message': 'You are not part of sales team'},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, customers_pk=None, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=pk).get()

            if not contract.customer == customer:
                return Response({'message': 'Contract is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            # user_cannot_edit_customer = services.is_support_team_user(user=current_user)
            # if user_cannot_edit_customer:
            #     return Response({'message': 'You are not part of sales team'},
            #                     status=status.HTTP_403_FORBIDDEN)
            #
            # sale_user_can_edit_contract = services.is_a_customer_assigned(user=current_user, customer=customer)
            # if not sale_user_can_edit_contract:
            #     return Response({'message': 'Customer is not assigned to you.'}, status=status.HTTP_403_FORBIDDEN)

            can_edit = \
                current_user.is_management() or (current_user.is_sales() and customer.is_user_assigned(current_user))
            if not can_edit:
                return Response({'message': 'You are not authorize to edit this customer'},
                                status=status.HTTP_403_FORBIDDEN)

            # data = {
            #     "amount": request.POST.get('amount', None),
            #     "payment_due": request.POST.get('payment_due', None),
            #     "status": request.POST.get('status', None),
            # }
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
