from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from apis.commons.error_codes import ErrorCode
from domains.accounts.models import User


class AuthService:

    def register(self, validated_data: dict) -> User:
        """회원가입"""
        email = validated_data.get("email")
        if User.objects.filter(email=email, is_deleted=False).exists():
            raise ValidationError({"email": ErrorCode.EMAIL_ALREADY_EXISTS})

        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)

    def login(self, email: str, password: str) -> dict:
        """로그인 - JWT 토큰 반환"""
        try:
            user = User.objects.get(email=email, is_deleted=False)
        except User.DoesNotExist:
            raise AuthenticationFailed(ErrorCode.USER_NOT_FOUND)

        if not user.check_password(password):
            raise AuthenticationFailed(ErrorCode.INVALID_PASSWORD)

        if not user.is_active:
            raise AuthenticationFailed("비활성화된 계정입니다.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }

    def logout(self, refresh_token: str) -> None:
        """로그아웃 - 리프레시 토큰 블랙리스트"""
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise ValidationError({"refresh": ErrorCode.INVALID_TOKEN})

    def get_user_by_uuid(self, user_uuid) -> User:
        try:
            return User.objects.get(user_uuid=user_uuid, is_deleted=False)
        except User.DoesNotExist:
            raise ValidationError({"user": ErrorCode.USER_NOT_FOUND})
