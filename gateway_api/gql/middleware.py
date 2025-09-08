# graphql_auth/middleware.py
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from djoser.conf import settings as djoser_settings


def get_user_jwt(request):
    user = get_user(request)
    if user.is_authenticated:
        return user
    try:
        # Извлекаем токен из заголовка Authorization: JWT <token>
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("JWT "):
            return None

        token = auth_header.split(" ")[1]
        # Декодируем токен, используя настройки SECRET_KEY Django
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[djoser_settings.TOKEN_ENCODING_ALGORITHM],
        )
        # Извлекаем идентификатор пользователя из полезной нагрузки токена
        user_id = payload.get("user_id")
        if user_id:
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            return user
    except (jwt.InvalidTokenError, User.DoesNotExist, IndexError):
        pass
    return None


class DjoserGraphQLAuthMiddleware(MiddlewareMixin):
    """Мидлвар для аутентификации пользователей через Djoser JWT в GraphQL."""

    def process_request(self, request):
        if hasattr(request, "user"):
            request.user = SimpleLazyObject(lambda: get_user_jwt(request))
