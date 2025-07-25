# 📚 Django Book Management System

<div align="center">
 
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-4.x-green.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0-orange.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*A modern, containerized Django web application for managing your book collection*

[Features](#-features) • [Quick Start](#-quick-start) • [API](#-api-endpoints) • [Docker](#-docker-services) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

- 📖 **Complete CRUD Operations** - Create, read, update, and delete books
- 🔍 **Advanced Search** - Search by title, author, or ISBN
- 🐳 **Docker Ready** - Fully containerized with Docker Compose
- 🚀 **Production Ready** - Nginx reverse proxy with static file serving
- 📱 **Responsive Design** - Clean and modern user interface
- 🗄️ **MySQL Database** - Robust data persistence
- ⚡ **High Performance** - Gunicorn WSGI server

## 🚀 Quick Start

### Prerequisites
- 🐳 Docker & Docker Compose
- 💻 Git

### 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/django-book-management.git
cd django-book-management

# Create environment file
cp .env.example .env

# Build and run with Docker Compose
docker-compose up --build

# Access the application
# 🌐 http://localhost


DEBUG=True
SECRET_KEY=your-super-secret-key-here
DATABASE_NAME=book
DATABASE_USER=appuser
DATABASE_PASSWORD=apppass
DATABASE_HOST=mysql-db
DATABASE_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1



🏗️ Project Architecture 
📁 django-book-management/
├── 🐳 docker-compose.yml      # Multi-container orchestration
├── 🐳 Dockerfile             # Django app containerization
├── 🌐 nginx.conf             # Web server configuration
├── 📄 requirements.txt       # Python dependencies
├── ⚙️ .env                   # Environment variables
├── 🎯 manage.py              # Django management
├── 📁 project/               # Django project settings
│   ├── ⚙️ settings.py
│   ├── 🔗 urls.py
│   └── 🚀 wsgi.py
├── 📁 books/                 # Book management app
│   ├── 🏗️ models.py
│   ├── 👀 views.py
│   ├── 📝 forms.py
│   └── 📁 templates/
└── 📁 static/               # Static files




📊 Database Schema

📚 Book Model
├── 📖 title (CharField)
├── ✍️ author (CharField) 
├── 🔢 isbn (CharField, unique)
├── 📅 published_date (DateField)
├── 📝 description (TextField)
├── 🕐 created_at (DateTimeField)
└── 🕐 updated_at (DateTimeField)


🛠️ API Endpoints

