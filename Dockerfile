FROM python:3.11-slim

RUN rm -rf embedding/
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .