from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from customers.serializers import CustomerSerializer

from customers.models import Customer
from users import services


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Customer.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            users = list(Customer.objects.all().order_by("id"))
            return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        # user_data = {
        #     "id": user.pk,
        #     "username": user.username,
        #     "role": user.role
        # }
        customer_status = Customer.status.field.choices[0][0]

        user_can_add_potential_customer = services.is_sale_team_user(user=current_user)
        if user_can_add_potential_customer:
            data = {
                "first_name": request.POST.get('first_name', None),
                "last_name": request.POST.get('last_name', None),
                "email": request.POST.get('email', None),
                "phone": request.POST.get('phone', None),
                "mobile": request.POST.get('mobile', None),
                "company_name": request.POST.get('company_name', None),
                # "employee_assigned": user.username,
                # "employee_role": user.role,
                "status": customer_status,
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

    def update(self, request, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer: Customer = self.get_object()

            user_cannot_edit_customer = services.is_support_team_user(user=current_user)
            if user_cannot_edit_customer:
                return Response({'message': 'You are not part of sales team'},
                                status=status.HTTP_403_FORBIDDEN)

            sale_user_can_edit_customer = services.is_a_customer_assigned(user=current_user, customer=customer)
            if not sale_user_can_edit_customer:
                return Response({'message': 'Customer is not assigned to you.'}, status=status.HTTP_403_FORBIDDEN)

            data = {
                "first_name": request.POST.get('first_name', None),
                "last_name": request.POST.get('last_name', None),
                "email": request.POST.get('email', None),
                "phone": request.POST.get('phone', None),
                "mobile": request.POST.get('mobile', None),
                "company_name": request.POST.get('company_name', None),
                "status": request.POST.get('status', None),
            }
            serializer = self.serializer_class(
                instance=customer,
                data=data,
                context={'user': current_user},
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
