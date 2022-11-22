import logging

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.serializers import EventSerializer

from customers.models import Customer
from contracts.models import Contract
from events.models import Event

from events.filters import EventFilterSet

from users.permissions import EditEventPermission, DisplayEventsPermission


logging.basicConfig(level=logging.INFO)


class EventOfContractViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, EditEventPermission)
    http_method_names = ['get', 'post', 'put', 'delete']

    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilterSet

    def get_queryset(self):
        return Event.objects.all()

    def list(self, request, customers_pk=None, contracts_pk=None, *args, **kwargs):
        try:
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=contracts_pk).get()
            if not contract.customer == customer:
                logging.info(f"'{customer}' does not have this '{contract}'")
                return Response({'message': 'Contract does not match with Customer'},
                                status=status.HTTP_404_NOT_FOUND)

            events = list(Event.objects.filter(contract=contract))
            return Response(self.serializer_class(events, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, customers_pk=None, contracts_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            contract = Contract.objects.filter(pk=contracts_pk).get()

            if not contract.customer == customer:
                logging.info(f"'{customer}' does not have this '{contract}'")
                return Response({'message': 'Contract does not match with Customer'},
                                status=status.HTTP_404_NOT_FOUND)

            if not contract.is_signed():
                logging.info(f"'{contract}' should be signed before event creation")
                return Response({'message': 'Contract is not signed'}, status=status.HTTP_403_FORBIDDEN)

            data = {
                "attendees": request.POST.get('attendees', None),
                "event_date": request.POST.get('event_date', None),
                "notes": request.POST.get('notes', None),
                "customer": customer.pk,
                "user": request.POST.get('user', None),
                "contract": contract.pk,
            }
            serializer = self.serializer_class(data=data, context={'user': current_user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or contract can not exist'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, customers_pk=None, contracts_pk=None, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            event = Event.objects.filter(pk=pk).get()

            if not event.customer == customer:
                logging.info(f"Event '{event}' is not assigned to current {customer}")
                return Response({'message': 'Event is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            contract = Contract.objects.filter(pk=contracts_pk).get()
            if not event.contract == contract:
                logging.info(f"Event '{event}' is not assigned to current {contract}")
                return Response({'message': 'Event is not assigned to current contract'},
                                status=status.HTTP_404_NOT_FOUND)

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
            return Response({'message': 'Customer, contract or event do not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, customers_pk=None, contracts_pk=None, pk=None, *args, **kwargs):
        try:
            customer = Customer.objects.filter(pk=customers_pk).get()
            event = Event.objects.filter(pk=pk).get()

            if not event.customer == customer:
                logging.info(f"Event '{event}' is not assigned to current {customer}")
                return Response({'message': 'Event is not assigned to current customer'},
                                status=status.HTTP_404_NOT_FOUND)

            contract = Customer.objects.filter(pk=contracts_pk).get()
            if not event.contract == contract:
                logging.info(f"Event '{event}' is not assigned to current {contract}")
                return Response({'message': 'Event is not assigned to current contract'},
                                status=status.HTTP_404_NOT_FOUND)

            return super(EventOfContractViewSet, self).destroy(request, customers_pk, *args, **kwargs)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)


class EventsViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, DisplayEventsPermission)
    http_method_names = ['get']

    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilterSet

    def get_queryset(self):
        return Event.objects.all()

    def list(self, request, customers_pk=None, *args, **kwargs):
        try:
            current_user = request.user
            customer = Customer.objects.filter(pk=customers_pk).get()
            if not Event.objects.filter(customer=customers_pk):
                logging.info(f"There is no events for user {current_user}")
                return Response({'message': 'There is no events'}, status=status.HTTP_404_NOT_FOUND)

            events = list(self.filter_queryset(self.get_queryset()))
            own_events = [event for event in events if event.customer == customer]
            return Response(self.serializer_class(own_events, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)

    # def create(self, request, customers_pk=None, *args, **kwargs):
    #     try:
    #         current_user = request.user
    #         customer = Customer.objects.filter(pk=customers_pk).get()
    #
    #         # event = list(Event.objects.filter(customer=customers_pk))[0]
    #         # user_support_assigned = event.is_user_assigned(current_user)
    #
    #         # if not (customer.is_user_assigned(current_user)):
    #         #     logging.info(f"User '{current_user}' is not authorize to create an event for '{customer}' ")
    #         #     return Response({'message': 'You are not authorize to see these events'},
    #         #                     status=status.HTTP_403_FORBIDDEN)
    #         # request_contract = request.POST.get('contract', None)
    #         if not request.POST.get('contract', None):
    #             logging.info(f"'contract' field must be filled")
    #             return Response({'message': 'Fill contract field'}, status=status.HTTP_403_FORBIDDEN)
    #
    #         contract_id = int(request.POST.get('contract', None))
    #         contract = Contract.objects.filter(pk=contract_id).get()
    #         # is_contract_signed = contract.is_contract_signed()
    #         # contract_exist = request.POST.get('contract', None).exists()
    #
    #         # if request.POST.get('contract', None):
    #         #     contract = request.POST.get('contract', None)
    #         if not contract.is_signed():
    #             logging.info(f"Contract '{contract}' should be signed before event creation")
    #             return Response({'message': 'Contract is not signed'}, status=status.HTTP_403_FORBIDDEN)
    #
    #         data = {
    #             "attendees": request.POST.get('attendees', None),
    #             "event_date": request.POST.get('event_date', None),
    #             "notes": request.POST.get('notes', None),
    #             "customer": customer.pk,
    #             "user": request.POST.get('user', None),
    #             "contract": request.POST.get('contract', None),
    #         }
    #         serializer = self.serializer_class(data=data, context={'user': current_user})
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     except ObjectDoesNotExist:
    #         return Response({'message': 'Customer or event can not exist'}, status=status.HTTP_404_NOT_FOUND)
    #
    # def update(self, request, customers_pk=None, pk=None, *args, **kwargs):
    #     try:
    #         current_user = request.user
    #         # customer = Customer.objects.filter(pk=customers_pk).get()
    #         event = Event.objects.filter(pk=pk).get()
    #         #
    #         # if not event.customer == customer:
    #         #     logging.info(f"Event '{event}' is not assigned to current {customer}")
    #         #     return Response({'message': 'Event is not assigned to current customer'},
    #         #                     status=status.HTTP_404_NOT_FOUND)
    #
    #         # can_edit = \
    #         #     current_user.is_management() \
    #         #     or (current_user.is_sales() and customer.is_user_assigned(current_user)) \
    #         #     or event.is_user_assigned(current_user)
    #
    #         # if not can_edit:
    #         #     logging.info(f"User '{current_user}' is not authorize to edit '{customer}' ")
    #         #     return Response({'message': 'You are not authorize to edit this customer'},
    #         #                     status=status.HTTP_403_FORBIDDEN)
    #
    #         serializer = self.serializer_class(
    #             instance=event,
    #             data=request.data,
    #             context={'user': current_user},
    #             partial=True
    #         )
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     except ObjectDoesNotExist:
    #         return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)
    #
    # def destroy(self, request, customers_pk=None, pk=None, *args, **kwargs):
    #     try:
    #         current_user = request.user
    #         customer = Customer.objects.filter(pk=customers_pk).get()
    #         event = Event.objects.filter(pk=pk).get()
    #
    #         if not event.customer == customer:
    #             logging.info(f"Event '{event}' is not assigned to current '{customer}' ")
    #             return Response({'message': 'Event is not assigned to current customer'},
    #                             status=status.HTTP_404_NOT_FOUND)
    #
    #         # can_edit = \
    #         #     current_user.is_management() \
    #         #     or (current_user.is_sales() and customer.is_user_assigned(current_user)) \
    #         #     or event.is_user_assigned(current_user)
    #
    #         # if not can_edit:
    #         #     logging.info(f"User '{current_user}' is not authorize to edit '{customer}' ")
    #         #     return Response({'message': 'You are not authorize to edit this customer'},
    #         #                     status=status.HTTP_403_FORBIDDEN)
    #
    #         return super(EventViewSet, self).destroy(request, customers_pk, *args, **kwargs)
    #
    #     except ObjectDoesNotExist:
    #         return Response({'message': 'Customer or event do not exist'}, status=status.HTTP_404_NOT_FOUND)
