from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from post.models import Post, PostComment
from post.serializers import PostListSerializer, PostDetailSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = Post.objects.all()

        filter = self.request.GET.get("filter", "all")
        hashtag = self.request.GET.get("hashtag", None)
        user = self.request.user

        if filter == "following" and user.is_authenticated:
            following_users = user.profile.following.all()
            queryset = queryset.filter(user__in=following_users)

        if filter == "mine":
            queryset = queryset.filter(user=user.id)

        if hashtag:
            queryset = queryset.filter(hash_tags__name__iexact=hashtag)

        return queryset

    def get_serializer_class(self):
        if self.action != 'detail':
            return PostListSerializer
        return PostDetailSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def create_comment(self, request, pk=None):
        post = self.get_object()
        user = request.user
        comment_data = request.data.get("comment")

        comment = PostComment.objects.create(user=user, post=post, content=comment_data)

        return Response(
            {
                "message": "Comment created successfully.",
                "comment_id": comment.id
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = self.get_object()

        # Get the authenticated user
        user = request.user

        if user in post.people_who_liked.all():
            # User already liked the post, remove the like
            post.people_who_liked.remove(user)
            message = "Post unliked successfully."
        else:
            # User has not liked the post, add the like
            post.people_who_liked.add(user)
            message = "Post liked successfully."

        return Response({"message": message}, status=status.HTTP_200_OK)
