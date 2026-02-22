import uuid
from django.db import models
from commons.const.choices import ProductStatusChoice
from domains.commons.base_models import BaseDatetimeField
from domains.products.models.product_querysets import ProductManager


class Product(BaseDatetimeField, models.Model):
    product_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=ProductStatusChoice.choices,
        default=ProductStatusChoice.ACTIVE,
    )
    image_url = models.URLField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = ProductManager()

    class Meta:
        db_table = "product"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
