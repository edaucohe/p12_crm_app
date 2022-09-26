from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from customers.serializers import CustomerSerializer

from customers.models import Customer


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Customer.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            # current_user = self.request.user
            users = list(Customer.objects.all().order_by("id"))
            return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
