"""
Connect Celery to Django-backend.
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
celery_app = Celery("config")

app.conf.update(
    broker_url='kafka://kafka1:9092',
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks()
