from rest_framework import serializers
from domains.products.models import Product
from commons.const.choices import ProductStatusChoice


class ProductCreateReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "status", "image_url"]


class ProductUpdateReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "status", "image_url"]
        extra_kwargs = {field: {"required": False} for field in fields}


class ProductResSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "product_uuid",
            "name",
            "description",
            "price",
            "stock",
            "status",
            "image_url",
            "created_at",
            "updated_at",
        ]
