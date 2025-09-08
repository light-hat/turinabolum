from core.models import ThreatIntelFeed, ThreatIntelIOC
from rest_framework import serializers


class ThreatIntelFeedSerializer(serializers.ModelSerializer):
    feed_type_display = serializers.CharField(
        source="get_feed_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ThreatIntelFeed
        fields = [
            "id",
            "name",
            "description",
            "feed_type",
            "feed_type_display",
            "url",
            "api_key",
            "collection_name",
            "polling_interval",
            "status",
            "status_display",
            "last_successful_poll",
            "last_error",
            "created_date",
            "modified_date",
        ]
        read_only_fields = [
            "id",
            "last_successful_poll",
            "last_error",
            "created_date",
            "modified_date",
        ]


class ThreatIntelIOCSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    tlp_display = serializers.CharField(source="get_tlp_display", read_only=True)
    confidence_display = serializers.CharField(
        source="get_confidence_display", read_only=True
    )
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )
    feed_name = serializers.CharField(source="feed.name", read_only=True)

    class Meta:
        model = ThreatIntelIOC
        fields = [
            "id",
            "feed",
            "feed_name",
            "type",
            "type_display",
            "value",
            "description",
            "first_seen",
            "last_seen",
            "confidence",
            "confidence_display",
            "severity",
            "severity_display",
            "tlp",
            "tlp_display",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["id", "created_date", "modified_date"]
