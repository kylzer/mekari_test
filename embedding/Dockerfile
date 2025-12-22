FROM python:3.10-slim

# Install basic dependencies
RUN apt-get update

# Set work directory
WORKDIR /app
COPY ./requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . /app