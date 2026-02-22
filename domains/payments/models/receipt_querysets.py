from django.db import models


class ReceiptQuerySet(models.QuerySet):
    def filter_receipt_uuid(self, receipt_uuid):
        return self.filter(receipt_uuid=receipt_uuid)

    def filter_user(self, user):
        return self.filter(user=user)

    def filter_status(self, status):
        return self.filter(status=status)

    def filter_is_deleted(self, is_deleted=False):
        return self.filter(is_deleted=is_deleted)

    def select_related_user(self):
        return self.select_related("user")

    def prefetch_receipt_details(self):
        return self.prefetch_related("receipt_details")


class ReceiptManager(models.Manager.from_queryset(ReceiptQuerySet)):
    pass


class ReceiptDetailQuerySet(models.QuerySet):
    def filter_receipt(self, receipt):
        return self.filter(receipt=receipt)

    def select_related_product(self):
        return self.select_related("product")


class ReceiptDetailManager(models.Manager.from_queryset(ReceiptDetailQuerySet)):
    pass
