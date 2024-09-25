# backend/Dockerfile.django
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]