# Using python:3.11-slim as base image because:
# - Python 3.11 offers improved performance and better error messages
# - Slim variant reduces image size by excluding unnecessary packages
# - Good balance between functionality and container size for development
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies and PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file (if you have one)
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Install psycopg2 for PostgreSQL connection
RUN pip install psycopg2-binary

# Copy your application code
# COPY . .

# Keep container running
CMD ["bash"]


