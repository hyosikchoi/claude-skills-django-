from rest_framework import serializers
from domains.payments.models import Receipt, ReceiptDetail


class PaymentItemSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class PaymentCreateReqSerializer(serializers.Serializer):
    items = PaymentItemSerializer(many=True, min_length=1)


class ReceiptDetailResSerializer(serializers.ModelSerializer):
    product_uuid = serializers.UUIDField(source="product.product_uuid")
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = ReceiptDetail
        fields = [
            "receipt_detail_uuid",
            "product_uuid",
            "product_name",
            "quantity",
            "unit_price",
            "subtotal",
        ]


class ReceiptResSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email")
    receipt_details = ReceiptDetailResSerializer(many=True)

    class Meta:
        model = Receipt
        fields = [
            "receipt_uuid",
            "user_email",
            "total_amount",
            "status",
            "paid_at",
            "receipt_details",
            "created_at",
            "updated_at",
        ]
