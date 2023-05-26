from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.models import User
from user.serializers import (
    UserSerializer,
    CustomAuthTokenSerializer,
    LogOutSerializer,
    UserDetailSerializer,
)


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustomAuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LogOutView(generics.RetrieveAPIView):
    serializer_class = LogOutSerializer
    permission_classes = [IsAuthenticated]

    def get_user(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_user()
        user.auth_token.delete()
        return Response("Successfully logged out")

    def retrieve(self, request, *args, **kwargs):
        user = self.get_user()
        serializer = LogOutSerializer(user)
        return Response(serializer.data)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["profile"] = self.request.user.profile
        return context
