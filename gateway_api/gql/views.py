from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from gql.middleware import DjoserGraphQLAuthMiddleware
from django.conf.settings import DEBUG

class CustomGraphQLView(GraphQLView):
    """
    Кастомная GraphQLView, которая добавляет пользователя в контекст
    и использует наш мидлвар для аутентификации.
    """

    @classmethod
    def get_context(cls, request):
        context = super().get_context(request)
        context.user = request.user
        return context

graphql_view = csrf_exempt(
    CustomGraphQLView.as_view(
        graphiql=DEBUG,
        middleware=[DjoserGraphQLAuthMiddleware()]
    )
)