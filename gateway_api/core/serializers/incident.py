from core.models import Incident
from django.contrib.auth.models import User
from rest_framework import serializers


class IncidentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    assigned_to_username = serializers.CharField(
        source="assigned_to.username", read_only=True, allow_null=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )
    classification_display = serializers.CharField(
        source="get_classification_display", read_only=True
    )

    class Meta:
        model = Incident
        fields = [
            "id",
            "title",
            "description",
            "status",
            "status_display",
            "severity",
            "severity_display",
            "classification",
            "classification_display",
            "confidentiality",
            "created_date",
            "modified_date",
            "closed_date",
            "created_by",
            "created_by_username",
            "assigned_to",
            "assigned_to_username",
        ]
        read_only_fields = ["id", "created_date", "modified_date", "created_by"]

    def validate_assigned_to(self, value):
        """Проверка, что назначаемый пользователь существует и активен"""
        if value and not value.is_active:
            raise serializers.ValidationError(
                "Нельзя назначить неактивного пользователя"
            )
        return value

    def create(self, validated_data):
        """Переопределение создания для установки created_by"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        return super().create(validated_data)
