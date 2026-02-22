from django_filters import rest_framework as filters
from domains.products.models import Product
from commons.const.choices import ProductStatusChoice


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = filters.ChoiceFilter(choices=ProductStatusChoice.choices)
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["name", "status", "min_price", "max_price"]
