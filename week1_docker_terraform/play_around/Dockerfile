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
# ENTRYPOINT vs CMD ["bash"] considerations:
#
# Use ENTRYPOINT when:
# 1. Container serves a specific purpose (e.g., a data pipeline script)
# 2. You want to enforce a specific executable that cannot be overridden
# 3. Container acts like a standalone executable/command
# Example: ENTRYPOINT ["python", "pipeline.py"]
#
# Use CMD ["bash"] when:
# 1. Container is for development/debugging purposes
# 2. You need flexibility to run different commands
# 3. Interactive shell access is required
# 4. Container serves multiple purposes
#
# Current setup uses CMD ["bash"] because:
# - This appears to be a development environment
# - We need flexibility to run different commands
# - Interactive shell access is useful for debugging

