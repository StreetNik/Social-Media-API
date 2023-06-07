from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

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


class FollowToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(Profile, user_id=pk)

        user_profile = get_object_or_404(Profile, user=request.user)

        user = request.user
        if user in user_to_follow.followers.all():
            print(user_to_follow.followers.count())
            print(user_to_follow.following.count())
            user_to_follow.followers.remove(user)
            user_to_follow.save()
            print(user_to_follow.followers.count())
            print(user_to_follow.following.count())

            user_profile.following.remove(user_to_follow.user)
            user_profile.save()

            return Response(
                {"message": "User unfollowed successfully"}, status=status.HTTP_200_OK
            )

        user_to_follow.followers.add(user_profile.user)
        user_profile.save()

        return Response(
            {"message": "User followed successfully"}, status=status.HTTP_200_OK
        )


# class FollowToggleAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, pk):
#         user_to_follow = get_object_or_404(Profile, id=pk)
#
#         user = request.user
#
#         if user in user_to_follow.followers.all():
#             user_to_follow.followers.remove(user)
#             user_to_follow.save()
#             return Response(
#                 {"message": "User unfollowed successfully"}, status=status.HTTP_200_OK
#             )
#         else:
#             user_to_follow.followers.add(user)
#             user_to_follow.save()
#             return Response(
#                 {"message": "User followed successfully"}, status=status.HTTP_200_OK
#             )
