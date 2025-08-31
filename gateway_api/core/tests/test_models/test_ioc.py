from core.models import IOC, Case, Incident
from django.contrib.auth.models import User
from django.test import TestCase


class IOCModelTest(TestCase):
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
            "case": self.case,
            "type": "Hash",
            "value": "d41d8cd98f00b204e9800998ecf8427e",
            "description": "Test MD5 hash",
            "tlp": "WHITE",
            "confidence": "High",
        }

    def test_create_ioc(self):
        ioc = IOC.objects.create(**self.ioc_data)
        self.assertEqual(ioc.value, "d41d8cd98f00b204e9800998ecf8427e")
        self.assertEqual(ioc.type, "Hash")
        self.assertEqual(ioc.case, self.case)

    def test_ioc_str_representation(self):
        ioc = IOC.objects.create(**self.ioc_data)
        expected_str = f"{ioc.type}: {ioc.value}"
        self.assertEqual(str(ioc), expected_str)
