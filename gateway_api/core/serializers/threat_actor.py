from core.models import IncidentThreatActor, ThreatActor
from rest_framework import serializers


class ThreatActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatActor
        fields = [
            "id",
            "name",
            "description",
            "aliases",
            "origin",
            "target_sectors",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "created_date", "modified_date"]


class IncidentThreatActorSerializer(serializers.ModelSerializer):
    threat_actor_details = ThreatActorSerializer(source="threat_actor", read_only=True)
    confidence_display = serializers.CharField(
        source="get_confidence_display", read_only=True
    )

    class Meta:
        model = IncidentThreatActor
        fields = [
            "id",
            "incident",
            "threat_actor",
            "threat_actor_details",
            "confidence",
            "confidence_display",
            "evidence",
            "created_date",
        ]
        read_only_fields = ["id", "created_date"]
