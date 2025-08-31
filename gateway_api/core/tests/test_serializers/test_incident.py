from core.serializers import IncidentSerializer
from django.contrib.auth.models import User
from django.test import TestCase


class IncidentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.incident_data = {
            "title": "Test Incident",
            "description": "This is a test incident",
            "status": "New",
            "severity": "High",
            "classification": "Malware",
            "confidentiality": "Internal",
            "created_by": self.user.id,
        }

    def test_incident_serializer_valid_data(self):
        serializer = IncidentSerializer(data=self.incident_data)
        self.assertTrue(serializer.is_valid())

    def test_incident_serializer_missing_title(self):
        invalid_data = self.incident_data.copy()
        del invalid_data["title"]
        serializer = IncidentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_incident_serializer_invalid_status(self):
        invalid_data = self.incident_data.copy()
        invalid_data["status"] = "InvalidStatus"
        serializer = IncidentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
