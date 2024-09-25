from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from app.consumers import MyGraphQLConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path('ws/graphql/', MyGraphQLConsumer.as_asgi()),
    ]),
})
