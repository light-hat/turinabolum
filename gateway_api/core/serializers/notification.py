from rest_framework import serializers

from core.models import Notification, UserNotification


class NotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(
        source="get_notification_type_display", read_only=True
    )
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "notification_type_display",
            "severity",
            "severity_display",
            "created_date",
            "is_read",
            "read_date",
            "related_object_id",
            "related_content_type",
        ]
        read_only_fields = ["id", "created_date"]


class UserNotificationSerializer(serializers.ModelSerializer):
    notification_details = NotificationSerializer(source="notification", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserNotification
        fields = [
            "id",
            "user",
            "user_username",
            "notification",
            "notification_details",
            "is_read",
            "read_date",
        ]
        read_only_fields = ["id", "read_date"]
