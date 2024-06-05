from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, CharField
from social.models import FriendRequest
from social.exceptions import FriendRequestAlreadySent, SameReceiverException, InvalidReceiverException


class FriendRequestDetailSerializer(ModelSerializer):
    receiver = CharField()
    sender = CharField()
    status = CharField(source='get_status_display')

    class Meta:
        model = FriendRequest
        fields = ('id', 'receiver', 'sender', 'status')


class SendFriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('receiver', 'status')
        read_only_fields = ('status',)

    def create(self, validated_data: dict):
        request: Request = self.context.get('request')
        sender: User = request.user
        receiver: User = validated_data['receiver']

        if sender == receiver:
            raise SameReceiverException

        already_states = [FriendRequest.Status.SENT, FriendRequest.Status.ACCEPT]
        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status__in=already_states).exists() or \
                FriendRequest.objects.filter(sender=receiver, receiver=sender, status__in=already_states).exists():
            raise FriendRequestAlreadySent

        friend_request: FriendRequest = FriendRequest.objects.create(
            sender=sender,
            receiver=receiver,
            status=FriendRequest.Status.SENT,
        )

        return friend_request


class AcceptOrRejectFriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id',)

    def update(self, instance: FriendRequest, validated_data: dict):
        request: Request = self.context.get('request')
        if request.user != instance.receiver:
            raise InvalidReceiverException

        status = self.context.get('status')
        if status == 'accept':
            instance.accept()
        elif status == 'reject':
            instance.reject()

        return instance
