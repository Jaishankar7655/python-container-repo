FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories for static and media files
RUN mkdir -p /app/static /app/media

# Expose port
EXPOSE 8000

# Command with migrations and static files collection
CMD ["sh", "-c", "echo 'Waiting for MySQL...' && while ! nc -z mysql-db 3306; do sleep 1; done && echo 'MySQL is ready!' && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
