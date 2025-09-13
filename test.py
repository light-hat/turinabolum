from urllib.parse import urlparse
url = "http://minio:9000/mybucket/dumps/2025/09/12/alerts_28_08_20250912_115432_454.json"
parsed = urlparse(url)
path = parsed.path.lstrip("/")
parts = path.split("/", 1)
if len(parts) < 2 or not parts[0] or not parts[1]:
    raise ValueError(f"Некорректный URL (ожидается /<bucket>/<object>): {url}")
bucket, object_name = parts[0], parts[1]
print(bucket)
print(object_name)
