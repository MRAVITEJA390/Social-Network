from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField
from social.validators import is_unique_email


class CreateUserSerializer(ModelSerializer):
    username = CharField(required=False)
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    email = EmailField(validators=[is_unique_email])
    password = CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name')


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id')


class LoginUserSerializer(Serializer):
    email = EmailField()
    password = CharField(max_length=128, write_only=True)
