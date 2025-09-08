from core.models import Incident, IncidentThreatActor, ThreatActor
from django.contrib.auth.models import User
from django.test import TestCase


class ThreatActorModelTest(TestCase):
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
        self.threat_actor_data = {
            "name": "APT29",
            "description": "Russian threat actor",
            "aliases": "Cozy Bear",
            "origin": "Russia",
        }

    def test_create_threat_actor(self):
        threat_actor = ThreatActor.objects.create(**self.threat_actor_data)
        self.assertEqual(threat_actor.name, "APT29")
        self.assertEqual(threat_actor.description, "Russian threat actor")
        self.assertEqual(threat_actor.origin, "Russia")

    def test_threat_actor_str_representation(self):
        threat_actor = ThreatActor.objects.create(**self.threat_actor_data)
        self.assertEqual(str(threat_actor), "APT29")

    def test_create_incident_threat_actor(self):
        threat_actor = ThreatActor.objects.create(**self.threat_actor_data)
        incident_ta_data = {
            "incident": self.incident,
            "threat_actor": threat_actor,
            "confidence": "High",
            "evidence": "Test evidence",
        }
        incident_ta = IncidentThreatActor.objects.create(**incident_ta_data)
        self.assertEqual(incident_ta.incident, self.incident)
        self.assertEqual(incident_ta.threat_actor, threat_actor)
        self.assertEqual(incident_ta.confidence, "High")

    def test_incident_threat_actor_str_representation(self):
        threat_actor = ThreatActor.objects.create(**self.threat_actor_data)
        incident_ta = IncidentThreatActor.objects.create(
            incident=self.incident, threat_actor=threat_actor, confidence="High"
        )
        expected_str = f"{incident_ta.incident} - {incident_ta.threat_actor}"
        self.assertEqual(str(incident_ta), expected_str)
