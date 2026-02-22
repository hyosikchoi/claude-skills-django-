from django.db import models


class UserRoleChoice(models.TextChoices):
    ADMIN = "ADMIN", "관리자"
    USER = "USER", "일반 유저"


class ProductStatusChoice(models.TextChoices):
    ACTIVE = "ACTIVE", "판매중"
    INACTIVE = "INACTIVE", "판매중지"
    SOLD_OUT = "SOLD_OUT", "품절"


class PaymentStatusChoice(models.TextChoices):
    PENDING = "PENDING", "결제 대기"
    COMPLETED = "COMPLETED", "결제 완료"
    CANCELLED = "CANCELLED", "결제 취소"
    REFUNDED = "REFUNDED", "환불"
