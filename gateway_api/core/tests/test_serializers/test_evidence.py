from core.models import Case, Incident
from core.serializers import EvidenceSourceSerializer
from django.contrib.auth.models import User
from django.test import TestCase


class EvidenceSourceSerializerTest(TestCase):
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
        self.evidence_data = {
            "case": self.case.id,
            "type": "Disk Image",
            "name": "Test Evidence",
            "hash_md5": "d41d8cd98f00b204e9800998ecf8427e",
            "acquisition_date": "2023-01-01T00:00:00Z",
            "storage_location": "/s3/bucket/evidence.img",
        }

    def test_evidence_source_serializer_valid_data(self):
        serializer = EvidenceSourceSerializer(data=self.evidence_data)
        self.assertTrue(serializer.is_valid())

    def test_evidence_source_serializer_missing_hash(self):
        invalid_data = self.evidence_data.copy()
        del invalid_data["hash_md5"]
        serializer = EvidenceSourceSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
