from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from social.serializers import SendFriendRequestSerializer, AcceptOrRejectFriendRequestSerializer, \
    FriendRequestDetailSerializer
from social.models import FriendRequest


class FriendRequestSendView(CreateAPIView):
    throttle_classes = [UserRateThrottle]
    http_method_names = ['post']
    serializer_class = SendFriendRequestSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        request_data = request.data.copy()
        serializer = SendFriendRequestSerializer(
            data=request_data,
            context={
                'request': request,
            },
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'detail': 'FriendRequest Sent Successfully'},
                status=HTTP_201_CREATED,
            )

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(UpdateAPIView):
    serializer_class = AcceptOrRejectFriendRequestSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['status'] = self.kwargs['status']
        return context

    def get_queryset(self):
        return FriendRequest.objects.filter(status=FriendRequest.Status.SENT)

    def update(self, request: Request, *args, **kwargs) -> Response:
        instance: FriendRequest = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data.copy(),
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        action = f"{self.kwargs['status'].title()}ed"
        return Response(
            data={'detail': f'Friend Request {action} Successfully'},
            status=HTTP_200_OK,
        )


class PendingFriendRequestListView(ListAPIView):
    serializer_class = FriendRequestDetailSerializer

    def get_queryset(self):
        return self.request.user.received_requests.filter(status=FriendRequest.Status.SENT)
