from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Incident
from core.serializers import CaseSerializer

class CaseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.incident = Incident.objects.create(
            title='Test Incident',
            description='This is a test incident',
            status='New',
            severity='High',
            classification='Malware',
            confidentiality='Internal',
            created_by=self.user
        )
        self.case_data = {
            'incident': self.incident.id,
            'title': 'Test Case',
            'description': 'This is a test case',
            'status': 'Active',
            'lead_investigator': self.user.id
        }

    def test_case_serializer_valid_data(self):
        serializer = CaseSerializer(data=self.case_data)
        self.assertTrue(serializer.is_valid())

    def test_case_serializer_missing_title(self):
        invalid_data = self.case_data.copy()
        del invalid_data['title']
        serializer = CaseSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        