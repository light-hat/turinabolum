from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Notification, UserNotification


class NotificationModelTest(TestCase):
    def setUp(self):
        self.notification_data = {
            "title": "Test Notification",
            "message": "This is a test notification",
            "notification_type": "System",
            "severity": "Info",
        }

    def test_create_notification(self):
        notification = Notification.objects.create(**self.notification_data)
        self.assertEqual(notification.title, "Test Notification")
        self.assertEqual(notification.message, "This is a test notification")
        self.assertEqual(notification.notification_type, "System")
        self.assertEqual(notification.severity, "Info")

    def test_notification_str_representation(self):
        notification = Notification.objects.create(**self.notification_data)
        expected_str = f"{notification.notification_type}: {notification.title}"
        self.assertEqual(str(notification), expected_str)


class UserNotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.notification = Notification.objects.create(
            title="Test Notification",
            message="This is a test notification",
            notification_type="System",
            severity="Info",
        )
        self.user_notification_data = {
            "user": self.user,
            "notification": self.notification,
        }

    def test_create_user_notification(self):
        user_notification = UserNotification.objects.create(
            **self.user_notification_data
        )
        self.assertEqual(user_notification.user, self.user)
        self.assertEqual(user_notification.notification, self.notification)
        self.assertFalse(user_notification.is_read)

    def test_user_notification_str_representation(self):
        user_notification = UserNotification.objects.create(
            **self.user_notification_data
        )
        expected_str = f"{user_notification.user} - {user_notification.notification}"
        self.assertEqual(str(user_notification), expected_str)
