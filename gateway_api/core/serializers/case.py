from rest_framework import serializers

from core.models import Case

from .incident import IncidentSerializer


class CaseSerializer(serializers.ModelSerializer):
    incident_details = IncidentSerializer(source="incident", read_only=True)
    lead_investigator_username = serializers.CharField(
        source="lead_investigator.username", read_only=True
    )

    class Meta:
        model = Case
        fields = [
            "id",
            "incident",
            "incident_details",
            "title",
            "description",
            "status",
            "lead_investigator",
            "lead_investigator_username",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "created_date", "modified_date"]

    def validate_incident(self, value):
        """Проверка, что инцидент существует и не закрыт"""
        if value.status == "Closed":
            raise serializers.ValidationError(
                "Нельзя создать расследование для закрытого инцидента"
            )
        return value
