import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from customers.models import Customer
from events.models import Event


class EditUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user.get_group_permissions()
        management_user = user.is_management()

        if request.method == 'GET' and management_user:
            return True
        else:
            logging.warning(f"User '{user}' is not authorize to see list of users")
            return False


class EditCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        management_user = user.is_management()
        sale_user = user.is_sale()
        support_user = user.is_support()

        if request.method == 'GET':
            if management_user or sale_user or support_user:
                return True
            else:
                logging.warning(f"User '{user}' should be part of a group")
                return False

        elif request.method == 'POST':
            if management_user or sale_user:
                return True
            else:
                logging.warning(f"User '{user}' is not authorize to edit this customer")
                return False

        else:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        management_user = user.is_management()
        sale_user_assigned = True if user == obj.user else False

        if request.method == "PUT" or request.method == "DELETE":
            if management_user or sale_user_assigned:
                return True
            else:
                logging.warning(f"User '{user}' is not authorize to edit this customer")
                return False
        else:
            return False


class EditContractPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        management_user = user.is_management()
        sale_user = user.is_sale()
        support_user = user.is_support()

        customer_id = int(view.kwargs.get('customers_pk', None))
        customer = Customer.objects.get(pk=customer_id)
        sale_user_assigned = True if user == customer.user else False

        if request.method == 'GET':
            if management_user or sale_user or support_user:
                return True
            else:
                logging.warning(f"User '{user}' should be part of a group")
                return False

        elif request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            if management_user or sale_user_assigned:
                return True
            else:
                logging.warning(f"User '{user}' is not authorize to edit this contract")
                return False
        else:
            return False


class EditEventPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        management_user = user.is_management()
        sale_user = user.is_sale()
        support_user = user.is_support()

        customer_id = int(view.kwargs.get('customers_pk', None))
        customer = Customer.objects.get(pk=customer_id)
        sale_user_assigned = True if user == customer.user else False

        if request.method == 'GET':
            if management_user or sale_user or support_user:
                return True
            else:
                logging.warning(f"User '{user}' should be part of a group")
                return False

        elif request.method == 'POST':
            if management_user or sale_user_assigned:
                return True
            else:
                logging.warning(f"User '{user}' is not authorize to edit this event")
                return False
        elif request.method == 'PUT' or request.method == 'DELETE':
            event_pk = int(view.kwargs.get('pk', None))
            try:
                event = Event.objects.get(pk=event_pk)
                support_user_assigned = True if user == event.user else False

                if management_user or sale_user_assigned or support_user_assigned:
                    return True
                else:
                    logging.warning(f"User '{user}' is not authorize to edit this event")
                    return False
            except ObjectDoesNotExist:
                logging.warning(f"Event does not exist")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return False


class DisplayEventsPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        management_user = user.is_management()
        sale_user = user.is_sale()
        support_user = user.is_support()

        if request.method == 'GET':
            if management_user or sale_user or support_user:
                return True
            else:
                logging.warning(f"User '{user}' should be part of a group")
                return False
        else:
            return False
