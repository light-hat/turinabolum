from core.models import Artifact, ArtifactTag
from rest_framework import serializers

from .evidence import EvidenceSourceSerializer


class ArtifactSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    source_details = EvidenceSourceSerializer(source="source", read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Artifact
        fields = [
            "id",
            "source",
            "source_details",
            "type",
            "type_display",
            "name",
            "path",
            "size",
            "created_date",
            "modified_date",
            "accessed_date",
            "hash_md5",
            "hash_sha1",
            "hash_sha256",
            "is_suspicious",
            "raw_data_reference",
            "tags",
        ]
        read_only_fields = ["id"]

    def get_tags(self, obj):
        """Получение тегов артефакта"""
        return [tag.name for tag in obj.artifacttag_set.all()]


class ArtifactTagSerializer(serializers.ModelSerializer):
    artifact_name = serializers.CharField(source="artifact.name", read_only=True)
    tag_name = serializers.CharField(source="tag.name", read_only=True)
    added_by_username = serializers.CharField(
        source="added_by.username", read_only=True
    )

    class Meta:
        model = ArtifactTag
        fields = [
            "id",
            "artifact",
            "artifact_name",
            "tag",
            "tag_name",
            "added_by",
            "added_by_username",
            "added_date",
        ]
        read_only_fields = ["id", "added_date"]

    def create(self, validated_data):
        """Переопределение создания для установки added_by"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["added_by"] = request.user
        return super().create(validated_data)
