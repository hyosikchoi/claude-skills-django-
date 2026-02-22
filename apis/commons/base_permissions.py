from rest_framework.permissions import BasePermission
from commons.const.choices import UserRoleChoice


class IsAdminUser(BasePermission):
    """관리자만 접근 가능"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoleChoice.ADMIN)


class IsAuthenticatedUser(BasePermission):
    """로그인한 사용자만 접근 가능"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
