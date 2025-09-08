from core.models import Artifact, Case, EvidenceSource, Incident
from django.contrib.auth.models import User
from django.test import TestCase


class ArtifactModelTest(TestCase):
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
        self.artifact_data = {
            "source": self.evidence,
            "type": "File",
            "name": "test.exe",
            "path": "C:\\Windows\\System32\\test.exe",
            "size": 1024,
            "hash_md5": "d41d8cd98f00b204e9800998ecf8427e",
        }

    def test_create_artifact(self):
        artifact = Artifact.objects.create(**self.artifact_data)
        self.assertEqual(artifact.name, "test.exe")
        self.assertEqual(artifact.type, "File")
        self.assertEqual(artifact.source, self.evidence)

    def test_artifact_str_representation(self):
        artifact = Artifact.objects.create(**self.artifact_data)
        expected_str = f"{artifact.type} - {artifact.name}"
        self.assertEqual(str(artifact), expected_str)
