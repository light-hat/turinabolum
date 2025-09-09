#!/bin/sh

python3 manage.py collectstatic --no-input
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py initdb
python3 manage.py init_minio


exec uvicorn config.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  ${RELOAD:+--reload}
  