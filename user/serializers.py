from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _


class CustomAuthTokenSerializer(AuthTokenSerializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    username = None

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password", "is_staff"]
        read_only_fields = ["id", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}, "min_length": 8}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source="profile.profile_picture")
    bio = serializers.CharField(source="profile.bio")
    followers_count = serializers.SerializerMethodField(
        method_name="get_followers_count"
    )
    following_count = serializers.SerializerMethodField(
        method_name="get_following_count"
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "profile_picture",
            "first_name",
            "last_name",
            "bio",
            "followers_count",
            "following_count",
        ]

    def get_followers_count(self, obj):
        return obj.profile.get_followers_count()

    def get_following_count(self, obj):
        return obj.profile.get_following_count()


class UserShortInfoSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source="profile.profile_picture")

    class Meta:
        model = get_user_model()
        fields = ["id", "profile_picture", "first_name", "last_name"]


class UserDetailPrivateSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source="profile.sex")
    profile_picture = serializers.ImageField(source="profile.profile_picture")
    bio = serializers.CharField(source="profile.bio")
    followers = UserShortInfoSerializer(
        source="profile.followers", many=True, read_only=True
    )
    following = UserShortInfoSerializer(
        source="profile.followers", many=True, read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "sex",
            "bio",
            "followers",
            "following",
        ]
        read_only_fields = ["id", "followers", "following"]


class UserDetailPublicSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source="profile.sex")
    profile_picture = serializers.ImageField(source="profile.profile_picture")
    bio = serializers.CharField(source="profile.bio")
    followers = UserShortInfoSerializer(
        source="profile.followers", many=True, read_only=True
    )
    following = UserShortInfoSerializer(
        source="profile.followers", many=True, read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "profile_picture",
            "sex",
            "bio",
            "followers",
            "following",
        ]


class LogOutSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
