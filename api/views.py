from imageboard.models import Board, Thread, UserPost
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from api.serializers import BoardSerializer, ThreadSerializer, UserPostSerializer
from api.utils import PostPermission

class BoardViewListSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'slug'


class ThreadViewListSet(viewsets.ModelViewSet):
    permission_classes = (PostPermission,)
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    lookup_field = 'thread_number'

class UserPostViewListSet(viewsets.ModelViewSet):
    permission_classes = (PostPermission,)
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
    lookup_field = 'post_number'


