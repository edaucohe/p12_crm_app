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
            # event = list(Event.objects.filter(customer=customers_pk))
            # user_support_assigned = [event.is_user_assigned(current_user)
            #                          for event in Event.objects.filter(customer=customer)]
            event = list(Event.objects.filter(customer=customers_pk))[0]
            user_support_assigned = event.is_user_assigned(current_user)

            if not (customer.is_user_assigned(current_user) or user_support_assigned):
                return Response({'message': 'You are not authorize to see these events'},
                                status=status.HTTP_403_FORBIDDEN)

            events = [event for event in Event.objects.filter(customer=customer)]
            events = sorted(events, key=lambda order_by: order_by.id)

            if not events:
                return Response({'message': 'There is no events for this customer'}, status=status.HTTP_404_NOT_FOUND)

            return Response(self.serializer_class(events, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, customers_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            # event = Event.objects.filter(customer=customers_pk).get()
            # user_support_assigned = [event.is_user_assigned(current_user)
            #                          for event in Event.objects.filter(customer=customer)]

            event = list(Event.objects.filter(customer=customers_pk))[0]
            user_support_assigned = event.is_user_assigned(current_user)

            if not (customer.is_user_assigned(current_user) or user_support_assigned):
                return Response({'message': 'You are not authorize to see these events'},
                                status=status.HTTP_403_FORBIDDEN)

            data = {
                "attendees": request.POST.get('attendees', None),
                "event_date": request.POST.get('event_date', None),
                "notes": request.POST.get('notes', None),
                "customer": customer.pk,
                "user": event.user.pk,
            }
            serializer = self.serializer_class(data=data, context={'user': current_user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, customers_pk=None, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            event = Event.objects.filter(pk=pk).get()

            if not event.customer == customer:
                return Response({'message': 'Event is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            can_edit = \
                current_user.is_management() \
                or (current_user.is_sales() and customer.is_user_assigned(current_user)) \
                or event.is_user_assigned(current_user)

            if not can_edit:
                return Response({'message': 'You are not authorize to edit this customer'},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(
                instance=event,
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
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, customers_pk=None, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            event = Event.objects.filter(pk=pk).get()

            if not event.customer == customer:
                return Response({'message': 'Event is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            can_edit = \
                current_user.is_management() \
                or (current_user.is_sales() and customer.is_user_assigned(current_user)) \
                or event.is_user_assigned(current_user)

            if not can_edit:
                return Response({'message': 'You are not authorize to edit this customer'},
                                status=status.HTTP_403_FORBIDDEN)

            return super(EventViewSet, self).destroy(request, customers_pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract do not exist'}, status=status.HTTP_404_NOT_FOUND)
