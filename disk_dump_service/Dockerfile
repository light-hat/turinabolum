FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -sSL https://raw.githubusercontent.com/log2timeline/plaso/master/install.sh | bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
