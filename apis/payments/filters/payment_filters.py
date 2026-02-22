from django_filters import rest_framework as filters
from domains.payments.models import Receipt
from commons.const.choices import PaymentStatusChoice


class ReceiptFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=PaymentStatusChoice.choices)

    class Meta:
        model = Receipt
        fields = ["status"]
