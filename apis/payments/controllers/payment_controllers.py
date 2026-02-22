from domains.payments.services import PaymentService
from domains.payments.models import Receipt


class PaymentController:
    service_class = PaymentService

    def list(self, user):
        return self.service_class().get_queryset(user)

    def retrieve(self, receipt_uuid, user) -> Receipt:
        return self.service_class().retrieve(receipt_uuid, user)

    def create_payment(self, user, items: list) -> Receipt:
        return self.service_class().create_payment(user, items)

    def cancel_payment(self, receipt: Receipt) -> Receipt:
        return self.service_class().cancel_payment(receipt)
