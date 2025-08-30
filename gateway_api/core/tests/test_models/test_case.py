from core.models import Case, Incident
from django.contrib.auth.models import User
from django.test import TestCase


class CaseModelTest(TestCase):
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
        self.case_data = {
            "incident": self.incident,
            "title": "Test Case",
            "description": "This is a test case",
            "status": "Active",
            "lead_investigator": self.user,
        }

    def test_create_case(self):
        case = Case.objects.create(**self.case_data)
        self.assertEqual(case.title, "Test Case")
        self.assertEqual(case.incident, self.incident)
        self.assertEqual(case.lead_investigator, self.user)

    def test_case_str_representation(self):
        case = Case.objects.create(**self.case_data)
        expected_str = f"Кейс: {case.title} (Инцидент: {case.incident_id})"
        self.assertEqual(str(case), expected_str)
