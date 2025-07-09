# Start from base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Accept secrets at build-time
ARG SECRET_KEY
ARG DATABASE_URL

# Make them available to Django during collectstatic
ENV SECRET_KEY=${SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}

# Copy code
COPY . /app/

# Collect static files (requires env vars)
RUN python manage.py collectstatic --noinput

# Expose port and run
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]














# # Use official Python image as base
# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy project files
# COPY . /app/

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Expose port 8000
# EXPOSE 8000

# # Start Django application
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]