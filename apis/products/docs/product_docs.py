from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.utils.translation import gettext_lazy as _
from apis.products.serializers import ProductResSerializer, ProductCreateReqSerializer, ProductUpdateReqSerializer

DOC_PRODUCT_VIEWSET = extend_schema_view(
    list=extend_schema(
        summary=_("상품 목록"),
        description=_("상품 목록"),
        responses={status.HTTP_200_OK: ProductResSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary=_("상품 상세"),
        description=_("상품 상세"),
        responses={status.HTTP_200_OK: ProductResSerializer},
    ),
    create=extend_schema(
        request=ProductCreateReqSerializer,
        summary=_("상품 생성"),
        description=_("상품 생성"),
        responses={status.HTTP_200_OK: ProductResSerializer},
    ),
    update=extend_schema(
        request=ProductUpdateReqSerializer,
        summary=_("상품 수정"),
        description=_("상품 수정"),
        responses={status.HTTP_200_OK: ProductResSerializer},
    ),
    destroy=extend_schema(
        summary=_("상품 삭제"),
        description=_("상품 삭제"),
        responses={status.HTTP_204_NO_CONTENT: None},
    ),
)