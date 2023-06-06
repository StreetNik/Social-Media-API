from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.models import User, Profile
from user.serializers import (
    UserSerializer,
    CustomAuthTokenSerializer,
    LogOutSerializer,
    UserDetailPrivateSerializer,
    UserListSerializer,
    UserDetailPublicSerializer,
)


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustomAuthTokenSerializer


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


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        user_profile = Profile.objects.create(user=user)
        user_profile.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = get_user_model().objects.all()


class UserPrivateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailPrivateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["profile"] = self.request.user.profile
        return context


class UserPublicProfileView(generics.RetrieveAPIView):
    serializer_class = UserDetailPublicSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["profile"] = self.get_object().profile
        return context
