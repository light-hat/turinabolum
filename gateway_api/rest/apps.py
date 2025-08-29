"""
REST API interface application.
"""

from django.apps import AppConfig


class RestConfig(AppConfig):
    """
    REST API interface application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "rest"
