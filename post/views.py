from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from post.models import Post
from post.serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action != 'detail':
            return PostListSerializer
        return PostDetailSerializer

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
