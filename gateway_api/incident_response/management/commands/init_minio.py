"""
Management command to initialize MinIO bucket for file storage.
"""

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Initialize MinIO bucket for file storage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--bucket-name",
            type=str,
            default=settings.AWS_STORAGE_BUCKET_NAME,
            help="Name of the bucket to create (default: from settings)",
        )

    def handle(self, *args, **options):
        bucket_name = options["bucket_name"]

        # if not settings.USE_S3:
        #     self.stdout.write(
        #         self.style.WARNING(
        #             "S3 storage is disabled. Skipping MinIO initialization."
        #         )
        #     )
        #     return

        try:
            # Create S3 client
            s3_client = boto3.client(
                "s3",
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name="us-east-1",  # MinIO doesn't care about region
            )

            # Check if bucket exists
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                self.stdout.write(
                    self.style.SUCCESS(f'Bucket "{bucket_name}" already exists.')
                )
            except ClientError as e:
                error_code = int(e.response["Error"]["Code"])
                if error_code == 404:
                    # Bucket doesn't exist, create it
                    s3_client.create_bucket(Bucket=bucket_name)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created bucket "{bucket_name}".'
                        )
                    )
                else:
                    raise CommandError(f"Error checking bucket: {e}")

            # Create folder structure
            folders = ["dumps/", "static/", "media/"]
            for folder in folders:
                try:
                    s3_client.put_object(Bucket=bucket_name, Key=folder)
                    self.stdout.write(f"Created folder: {folder}")
                except ClientError as e:
                    self.stdout.write(
                        self.style.WARNING(f"Could not create folder {folder}: {e}")
                    )

            self.stdout.write(
                self.style.SUCCESS("MinIO initialization completed successfully!")
            )

        except Exception as e:
            raise CommandError(f"Failed to initialize MinIO: {e}")
