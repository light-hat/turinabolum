from core.models import CorrelationResult
from rest_framework import serializers


class CorrelationResultSerializer(serializers.ModelSerializer):
    correlation_type_display = serializers.CharField(
        source="get_correlation_type_display", read_only=True
    )
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )
    artifact_name = serializers.CharField(source="artifact.name", read_only=True)
    source_ioc_value = serializers.CharField(
        source="source_ioc.value", read_only=True, allow_null=True
    )
    source_ti_ioc_value = serializers.CharField(
        source="source_ti_ioc.value", read_only=True, allow_null=True
    )
    detected_by_username = serializers.CharField(
        source="detected_by.username", read_only=True, allow_null=True
    )

    class Meta:
        model = CorrelationResult
        fields = [
            "id",
            "artifact",
            "artifact_name",
            "correlation_type",
            "correlation_type_display",
            "source_ioc",
            "source_ioc_value",
            "source_ti_ioc",
            "source_ti_ioc_value",
            "severity",
            "severity_display",
            "confidence",
            "description",
            "detected_date",
            "detected_by",
            "detected_by_username",
            "is_false_positive",
            "false_positive_reason",
        ]
        read_only_fields = ["id", "detected_date"]
