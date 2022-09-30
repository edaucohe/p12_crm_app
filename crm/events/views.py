from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.serializers import EventSerializer

from customers.models import Customer
from contracts.models import Contract
from events.models import Event


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Event.objects.all()

    def list(self, request, customers_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            event = Event.objects.filter(customer=customers_pk).get()

            if not (customer.is_user_assigned(current_user) or event.is_user_assigned(current_user)):
                return Response({'message': 'You are not authorize to see these events'},
                                status=status.HTTP_403_FORBIDDEN)

            events = [event for event in Event.objects.filter(customer=customer)]
            events = sorted(events, key=lambda order_by: order_by.id)

            if not events:
                return Response({'message': 'There is no events for this customer'}, status=status.HTTP_404_NOT_FOUND)

            return Response(self.serializer_class(events, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)
