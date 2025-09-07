from rest_framework import serializers

from core.models import IOC


class IOCSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    tlp_display = serializers.CharField(source="get_tlp_display", read_only=True)
    confidence_display = serializers.CharField(
        source="get_confidence_display", read_only=True
    )
    case_title = serializers.CharField(source="case.title", read_only=True)

    class Meta:
        model = IOC
        fields = [
            "id",
            "case",
            "case_title",
            "type",
            "type_display",
            "value",
            "description",
            "first_seen",
            "last_seen",
            "tlp",
            "tlp_display",
            "confidence",
            "confidence_display",
            "created_date",
        ]
        read_only_fields = ["id", "created_date"]

    def validate(self, data):
        """Валидация значения IOC в зависимости от типа"""
        ioc_type = data.get("type")
        value = data.get("value")

        if ioc_type == "Hash":
            if len(value) not in [32, 40, 64]:
                raise serializers.ValidationError(
                    "Хеш должен быть длиной 32 (MD5), 40 (SHA-1) или 64 (SHA-256) символа"
                )
        elif ioc_type == "IP Address":
            # Простая проверка на IP адрес (можно расширить)
            if not value.replace(".", "").isdigit():
                raise serializers.ValidationError("Неверный формат IP адреса")
        elif ioc_type == "Domain":
            if not value.replace(".", "").replace("-", "").isalnum():
                raise serializers.ValidationError("Неверный формат домена")
        elif ioc_type == "URL":
            if not value.startswith(("http://", "https://")):
                raise serializers.ValidationError(
                    "URL должен начинаться с http:// или https://"
                )
        elif ioc_type == "Email":
            if "@" not in value:
                raise serializers.ValidationError("Неверный формат email")

        return data
