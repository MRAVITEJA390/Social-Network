"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter
from social.views import (
    UserSignUpView, UserLoginView, UserListAPIView, UserFriendsListAPIView, PendingFriendRequestListView,
    FriendRequestSendView, AcceptFriendRequestView,
)
from social.converters import StatusConverter

register_converter(StatusConverter, 'status')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/signup/', UserSignUpView.as_view()),
    path('api/v1/login/', UserLoginView.as_view()),
    path('api/v1/users/', UserListAPIView.as_view()),
    path('api/v1/pending_requests/', PendingFriendRequestListView.as_view()),
    path('api/v1/friends/', UserFriendsListAPIView.as_view()),
    path('api/v1/friend_request/send/', FriendRequestSendView.as_view()),
    path('api/v1/friend_request/<status:status>/<int:pk>/', AcceptFriendRequestView.as_view()),
]
