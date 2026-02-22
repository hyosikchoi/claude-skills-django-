from django.db import models


class UserQuerySet(models.QuerySet):
    def filter_user_uuid(self, user_uuid):
        return self.filter(user_uuid=user_uuid)

    def filter_email(self, email):
        return self.filter(email=email)

    def filter_role(self, role):
        return self.filter(role=role)

    def filter_is_deleted(self, is_deleted=False):
        return self.filter(is_deleted=is_deleted)


class UserManager(models.Manager.from_queryset(UserQuerySet)):
    pass
