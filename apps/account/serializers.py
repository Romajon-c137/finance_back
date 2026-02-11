from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            # Аутентификация пользователя
            user = authenticate(
                request=self.context.get("request"),
                username=username,  # Используем username
                password=password,
            )

            if not user:
                msg = _("Unable to log in with the provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        # Проверка успешной аутентификации
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """
        Генерация токена после успешной аутентификации.
        """
        user = validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return {"token": token.key}