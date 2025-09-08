import graphene
from django.urls import path
from graphene_django.views import GraphQLView
from graphql_auth.middleware import DjoserGraphQLAuthMiddleware


class CustomGraphQLView(GraphQLView):
    """Custom GraphQLView with Djoser auth."""

    @classmethod
    def get_context(cls, request):
        context = super().get_context(request)
        context.user = request.user
        return context
