from django.urls import include, path
from rest_framework.routers import SimpleRouter
from apis.accounts.views import AuthViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"auth", AuthViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
]
