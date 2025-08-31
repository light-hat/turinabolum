from core.models import DumpUpload
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class DumpUploadModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.dump_file = SimpleUploadedFile(
            "test.dmp", b"file_content", content_type="application/octet-stream"
        )
        self.dump_upload_data = {
            "dump_type": "Memory",
            "original_filename": "memory.dmp",
            "dump_file": self.dump_file,
            "uploaded_by": self.user,
            "status": "Uploaded",
        }

    def test_create_dump_upload(self):
        dump_upload = DumpUpload.objects.create(**self.dump_upload_data)
        self.assertEqual(dump_upload.dump_type, "Memory")
        self.assertEqual(dump_upload.original_filename, "memory.dmp")
        self.assertEqual(dump_upload.uploaded_by, self.user)
        self.assertEqual(dump_upload.status, "Uploaded")

    def test_dump_upload_str_representation(self):
        dump_upload = DumpUpload.objects.create(**self.dump_upload_data)
        expected_str = f"{dump_upload.dump_type} Dump: {dump_upload.original_filename}"
        self.assertEqual(str(dump_upload), expected_str)
