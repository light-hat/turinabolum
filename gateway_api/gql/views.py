from django.views.decorators.csrf import csrf_exempt
from gql.auth.middleware import DjoserGraphQLAuthMiddleware
from graphene_django.views import GraphQLView


class CustomGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        formatted_error = super().format_error(error)
        formatted_error["code"] = getattr(error, "code", "error")
        return formatted_error

    @classmethod
    def get_context(cls, request):
        context = super().get_context(request)
        context.user = request.user
        return context


graphql_view = csrf_exempt(
    CustomGraphQLView.as_view(graphiql=True, middleware=[DjoserGraphQLAuthMiddleware()])
)
