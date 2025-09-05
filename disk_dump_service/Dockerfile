FROM python:3.11-slim-bullseye

RUN apt-get update \
    apt-get install -y software-properties-common

RUN add-apt-repository universe -y \
    && add-apt-repository ppa:gift/stable -y

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    plaso-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
