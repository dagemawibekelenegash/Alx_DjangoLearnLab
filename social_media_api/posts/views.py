from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"detail": "You do not have permission to edit this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.request.data.get("post"))
        serializer.save(author=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        followed_users = self.request.user.following.all()
        return Post.objects.filter(author__in=followed_users).order_by("-created_at")


# Post.objects.filter(author__in=following_users).order_by


class LikePostView(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.create(user=request.user, post=post)

        notification = Notification(
            recipient=post.user,
            actor=request.user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id,
        )
        notification.save()

        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_200_OK
        )


class UnlikePostView(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()

        return Response(
            {"detail": "Post unliked successfully."}, status=status.HTTP_200_OK
        )


# generics.get_object_or_404(Post, pk=pk)", "Like.objects.get_or_create(user=request.user, post=post)", "Notification.objects.create
