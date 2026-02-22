from rest_framework import serializers
from domains.accounts.models import User
from commons.const.choices import UserRoleChoice


class RegisterReqSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)


class LoginReqSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutReqSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserResSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_uuid",
            "email",
            "name",
            "phone",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        ]


class LoginResSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserResSerializer()
