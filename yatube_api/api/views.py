# TODO:  Напишите свой вариант
from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        new_queryset = post.comments.all()
        return new_queryset

class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Follow."""
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        posts = Post.objects.filter(author__following__user=self.request.user)
        new_queryset = posts
        return new_queryset