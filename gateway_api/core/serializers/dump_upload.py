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
    file_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = DumpUpload
        fields = [
            "id",
            "upload_date",
            "dump_type",
            "dump_type_display",
            "original_filename",
            "dump_file",
            "file_url",
            "uploaded_by",
            "uploaded_by_username",
            "status",
            "status_display",
            "file_size",
            "file_size_display",
            "md5_hash",
            "sha1_hash",
            "sha256_hash",
            "processing_log",
            "analysis_results",
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
        ]

    def get_file_url(self, obj):
        """Get the URL for accessing the uploaded file."""
        return obj.get_file_url()

    def get_file_size_display(self, obj):
        """Get human-readable file size."""
        if not obj.file_size:
            return "Unknown"

        # Convert bytes to human readable format
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def create(self, validated_data):
        """Переопределение создания для установки uploaded_by и расчета хешей"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["uploaded_by"] = request.user

        instance = super().create(validated_data)

        # Хеши и размер файла будут рассчитаны автоматически в методе save() модели
        # Здесь можно добавить дополнительную логику, например, отправку в Kafka

        return instance
