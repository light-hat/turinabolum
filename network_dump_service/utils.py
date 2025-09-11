import os
import subprocess

import aiofiles
import aiohttp
from minio import Minio
from minio.error import S3Error

from .config import Config


async def download_from_s3(url: str, save_path: str):
    """Асинхронно скачивает файл по presigned URL из MinIO"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)
            else:
                raise Exception(f"Failed to download file. Status: {response.status}")


# def run_plaso_command(cmd: list[str]) -> str:
#     """Запускает команду plaso (log2timeline/psort) и возвращает вывод"""
#     process = subprocess.Popen(
#         cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
#     )
#     stdout, _ = process.communicate()
#     if process.returncode != 0:
#         raise RuntimeError(f"Plaso command failed: {stdout}")
#     return stdout
