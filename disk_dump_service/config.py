import os

class Config:
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"

    OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "os01:9200")
    OPENSEARCH_INDEX_PREFIX = os.getenv("OPENSEARCH_INDEX_PREFIX", "disk_dump")

    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
    TEMP_DIR = os.getenv("TEMP_DIR", "/tmp")
