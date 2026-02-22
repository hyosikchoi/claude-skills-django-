from domains.accounts.services import AuthService
from domains.accounts.models import User


class AuthController:
    service_class = AuthService

    def register(self, validated_data: dict) -> User:
        return self.service_class().register(validated_data)

    def login(self, email: str, password: str) -> dict:
        return self.service_class().login(email, password)

    def logout(self, refresh_token: str) -> None:
        return self.service_class().logout(refresh_token)
