from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)

from .permissions import IsAuthor


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthor,)

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = (IsAuthor,)

    def get_object(self) -> Comment:
        post = get_object_or_404(
            Comment,
            post_id=self.kwargs.get('post_id'),
            id=self.kwargs.get('comment_id'),
        )
        self.check_object_permissions(self.request, post)
        return post

    def get_post(self) -> Post:
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet[Comment]:
        return self.get_post().comments

    def perform_create(self, serializer) -> None:
        serializer.save(post=self.get_post(), author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> BaseManager[Follow]:
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        following_username = self.request.data.get('following')

        try:
            following = User.objects.get(username=following_username)
        except User.DoesNotExist:
            raise ValidationError(
                {'detail': 'User not found'}, code=status.HTTP_400_BAD_REQUEST
            )

        if self.request.user == following:
            raise ValidationError('You cannot follow yourself')

        if Follow.objects.filter(
            user=self.request.user, following=following
        ).exists():
            raise ValidationError(
                'You are already following this user',
                code=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=self.request.user, following=following)
