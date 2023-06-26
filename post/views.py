from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.serializers import PostListSerializer, PostDetailSerializer


class PostListViewSet(ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PostDetailSerializer

    def get_object(self):
        post = Post.objects.get(pk=self.kwargs["pk"])
        return post
