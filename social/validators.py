from django.contrib.auth.models import User
from .exceptions import EmailAlreadyExists


def is_unique_email(email: str):
    if User.objects.filter(email__iexact=email).exists():
        raise EmailAlreadyExists
