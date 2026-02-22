import uuid
from django.db import models
from commons.const.choices import PaymentStatusChoice
from domains.commons.base_models import BaseDatetimeField
from domains.payments.models.receipt_querysets import ReceiptManager, ReceiptDetailManager


class Receipt(BaseDatetimeField, models.Model):
    """결제 영수증"""
    receipt_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "domain_accounts.User",
        on_delete=models.PROTECT,
        related_name="receipts",
    )
    total_amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.PENDING,
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = ReceiptManager()

    class Meta:
        db_table = "receipt"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Receipt({self.receipt_uuid}) - {self.user.email}"


class ReceiptDetail(BaseDatetimeField, models.Model):
    """결제 영수증 상세 (구매 상품 내역)"""
    receipt_detail_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="receipt_details",
    )
    product = models.ForeignKey(
        "domain_products.Product",
        on_delete=models.PROTECT,
        related_name="receipt_details",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)  # 구매 시점 가격
    subtotal = models.DecimalField(max_digits=14, decimal_places=2)    # quantity * unit_price

    objects = ReceiptDetailManager()

    class Meta:
        db_table = "receipt_detail"
        ordering = ["-created_at"]

    def __str__(self):
        return f"ReceiptDetail({self.receipt_detail_uuid}) - {self.product.name} x{self.quantity}"
