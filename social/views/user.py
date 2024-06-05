from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from social.models import FriendRequest
from social.serializers import CreateUserSerializer, LoginUserSerializer, UserDetailSerializer
from social.exceptions import InvalidCredentialsException


# Create your views here.
class UserSignUpView(APIView):
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = []

    def post(self, request: Request, *args, **kwargs) -> Response:
        user_data = request.data.copy()
        serializer = CreateUserSerializer(data=user_data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data.pop('username', email)
            password = serializer.validated_data.pop('password')
            raw_password = make_password(password)
            serializer.save(username=username, password=raw_password, **serializer.validated_data)
            return Response(
                data={'detail': 'user signup successful'},
                status=HTTP_201_CREATED,
            )

        return Response(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = []

    def post(self, request: Request, *args, **kwargs) -> Response:
        login_data = request.data.copy()
        serializer = LoginUserSerializer(data=login_data)
        if serializer.is_valid():
            email, password = serializer.validated_data['email'], serializer.validated_data['password']
            user: User | None = User.objects.filter(email__iexact=email).first()
            if user is None or not user.check_password(password):
                raise InvalidCredentialsException

            token, created = Token.objects.get_or_create(user=user)
            return Response(
                data={
                    'token': token.key,
                    'user': token.user.id,
                    'created': token.created,
                },
                status=HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    pagination_class = UserListPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name')

    def filter_queryset(self, queryset):
        search_by_val = self.request.query_params.get('search')
        if search_by_val is None:
            return super().filter_queryset(queryset).exclude(id__in=[self.request.user.id])

        exact_qs = self.queryset.filter(email__iexact=self.request.query_params['search'])
        if not exact_qs.exists():
            return super().filter_queryset(queryset).exclude(id__in=[self.request.user.id])

        return exact_qs


class UserFriendsListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def filter_queryset(self, queryset):
        sent_accepted_user_ids = self.request.user.sent_requests.filter(
            status=FriendRequest.Status.ACCEPT
        ).values_list("receiver__id", flat=True)
        received_accepted_user_ids = self.request.user.received_requests.filter(
            status=FriendRequest.Status.ACCEPT
        ).values_list("sender__id", flat=True)

        friends_ids = sent_accepted_user_ids.union(received_accepted_user_ids)
        return queryset.filter(id__in=friends_ids)
