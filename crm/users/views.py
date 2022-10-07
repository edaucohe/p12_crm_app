import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer, SignUpSerializer

logging.basicConfig(level=logging.INFO)


class SignUpViewSet(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return get_user_model().objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            users = list(User.objects.all().order_by("id"))
            return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            current_user = request.user
            if not current_user.role == User.Role.MANAGEMENT:
                logging.info(f"User '{current_user}' is not authorize to create an user")
                return Response({'message': 'You are not part of Management team'}, status=status.HTTP_403_FORBIDDEN)
            else:
                data = {
                    "username": request.POST.get("username", None),
                    "first_name": request.POST.get("first_name", None),
                    "role": request.POST.get("role", None),
                }
                serializer = self.serializer_class(data=data, context={'user': current_user})
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
