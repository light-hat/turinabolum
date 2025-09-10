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
