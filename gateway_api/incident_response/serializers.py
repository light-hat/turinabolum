from incident_response.models import Case
from rest_framework import serializers


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "id",
            "title",
            "description",
            "status",
            "severity",
            "classification",
            "tlp",
            "created_date",
            "modified_date",
            "closed_date",
            "created_by",
        ]
        read_only_fields = ["id", "created_date", "modified_date"]

    def validate_incident(self, value):
        """Проверка, что инцидент существует и не закрыт"""
        if value.status == "Closed":
            raise serializers.ValidationError(
                "Нельзя создать расследование для закрытого инцидента"
            )
        return value
