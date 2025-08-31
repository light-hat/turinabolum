import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Set up logger
logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def jwt_create(request):
    """Custom JWT token creation that sets refresh token as HttpOnly cookie."""
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"success": False, "error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate user
        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"success": False, "error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Create response with access token
        response = Response(
            {
                "success": True,
                "access": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "date_joined": user.date_joined,
                    "last_login": user.last_login,
                },
            },
            status=status.HTTP_200_OK,
        )

        # Set refresh token as HttpOnly cookie
        response.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            httponly=True,
            secure=True,
            samesite="Lax",
            path=settings.SIMPLE_JWT.get("REFRESH_TOKEN_COOKIE_PATH", "/"),
        )

        logger.info(f"User {username} logged in successfully")

        return response

    except Exception as e:
        logger.error("Failed to create JWT tokens", exc_info=True)
        return Response(
            {"success": False, "error": "An unexpected error occurred during login"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def jwt_refresh(request):
    """Custom JWT token refresh that uses HttpOnly cookie."""
    try:
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"success": False, "error": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Validate and refresh token
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception as token_error:
            logger.warning(f"Invalid refresh token: {token_error}")
            return Response(
                {"success": False, "error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Create response with new access token
        response = Response(
            {"success": True, "access": access_token}, status=status.HTTP_200_OK
        )

        # Set new refresh token as HttpOnly cookie (if rotation is enabled)
        if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS", False):
            try:
                new_refresh = RefreshToken.for_user(refresh.user)
                new_refresh_token = str(new_refresh)

                response.set_cookie(
                    "refresh_token",
                    new_refresh_token,
                    max_age=settings.SIMPLE_JWT[
                        "REFRESH_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    path=settings.SIMPLE_JWT.get("REFRESH_TOKEN_COOKIE_PATH", "/"),
                )
            except Exception as rotation_error:
                logger.warning(f"Failed to rotate refresh token: {rotation_error}")

        return response

    except Exception as e:
        logger.error("Failed to refresh JWT token", exc_info=True)
        return Response(
            {
                "success": False,
                "error": "An unexpected error occurred during token refresh",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def jwt_logout(request):
    """Logout endpoint that blacklists the current JWT token."""
    try:
        # Get the refresh token from the request cookies
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(
                    f"User {request.user.username} logged out successfully - token blacklisted"
                )
            except Exception as token_error:
                logger.warning(
                    f"Failed to blacklist token for user {request.user.username}: {token_error}"
                )
        else:
            logger.info(
                f"User {request.user.username} logged out - no refresh token found in cookies"
            )

        # Create response with cookie deletion
        response = Response(
            {"success": True, "message": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )

        # Delete the refresh token cookie
        response.delete_cookie("refresh_token")

        return response

    except Exception as e:
        logger.error("Failed to logout user", exc_info=True)
        return Response(
            {"success": False, "error": "An unexpected error occurred during logout"},
            status=status.HTTP_400_BAD_REQUEST,
        )
