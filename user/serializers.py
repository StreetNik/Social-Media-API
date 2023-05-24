from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _


class CustomAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField(label=_("Email"), write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
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
