from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from apis.commons.views import BaseViewSet, serializer_view
from apis.payments.controllers import PaymentController
from apis.payments.serializers import PaymentCreateReqSerializer, ReceiptResSerializer
from apis.payments.filters import ReceiptFilter
from domains.payments.models import Receipt


class PaymentViewSet(BaseViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptResSerializer
    controller_class = PaymentController
    filterset_class = ReceiptFilter
    lookup_field = "receipt_uuid"

    action_permissions = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "cancel": [IsAuthenticated],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.controller_class().list(user=request.user))
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        serializer = ReceiptResSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @serializer_view(res_serializer=ReceiptResSerializer)
    def retrieve(self, request, receipt_uuid=None, *args, **kwargs):
        return self.controller_class().retrieve(receipt_uuid, user=request.user)

    @serializer_view(req_serializer=PaymentCreateReqSerializer, res_serializer=ReceiptResSerializer, status=status.HTTP_201_CREATED)
    def create(self, request, *args, validated_data=None, **kwargs):
        return self.controller_class().create_payment(
            user=request.user,
            items=validated_data["items"],
        )

    @action(detail=True, methods=["post"], url_path="cancel")
    @serializer_view(res_serializer=ReceiptResSerializer)
    def cancel(self, request, receipt_uuid=None, *args, **kwargs):
        instance = self.controller_class().retrieve(receipt_uuid, user=request.user)
        return self.controller_class().cancel_payment(instance)
