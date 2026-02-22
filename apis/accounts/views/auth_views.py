from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from apis.commons.views import BaseViewSet, serializer_view
from apis.accounts.controllers import AuthController
from apis.accounts.serializers import (
    RegisterReqSerializer,
    LoginReqSerializer,
    LogoutReqSerializer,
    LoginResSerializer,
    UserResSerializer,
)


class AuthViewSet(BaseViewSet):
    controller_class = AuthController

    action_permissions = {
        "register": [AllowAny],
        "login": [AllowAny],
        "logout": [IsAuthenticated],
        "me": [IsAuthenticated],
    }

    @serializer_view(req_serializer=RegisterReqSerializer, res_serializer=UserResSerializer, status=status.HTTP_201_CREATED)
    def register(self, request, *args, validated_data=None, **kwargs):
        return self.controller_class().register(validated_data)

    @serializer_view(req_serializer=LoginReqSerializer, res_serializer=LoginResSerializer)
    def login(self, request, *args, validated_data=None, **kwargs):
        return self.controller_class().login(
            email=validated_data["email"],
            password=validated_data["password"],
        )

    @serializer_view(req_serializer=LogoutReqSerializer, status=status.HTTP_204_NO_CONTENT)
    def logout(self, request, *args, validated_data=None, **kwargs):
        self.controller_class().logout(validated_data["refresh"])

    @serializer_view(res_serializer=UserResSerializer)
    def me(self, request, *args, **kwargs):
        return request.user
