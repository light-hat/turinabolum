from core.models import DumpUpload
from rest_framework import serializers


class DumpUploadSerializer(serializers.ModelSerializer):
    dump_type_display = serializers.CharField(
        source="get_dump_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    uploaded_by_username = serializers.CharField(
        source="uploaded_by.username", read_only=True
    )

    class Meta:
        model = DumpUpload
        fields = [
            "id",
            "upload_date",
            "dump_type",
            "dump_type_display",
            "original_filename",
            "dump_file",
            "uploaded_by",
            "uploaded_by_username",
            "status",
            "status_display",
            "file_size",
            "md5_hash",
            "sha1_hash",
            "sha256_hash",
            "processing_log",
            "analysis_results",
            "kafka_message_id",
        ]
        read_only_fields = [
            "id",
            "upload_date",
            "file_size",
            "md5_hash",
            "sha1_hash",
            "sha256_hash",
            "processing_log",
            "analysis_results",
            "kafka_message_id",
        ]

    def create(self, validated_data):
        """Переопределение создания для установки uploaded_by и расчета хешей"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["uploaded_by"] = request.user

        instance = super().create(validated_data)

        # Здесь можно добавить логику расчета хешей и размера файла
        # Например, с использованием Celery задачи

        return instance
