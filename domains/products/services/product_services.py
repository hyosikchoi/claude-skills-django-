from rest_framework.exceptions import ValidationError, NotFound
from apis.commons.error_codes import ErrorCode
from domains.products.models import Product
from commons.const.choices import ProductStatusChoice


class ProductService:

    def get_queryset(self):
        return Product.objects.filter_is_deleted(False)

    def list(self, filters: dict = None) -> "QuerySet":
        qs = self.get_queryset()
        if filters:
            if name := filters.get("name"):
                qs = qs.filter_name_contains(name)
            if status := filters.get("status"):
                qs = qs.filter_status(status)
            if min_price := filters.get("min_price"):
                qs = qs.filter_price_range(min_price=min_price)
            if max_price := filters.get("max_price"):
                qs = qs.filter_price_range(max_price=max_price)
        return qs

    def retrieve(self, product_uuid) -> Product:
        try:
            return self.get_queryset().get(product_uuid=product_uuid)
        except Product.DoesNotExist:
            raise NotFound(ErrorCode.PRODUCT_NOT_FOUND)

    def create(self, validated_data: dict) -> Product:
        return Product.objects.create(**validated_data)

    def update(self, instance: Product, validated_data: dict) -> Product:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def soft_delete(self, instance: Product) -> None:
        instance.is_deleted = True
        instance.save()
