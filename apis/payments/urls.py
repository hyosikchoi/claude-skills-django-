from django.urls import include, path
from rest_framework.routers import SimpleRouter
from apis.payments.views import PaymentViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
