from core.models import Case, EvidenceSource, Incident
from django.contrib.auth.models import User
from django.test import TestCase


class EvidenceSourceModelTest(TestCase):
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
            "case": self.case,
            "type": "Disk Image",
            "name": "Test Evidence",
            "description": "This is a test evidence",
            "hash_md5": "d41d8cd98f00b204e9800998ecf8427e",
            "acquisition_date": "2023-01-01T00:00:00Z",
            "storage_location": "/s3/bucket/evidence.img",
        }

    def test_create_evidence_source(self):
        evidence = EvidenceSource.objects.create(**self.evidence_data)
        self.assertEqual(evidence.name, "Test Evidence")
        self.assertEqual(evidence.type, "Disk Image")
        self.assertEqual(evidence.case, self.case)

    def test_evidence_source_str_representation(self):
        evidence = EvidenceSource.objects.create(**self.evidence_data)
        expected_str = f"{evidence.type}: {evidence.name}"
        self.assertEqual(str(evidence), expected_str)
