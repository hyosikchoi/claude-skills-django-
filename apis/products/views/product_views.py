from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from apis.commons.views import BaseViewSet, serializer_view
from apis.commons.base_permissions import IsAdminUser
from apis.products.controllers import ProductController
from apis.products.docs.product_docs import DOC_PRODUCT_VIEWSET
from apis.products.serializers import (
    ProductCreateReqSerializer,
    ProductUpdateReqSerializer,
    ProductResSerializer,
)
from apis.products.filters import ProductFilter
from domains.products.models import Product

@DOC_PRODUCT_VIEWSET
class ProductViewSet(BaseViewSet):
    queryset = Product.objects
    serializer_class = ProductResSerializer
    controller_class = ProductController
    filterset_class = ProductFilter
    lookup_field = "product_uuid"

    action_permissions = {
        "list": [AllowAny],
        "retrieve": [AllowAny],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "destroy": [IsAdminUser],
    }

    @serializer_view(req_serializer=None, res_serializer=ProductResSerializer)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.controller_class().list())
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductResSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @serializer_view(res_serializer=ProductResSerializer)
    def retrieve(self, request, product_uuid=None, *args, **kwargs):
        return self.controller_class().retrieve(product_uuid)

    @serializer_view(req_serializer=ProductCreateReqSerializer, res_serializer=ProductResSerializer, status=status.HTTP_201_CREATED)
    def create(self, request, *args, validated_data=None, **kwargs):
        return self.controller_class().create(validated_data)

    @serializer_view(req_serializer=ProductUpdateReqSerializer, res_serializer=ProductResSerializer)
    def update(self, request, product_uuid=None, *args, validated_data=None, **kwargs):
        instance = self.controller_class().retrieve(product_uuid)
        return self.controller_class().update(instance, validated_data)

    @serializer_view(status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, product_uuid=None, *args, **kwargs) -> str:
        instance = self.controller_class().retrieve(product_uuid)
        self.controller_class().delete(instance)
        return "SUCCESS"