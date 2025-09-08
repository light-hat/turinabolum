from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from djoser.conf import settings as djoser_settings

def get_user_jwt(request):
    """
    Попытка аутентифицировать пользователя через JWT-токен из заголовка Authorization.
    """
    user = get_user(request)
    if user.is_authenticated:
        return user

    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('JWT '):
        return None

    try:
        token = auth_header.split(' ')[1]
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[djoser_settings.TOKEN_ENCODING_ALGORITHM]
        )
        user_id = payload.get('user_id')
        if user_id is not None:
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            return user
    except (IndexError, jwt.InvalidTokenError, User.DoesNotExist) as e:
        from django.core.exceptions import PermissionDenied
        return None

    return None

class DjoserGraphQLAuthMiddleware(MiddlewareMixin):
    """
    Мидлвар, который устанавливает аутентифицированного пользователя
    для запросов к GraphQL на основе JWT-токена Djoser.
    """
    def process_request(self, request):
        if hasattr(request, 'user'):
            request.user = SimpleLazyObject(lambda: get_user_jwt(request))