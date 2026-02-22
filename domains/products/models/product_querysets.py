from django.db import models


class ProductQuerySet(models.QuerySet):
    def filter_product_uuid(self, product_uuid):
        return self.filter(product_uuid=product_uuid)

    def filter_status(self, status):
        return self.filter(status=status)

    def filter_is_deleted(self, is_deleted=False):
        return self.filter(is_deleted=is_deleted)

    def filter_name_contains(self, name):
        return self.filter(name__icontains=name)

    def filter_price_range(self, min_price=None, max_price=None):
        qs = self
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        return qs


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    pass
