import functools
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status as http_status


class BaseViewSet(GenericViewSet):
    """Base ViewSet with action-based permissions"""

    action_permissions = {}

    def get_permissions(self):
        permissions = self.action_permissions.get(self.action, [])
        return [permission() for permission in permissions]


def serializer_view(req_serializer=None, res_serializer=None, status=http_status.HTTP_200_OK):
    """
    Decorator for ViewSet action methods.

    - req_serializer: Request data를 검증할 serializer 클래스 (없으면 검증 생략)
    - res_serializer: Response data를 직렬화할 serializer 클래스 (없으면 반환값 그대로 사용)
    - status: HTTP 응답 상태 코드 (기본값: 200)

    데코레이팅된 함수는 다음 인자를 받습니다:
      - self, request, *args, **kwargs
      - validated_data (req_serializer가 있을 경우 keyword argument로 전달)

    반환값:
      - res_serializer가 있을 경우 직렬화 후 Response 반환
      - 반환값이 None이면 빈 Response 반환
      - 그 외에는 반환값을 그대로 Response data로 사용
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if req_serializer is not None:
                serializer = req_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                kwargs["validated_data"] = serializer.validated_data

            result = func(self, request, *args, **kwargs)

            if isinstance(result, Response):
                return result

            if result is None:
                return Response(status=status)

            if res_serializer is not None:
                many = isinstance(result, (list, tuple)) or hasattr(result, "__iter__") and not hasattr(result, "pk")
                # QuerySet 등 iterable이지만 단일 객체인 경우를 구분
                if hasattr(result, "model"):  # QuerySet
                    data = res_serializer(result, many=True).data
                elif isinstance(result, (list, tuple)):
                    data = res_serializer(result, many=True).data
                else:
                    data = res_serializer(result).data
                return Response(data, status=status)

            return Response(result, status=status)

        return wrapper
    return decorator
