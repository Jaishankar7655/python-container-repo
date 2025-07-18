# Django Book Management System - Deployment Guide

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Latest-blue.svg)](https://www.docker.com/)

## 📋 Table of Contents

- [Application Overview](#application-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Database Setup](#database-setup)
- [Application Configuration](#application-configuration)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Static Files & Media](#static-files--media)
- [SSL/HTTPS Setup](#sslhttps-setup)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

## 🚀 Application Overview

The Django Book Management System is a web application that allows users to manage a library of books with full CRUD operations. The application includes:

### Core Features
- **Book Management**: Create, read, update, and delete books
- **Search Functionality**: Search books by title, author, or ISBN
- **Responsive UI**: Bootstrap-based responsive design
- **Flash Messages**: User feedback for all operations
- **Data Validation**: Form validation and error handling

### Technical Stack
- **Backend**: Django 5.2.4 with Python 3.12
- **Database**: MySQL 8.0
- **Frontend**: HTML5, Bootstrap 5, Font Awesome
- **Web Server**: Nginx (reverse proxy)
- **Application Server**: Gunicorn
- **Containerization**: Docker & Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Client      │    │     Nginx       │    │  Django App     │
│   (Browser)     │◄──►│ (Reverse Proxy) │◄──►│   (Gunicorn)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │   MySQL DB      │
                                              │  (Data Layer)   │
                                              └─────────────────┘
```

### Application Structure
```
book_management/
├── project/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── books/                  # Books application
│   ├── models.py          # Book model
│   ├── views.py           # Business logic
│   ├── forms.py           # Form definitions
│   ├── urls.py            # App URLs
│   └── templates/         # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── requirements.txt        # Python dependencies
└── manage.py              # Django management
```

## 🔧 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04 LTS or CentOS 8+
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 10GB+ available space
- **Network**: Ports 80, 443, 8000, 3306 accessible

### Required Software
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- OpenSSL (for SSL certificates)

### AWS/Cloud Requirements
- EC2 instance (t3.small minimum)
- Security groups configured
- Elastic IP (recommended)
- RDS MySQL instance (optional)

## 🗄️ Database Setup

### Database Schema
The application uses the following database structure:

```sql
CREATE DATABASE book DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Book model fields
CREATE TABLE books_book (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    publication_date DATE NOT NULL,
    pages INTEGER NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_books_title ON books_book(title);
CREATE INDEX idx_books_author ON books_book(author);
CREATE INDEX idx_books_isbn ON books_book(isbn);
```

### Database Configuration
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'book'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'mysql-db'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
```

## ⚙️ Application Configuration

### Django Settings Overview
```python
# Key settings for deployment
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', '13.126.115.143']
SECRET_KEY = 'your-secret-key-here'

# Database configuration
DATABASES = { ... }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### URL Configuration
```python
# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/add/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
]
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
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

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/static /app/media /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -s /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "project.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  mysql-db:
    image: mysql:8.0
    container_name: book-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - book_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u${DB_USER}", "-p${DB_PASSWORD}"]
      timeout: 20s
      retries: 10
      interval: 30s
      start_period: 80s

  django-app:
    build: .
    container_name: book-django
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      mysql-db:
        condition: service_healthy
    networks:
      - book_network
    volumes:
      - static_volume:/app/static
      - media_volume:/app/media
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    container_name: book-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - static_volume:/app/static
      - media_volume:/app/media
    depends_on:
      - django-app
    networks:
      - book_network

volumes:
  mysql_data:
  static_volume:
  media_volume:

networks:
  book_network:
    driver: bridge
```

## 🔐 Environment Variables

### .env File
```env
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DJANGO_SETTINGS_MODULE=project.settings

# Database Configuration
DB_NAME=book
DB_USER=bookuser
DB_PASSWORD=secure_password_here
DB_HOST=mysql-db
DB_PORT=3306

# Server Configuration
ALLOWED_HOSTS=13.126.115.143,yourdomain.com,localhost
SERVER_NAME=yourdomain.com

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Environment-Specific Configurations

#### Production (.env.prod)
```env
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### Staging (.env.staging)
```env
DEBUG=False
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

#### Development (.env.dev)
```env
DEBUG=True
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

## 📁 Static Files & Media

### Static Files Configuration
```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'books/static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Nginx Static Files Configuration
```nginx
# nginx/nginx.conf
server {
    listen 80;
    server_name 13.126.115.143;

    # Static files
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /app/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Django application
    location / {
        proxy_pass http://django-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 SSL/HTTPS Setup

### Generate SSL Certificate
```bash
# Self-signed certificate for testing
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Let's Encrypt certificate for production
certbot certonly --webroot -w /var/www/html -d yourdomain.com
```

### Nginx SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Application proxy
    location / {
        proxy_pass http://django-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints
```python
# books/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)
```

### Monitoring Script
```bash
#!/bin/bash
# scripts/monitor.sh

# Health check
echo "Checking application health..."
curl -f http://localhost:8000/health/ || echo "Health check failed"

# Check containers
echo "Checking container status..."
docker-compose ps

# Check disk space
echo "Checking disk space..."
df -h

# Check memory usage
echo "Checking memory usage..."
free -h

# Check application logs
echo "Recent application logs..."
docker-compose logs --tail=10 django-app
```

## 💾 Backup & Recovery

### Database Backup Script
```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="book"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
echo "Creating database backup..."
docker-compose exec mysql-db mysqldump -u root -p$DB_PASSWORD $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
echo "Creating media files backup..."
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# Static files backup
echo "Creating static files backup..."
tar -czf $BACKUP_DIR/static_backup_$DATE.tar.gz static/

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR"
```

### Recovery Script
```bash
#!/bin/bash
# scripts/restore.sh

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_date>"
    echo "Example: $0 20250118_143022"
    exit 1
fi

BACKUP_DATE=$1
BACKUP_DIR="/opt/backups"

# Restore database
echo "Restoring database from backup..."
docker-compose exec -T mysql-db mysql -u root -p$DB_PASSWORD $DB_NAME < $BACKUP_DIR/db_backup_$BACKUP_DATE.sql

# Restore media files
echo "Restoring media files..."
tar -xzf $BACKUP_DIR/media_backup_$BACKUP_DATE.tar.gz

# Restore static files
echo "Restoring static files..."
tar -xzf $BACKUP_DIR/static_backup_$BACKUP_DATE.tar.gz

echo "Restore completed"
```

## 🚀 Deployment Steps

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
sudo mkdir -p /opt/book-management
sudo chown $USER:$USER /opt/book-management
```

### 2. Application Setup
```bash
# Clone repository
cd /opt/book-management
git clone https://github.com/your-repo/book-management.git .

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Create necessary directories
mkdir -p logs nginx/ssl mysql
```

### 3. SSL Certificate Setup
```bash
# For production with Let's Encrypt
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

### 4. Deploy Application
```bash
# Build and start containers
docker-compose up --build -d

# Check status
docker-compose ps

# Run migrations
docker-compose exec django-app python manage.py migrate

# Create superuser
docker-compose exec django-app python manage.py createsuperuser

# Test application
curl -f http://localhost:8000/
```

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check MySQL container
docker-compose logs mysql-db

# Test connection
docker-compose exec django-app python manage.py dbshell

# Reset database
docker-compose down -v mysql-db
docker-compose up -d mysql-db
```

#### Static Files Not Loading
```bash
# Collect static files
docker-compose exec django-app python manage.py collectstatic --noinput

# Check nginx configuration
docker-compose exec nginx nginx -t

# Restart nginx
docker-compose restart nginx
```

#### Application Won't Start
```bash
# Check application logs
docker-compose logs django-app

# Check for syntax errors
docker-compose exec django-app python manage.py check

# Debug mode
docker-compose exec django-app python manage.py runserver 0.0.0.0:8000
```

#### Performance Issues
```bash
# Monitor resources
docker stats

# Check database performance
docker-compose exec mysql-db mysql -u root -p -e "SHOW PROCESSLIST;"

# Optimize database
docker-compose exec mysql-db mysql -u root -p -e "OPTIMIZE TABLE books_book;"
```

### Log Analysis
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs django-app
docker-compose logs mysql-db
docker-compose logs nginx

# Application logs
tail -f logs/django.log
tail -f logs/gunicorn.log
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Server resources adequate
- [ ] Docker and Docker Compose installed
- [ ] Security groups configured
- [ ] SSL certificates obtained
- [ ] Environment variables configured
- [ ] Database backup taken (if updating)

### Deployment
- [ ] Code pulled from repository
- [ ] Environment file updated
- [ ] Containers built and started
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Health checks passing
- [ ] SSL working correctly

### Post-Deployment
- [ ] Application accessible
- [ ] All features working
- [ ] Performance acceptable
- [ ] Monitoring configured
- [ ] Backup scheduled
- [ ] Documentation updated
