from core.models import EvidenceSource
from rest_framework import serializers


class EvidenceSourceSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    case_title = serializers.CharField(source="case.title", read_only=True)

    class Meta:
        model = EvidenceSource
        fields = [
            "id",
            "case",
            "case_title",
            "type",
            "type_display",
            "name",
            "description",
            "hash_md5",
            "hash_sha1",
            "hash_sha256",
            "acquisition_date",
            "acquisition_tool",
            "custodian",
            "storage_location",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        """Проверка, что хотя бы один хеш предоставлен"""
        if not any(
            [data.get("hash_md5"), data.get("hash_sha1"), data.get("hash_sha256")]
        ):
            raise serializers.ValidationError(
                "Должен быть предоставлен хотя бы один хеш (MD5, SHA-1 или SHA-256)"
            )
        return data
