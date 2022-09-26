from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, EmailField, ValidationError
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'role']


class SignUpSerializer(ModelSerializer):
    password = CharField(required=True, validators=[validate_password])
    password2 = CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Please write the same password"})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
