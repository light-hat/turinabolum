from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from djoser.conf import settings as djoser_settings


def get_user_jwt(request) -> Optional[get_user_model()]:
    user = get_user(request)
    if user.is_authenticated:
        return user
    try:
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("JWT "):
            return None

        token = auth_header.split(" ")[1]
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[djoser_settings.TOKEN_ENCODING_ALGORITHM],
        )
        user_id = payload.get("user_id")
        if user_id is not None:
            User = get_user_model()
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None
    except (jwt.InvalidTokenError, IndexError, ValueError) as e:
        pass
    return None


class DjoserGraphQLAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, "user"):
            request.user = SimpleLazyObject(lambda: get_user_jwt(request))
