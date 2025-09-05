FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libffi-dev \
    pkg-config \
    wget \
    curl \
    gnupg \
    python3 \
    python3-pip \
    python3-full \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository universe -y \
    && add-apt-repository ppa:gift/stable -y \
    && apt update \
    && apt-get -y install plaso-tools

RUN apt-get update && apt-get remove -y python3-urllib3 && apt-get autoremove -y

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . /app/

EXPOSE 8000

RUN groupadd -g 1000 turinabolum && useradd -u 1000 -g turinabolum -m turinabolum

RUN chown -R turinabolum:turinabolum /app

USER turinabolum

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
