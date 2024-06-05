from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_208_ALREADY_REPORTED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT


class EmailAlreadyExists(APIException):
    status_code = HTTP_208_ALREADY_REPORTED
    default_detail = _('email already registered')
    default_code = 'email_already_registered'


class InvalidCredentialsException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _('invalid email and/or password.')
    default_code = 'invalid_email_and_or_password'


class FriendRequestAlreadySent(APIException):
    status_code = HTTP_208_ALREADY_REPORTED
    default_detail = _('friend request already sent.')
    default_code = 'friend_request_already_sent'


class SameReceiverException(APIException):
    status_code = HTTP_409_CONFLICT
    default_detail = _("you can't send friend request to yourself")
    default_code = 'same_receiver'


class InvalidReceiverException(APIException):
    status_code = HTTP_409_CONFLICT
    default_detail = _("you can only accept/reject friend requests sent to you")
    default_code = 'invalid_receiver'
