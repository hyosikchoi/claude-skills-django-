from domains.products.services import ProductService
from domains.products.models import Product


class ProductController:
    service_class = ProductService

    def list(self, filters: dict = None):
        return self.service_class().list(filters)

    def retrieve(self, product_uuid) -> Product:
        return self.service_class().retrieve(product_uuid)

    def create(self, validated_data: dict) -> Product:
        return self.service_class().create(validated_data)

    def update(self, instance: Product, validated_data: dict) -> Product:
        return self.service_class().update(instance, validated_data)

    def delete(self, instance: Product) -> None:
        return self.service_class().soft_delete(instance)
