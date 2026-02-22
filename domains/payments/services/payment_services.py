from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound
from apis.commons.error_codes import ErrorCode
from commons.const.choices import PaymentStatusChoice
from domains.payments.models import Receipt, ReceiptDetail
from domains.products.models import Product


class PaymentService:

    def get_queryset(self, user=None):
        qs = Receipt.objects.filter_is_deleted(False).select_related_user().prefetch_receipt_details()
        if user:
            qs = qs.filter_user(user)
        return qs

    def retrieve(self, receipt_uuid, user=None) -> Receipt:
        try:
            qs = self.get_queryset(user)
            return qs.get(receipt_uuid=receipt_uuid)
        except Receipt.DoesNotExist:
            raise NotFound(ErrorCode.PAYMENT_NOT_FOUND)

    @transaction.atomic
    def create_payment(self, user, items: list) -> Receipt:
        """
        결제 처리
        items: [{"product_uuid": ..., "quantity": ...}, ...]
        """
        total_amount = 0
        receipt_details_data = []

        for item in items:
            try:
                product = Product.objects.get(product_uuid=item["product_uuid"], is_deleted=False)
            except Product.DoesNotExist:
                raise ValidationError({"product": f"{item['product_uuid']} - {ErrorCode.PRODUCT_NOT_FOUND}"})

            quantity = item["quantity"]
            if product.stock < quantity:
                raise ValidationError({"stock": f"{product.name} 재고가 부족합니다."})

            unit_price = product.price
            subtotal = unit_price * quantity
            total_amount += subtotal

            receipt_details_data.append({
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
            })

            # 재고 차감
            product.stock -= quantity
            product.save()

        receipt = Receipt.objects.create(
            user=user,
            total_amount=total_amount,
            status=PaymentStatusChoice.COMPLETED,
            paid_at=timezone.now(),
        )

        for detail_data in receipt_details_data:
            ReceiptDetail.objects.create(receipt=receipt, **detail_data)

        return Receipt.objects.prefetch_receipt_details().get(pk=receipt.pk)

    def cancel_payment(self, receipt: Receipt) -> Receipt:
        """결제 취소"""
        if receipt.status != PaymentStatusChoice.COMPLETED:
            raise ValidationError({"status": ErrorCode.PAYMENT_ALREADY_COMPLETED})

        with transaction.atomic():
            # 재고 복구
            for detail in receipt.receipt_details.select_related("product"):
                product = detail.product
                product.stock += detail.quantity
                product.save()

            receipt.status = PaymentStatusChoice.CANCELLED
            receipt.save()

        return receipt
