FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=1000
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libtk8.6 \
    libtcl8.6 \
    librdkafka-dev \
    python3-dev \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir --timeout 1000 --retries 5 -r requirements.txt

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

COPY . /app/

EXPOSE 8000

RUN groupadd -g 1000 turinabolum && useradd -u 1000 -g turinabolum -m turinabolum

RUN chown -R turinabolum:turinabolum /app

USER turinabolum

ENTRYPOINT ["sh", "./entrypoint.sh"]
