from core.models import TTP, Case, CaseTTP, Incident
from django.contrib.auth.models import User
from django.test import TestCase


class TTPModelTest(TestCase):
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
        self.ttp_data = {
            "technique_id": "T1059.003",
            "name": "Windows Command Shell",
            "tactic": "Execution",
        }

    def test_create_ttp(self):
        ttp = TTP.objects.create(**self.ttp_data)
        self.assertEqual(ttp.technique_id, "T1059.003")
        self.assertEqual(ttp.name, "Windows Command Shell")
        self.assertEqual(ttp.tactic, "Execution")

    def test_ttp_str_representation(self):
        ttp = TTP.objects.create(**self.ttp_data)
        expected_str = f"{ttp.technique_id} - {ttp.name}"
        self.assertEqual(str(ttp), expected_str)

    def test_create_case_ttp(self):
        ttp = TTP.objects.create(**self.ttp_data)
        case_ttp_data = {
            "case": self.case,
            "ttp": ttp,
            "notes": "Test TTP detection",
            "detected_by": self.user,
        }
        case_ttp = CaseTTP.objects.create(**case_ttp_data)
        self.assertEqual(case_ttp.case, self.case)
        self.assertEqual(case_ttp.ttp, ttp)
        self.assertEqual(case_ttp.notes, "Test TTP detection")

    def test_case_ttp_str_representation(self):
        ttp = TTP.objects.create(**self.ttp_data)
        case_ttp = CaseTTP.objects.create(
            case=self.case, ttp=ttp, detected_by=self.user
        )
        expected_str = f"{case_ttp.case} - {case_ttp.ttp}"
        self.assertEqual(str(case_ttp), expected_str)
