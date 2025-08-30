from core.models import ThreatIntelFeed, ThreatIntelIOC
from django.test import TestCase


class ThreatIntelFeedModelTest(TestCase):
    def setUp(self):
        self.feed_data = {
            "name": "Test Feed",
            "description": "Test Threat Intelligence Feed",
            "feed_type": "STIX",
            "url": "https://example.com/feed.json",
            "polling_interval": 3600,
            "status": "Active",
        }

    def test_create_threat_intel_feed(self):
        feed = ThreatIntelFeed.objects.create(**self.feed_data)
        self.assertEqual(feed.name, "Test Feed")
        self.assertEqual(feed.feed_type, "STIX")
        self.assertEqual(feed.url, "https://example.com/feed.json")
        self.assertEqual(feed.status, "Active")

    def test_threat_intel_feed_str_representation(self):
        feed = ThreatIntelFeed.objects.create(**self.feed_data)
        self.assertEqual(str(feed), "Test Feed")


class ThreatIntelIOCModelTest(TestCase):
    def setUp(self):
        self.feed = ThreatIntelFeed.objects.create(
            name="Test Feed",
            feed_type="STIX",
            url="https://example.com/feed.json",
            status="Active",
        )
        self.ioc_data = {
            "feed": self.feed,
            "type": "Hash",
            "value": "d41d8cd98f00b204e9800998ecf8427e",
            "description": "Test MD5 hash",
            "tlp": "WHITE",
            "confidence": "High",
            "severity": "Critical",
        }

    def test_create_threat_intel_ioc(self):
        ioc = ThreatIntelIOC.objects.create(**self.ioc_data)
        self.assertEqual(ioc.feed, self.feed)
        self.assertEqual(ioc.type, "Hash")
        self.assertEqual(ioc.value, "d41d8cd98f00b204e9800998ecf8427e")
        self.assertEqual(ioc.confidence, "High")

    def test_threat_intel_ioc_str_representation(self):
        ioc = ThreatIntelIOC.objects.create(**self.ioc_data)
        expected_str = f"{ioc.type}: {ioc.value}"
        self.assertEqual(str(ioc), expected_str)
