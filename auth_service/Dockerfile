FROM python:3.11

WORKDIR /auth_service

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY .env ./auth_service

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . /auth_service/

# Добавьте путь /auth_service в PYTHONPATH
ENV PYTHONPATH=/auth_service