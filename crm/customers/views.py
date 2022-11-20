import logging

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from customers.serializers import CustomerSerializer
from customers.models import Customer
from customers.filters import CustomerFilterSet

from users.permissions import EditCustomerPermission

logging.basicConfig(level=logging.INFO)


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated, EditCustomerPermission)
    http_method_names = ['get', 'post', 'put', 'delete']

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomerFilterSet

    def get_queryset(self):
        return Customer.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            customers = self.filter_queryset(self.get_queryset())
            return Response(self.serializer_class(customers, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        data = {
            "first_name": request.POST.get('first_name', None),
            "last_name": request.POST.get('last_name', None),
            "email": request.POST.get('email', None),
            "phone": request.POST.get('phone', None),
            "mobile": request.POST.get('mobile', None),
            "company_name": request.POST.get('company_name', None),
            "user": current_user.pk,
            }

        serializer = self.serializer_class(data=data, context={'user': current_user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer: Customer = self.get_object()

            serializer = self.serializer_class(
                instance=customer,
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
            return Response({'message': 'Customer does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            return super(CustomerViewSet, self).destroy(request, pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
