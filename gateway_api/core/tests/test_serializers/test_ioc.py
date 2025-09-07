from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Case, Incident
from core.serializers import IOCSerializer


class IOCSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.incident = Incident.objects.create(
            title="Test Incident",
            description="This is a test incident",
            status="New",
            severity="High",
            classification="Malware",
            confidentiality="Internal",
            created_by=self.user,
        )
        self.case = Case.objects.create(
            incident=self.incident,
            title="Test Case",
            description="This is a test case",
            status="Active",
            lead_investigator=self.user,
        )
        self.ioc_data = {
            "case": self.case.id,
            "type": "Hash",
            "value": "d41d8cd98f00b204e9800998ecf8427e",
            "tlp": "WHITE",
            "confidence": "High",
        }

    def test_ioc_serializer_valid_data(self):
        serializer = IOCSerializer(data=self.ioc_data)
        self.assertTrue(serializer.is_valid())

    def test_ioc_serializer_invalid_hash_length(self):
        invalid_data = self.ioc_data.copy()
        invalid_data["value"] = "invalidhash"
        serializer = IOCSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
