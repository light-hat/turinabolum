import os
import subprocess

import aiofiles
import aiohttp
from minio import Minio
from minio.error import S3Error
from urllib.parse import urlparse
from .config import Config
from datetime import timedelta
from minio.error import S3Error

async def download_from_s3(url: str, save_path: str, expires_seconds: int = 3600):
    """
    Скачивает объект из MinIO по "старому" url вида:
      http://127.0.0.1:9000/mybucket/path/to/object.json

    Берёт креды из ENV:
      MINIO_ENDPOINT  (например "localhost:9000" или "http://minio:9000")
      MINIO_ACCESS_KEY
      MINIO_SECRET_KEY
      MINIO_SECURE    ("true"/"false") — используется, если в MINIO_ENDPOINT не указана схема

    expires_seconds — время жизни presigned URL в секундах (по умолчанию 3600 = 1 час).
    """

    # --- извлекаем bucket и object_name из переданного URL ---
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")  # "mybucket/path/to/object"
    parts = path.split("/", 1)
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError(f"Некорректный URL (ожидается /<bucket>/<object>): {url}")

    bucket, object_name = parts[0], parts[1]

    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")
    secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
    if not access_key or not secret_key:
        raise EnvironmentError("MINIO_ACCESS_KEY и MINIO_SECRET_KEY должны быть заданы в окружении")

    client = Minio(
            "minio:9000",
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
    )

    try:
        # minio ожидает datetime.timedelta для expires
        presigned_url = client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_name,
            expires=timedelta(seconds=int(expires_seconds))
        )
    except S3Error as exc:
        raise RuntimeError(f"Не удалось сгенерировать presigned URL: {exc}") from exc

    # --- скачиваем через aiohttp ---
    async with aiohttp.ClientSession() as session:
        async with session.get(presigned_url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(1024 * 64):
                        await f.write(chunk)
                return save_path
            else:
                body = await response.text()
                raise RuntimeError(f"Failed to download file. Status: {response.status}. Body: {body}")


def run_plaso_command(cmd: list[str]) -> str:
     """Запускает команду plaso (log2timeline/psort) и возвращает вывод"""
     process = subprocess.Popen(
         cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
     )
     stdout, _ = process.communicate()
     if process.returncode != 0:
         raise RuntimeError(f"Plaso command failed: {stdout}")
     return stdout
