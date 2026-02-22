from django.urls import include, path
from rest_framework.routers import SimpleRouter
from apis.products.views import ProductViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
