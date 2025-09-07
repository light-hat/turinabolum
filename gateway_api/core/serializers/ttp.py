from rest_framework import serializers

from core.models import TTP, CaseTTP


class TTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTP
        fields = [
            "id",
            "technique_id",
            "name",
            "tactic",
            "description",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "created_date", "modified_date"]


class CaseTTPSerializer(serializers.ModelSerializer):
    ttp_details = TTPSerializer(source="ttp", read_only=True)
    detected_by_username = serializers.CharField(
        source="detected_by.username", read_only=True
    )

    class Meta:
        model = CaseTTP
        fields = [
            "id",
            "case",
            "ttp",
            "ttp_details",
            "notes",
            "detected_date",
            "detected_by",
            "detected_by_username",
        ]
        read_only_fields = ["id", "detected_date"]

    def create(self, validated_data):
        """Переопределение создания для установки detected_by"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["detected_by"] = request.user
        return super().create(validated_data)
