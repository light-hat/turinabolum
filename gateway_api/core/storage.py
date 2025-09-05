"""
Custom storage backends for Turinabolum.
"""

import os
from datetime import datetime

from storages.backends.s3boto3 import S3Boto3Storage


class MinIOStorage(S3Boto3Storage):
    """
    Custom MinIO storage backend for Turinabolum.
    Provides organized file structure for different types of uploads.
    """

    def get_available_name(self, name, max_length=None):
        """
        Override to ensure unique filenames and organized structure.
        """
        # Get the original filename and extension
        name, ext = os.path.splitext(name)

        # Create organized path structure: dumps/YYYY/MM/DD/
        now = datetime.now()
        date_path = now.strftime("%Y/%m/%d")

        # Create unique filename with timestamp
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")[
            :-3
        ]  # Remove last 3 digits of microseconds
        unique_name = f"{name}_{timestamp}{ext}"

        # Construct full path
        full_path = f"dumps/{date_path}/{unique_name}"

        return full_path

    def url(self, name):
        """
        Override URL generation to use MinIO endpoint.
        """
        if self.custom_domain:
            return f"{self.custom_domain}/{name}"
        else:
            return f"{self.endpoint_url}/{self.bucket_name}/{name}"


class StaticMinIOStorage(MinIOStorage):
    """
    Storage backend for static files in MinIO.
    """

    location = "static"
    default_acl = "public-read"


class MediaMinIOStorage(MinIOStorage):
    """
    Storage backend for media files in MinIO.
    """

    location = "media"
    default_acl = "private"

