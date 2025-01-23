FROM python:3.11

WORKDIR /user_service

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY .env ./user_service

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . /user_service/
# Добавьте путь /auth_service в PYTHONPATH
ENV PYTHONPATH=/user_service