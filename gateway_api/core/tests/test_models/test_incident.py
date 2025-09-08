from core.models import Incident
from django.contrib.auth.models import User
from django.test import TestCase


class IncidentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.incident_data = {
            "title": "Test Incident",
            "description": "This is a test incident",
            "status": "New",
            "severity": "High",
            "classification": "Malware",
            "confidentiality": "Internal",
            "created_by": self.user,
        }

    def test_create_incident(self):
        incident = Incident.objects.create(**self.incident_data)
        self.assertEqual(incident.title, "Test Incident")
        self.assertEqual(incident.status, "New")
        self.assertEqual(incident.severity, "High")
        self.assertEqual(incident.created_by, self.user)

    def test_incident_str_representation(self):
        incident = Incident.objects.create(**self.incident_data)
        expected_str = f"{incident.title} (ID: {incident.id})"
        self.assertEqual(str(incident), expected_str)

    def test_incident_ordering(self):
        incident1 = Incident.objects.create(**self.incident_data)
        incident2 = Incident.objects.create(
            title="Another Incident",
            description="Another test incident",
            status="New",
            severity="Medium",
            classification="Phishing",
            confidentiality="Internal",
            created_by=self.user,
        )
        incidents = Incident.objects.all()
        self.assertEqual(incidents[0], incident2)
        self.assertEqual(incidents[1], incident1)
