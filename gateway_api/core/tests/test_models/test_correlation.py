from core.models import Artifact, Case, CorrelationResult, EvidenceSource, Incident
from django.contrib.auth.models import User
from django.test import TestCase


class CorrelationResultModelTest(TestCase):
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
        self.evidence = EvidenceSource.objects.create(
            case=self.case,
            type="Disk Image",
            name="Test Evidence",
            hash_md5="d41d8cd98f00b204e9800998ecf8427e",
            acquisition_date="2023-01-01T00:00:00Z",
            storage_location="/s3/bucket/evidence.img",
        )
        self.artifact = Artifact.objects.create(
            source=self.evidence,
            type="File",
            name="test.exe",
            path="C:\\Windows\\System32\\test.exe",
            size=1024,
            hash_md5="d41d8cd98f00b204e9800998ecf8427e",
        )
        self.correlation_data = {
            "artifact": self.artifact,
            "correlation_type": "TI",
            "severity": "High",
            "confidence": 0.9,
            "description": "Test correlation",
            "detected_by": self.user,
        }

    def test_create_correlation_result(self):
        correlation = CorrelationResult.objects.create(**self.correlation_data)
        self.assertEqual(correlation.artifact, self.artifact)
        self.assertEqual(correlation.correlation_type, "TI")
        self.assertEqual(correlation.severity, "High")
        self.assertEqual(correlation.confidence, 0.9)
        self.assertEqual(correlation.detected_by, self.user)

    def test_correlation_result_str_representation(self):
        correlation = CorrelationResult.objects.create(**self.correlation_data)
        expected_str = (
            f"Correlation: {correlation.artifact} - {correlation.correlation_type}"
        )
        self.assertEqual(str(correlation), expected_str)
