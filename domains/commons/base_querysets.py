from django.db import models


class BaseQuerySet(models.QuerySet):
    def filter_is_deleted(self, is_deleted=False):
        return self.filter(is_deleted=is_deleted)


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
