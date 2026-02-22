import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from commons.const.choices import UserRoleChoice
from domains.commons.base_models import BaseDatetimeField
from domains.accounts.models.user_querysets import UserManager


class User(BaseDatetimeField, AbstractBaseUser, PermissionsMixin):
    user_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=UserRoleChoice.choices,
        default=UserRoleChoice.USER,
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_admin(self):
        return self.role == UserRoleChoice.ADMIN
