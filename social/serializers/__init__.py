from .user import CreateUserSerializer, LoginUserSerializer, UserDetailSerializer
from .friend_request import SendFriendRequestSerializer, AcceptOrRejectFriendRequestSerializer, FriendRequestDetailSerializer

__all__ = [
    'CreateUserSerializer', 'LoginUserSerializer', 'UserDetailSerializer', 'SendFriendRequestSerializer',
    'AcceptOrRejectFriendRequestSerializer', 'FriendRequestDetailSerializer'
]
