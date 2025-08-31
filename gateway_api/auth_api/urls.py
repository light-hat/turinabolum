from django.urls import include, path

from . import views

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/jwt/create/", views.jwt_create, name="jwt-create"),
    path("auth/jwt/refresh/", views.jwt_refresh, name="jwt-refresh"),
    path("auth/jwt/logout/", views.jwt_logout, name="jwt-logout"),
]
