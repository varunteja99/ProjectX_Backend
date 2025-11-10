# Campus Marketplace Backend

A comprehensive Django REST Framework backend for a campus marketplace platform that enables students to buy, sell, and trade items within their campus community. The platform includes features for listings, messaging, transactions, reviews, and safety moderation.

## 🚀 Features

### Core Marketplace
- **Listings Management**: Create, update, and manage product listings with images
- **Search & Filtering**: Advanced search with filtering by category, price, condition, and location
- **Wishlist & Saved Searches**: Save favorite items and set up search alerts

### Communication & Transactions
- **Messaging System**: Real-time messaging between buyers and sellers
- **Offer Management**: Make, accept, and negotiate offers on listings
- **Transaction Processing**: Secure transaction handling and payment tracking

### User Management
- **User Authentication**: JWT-based authentication with email verification
- **User Profiles**: Comprehensive user profiles with ratings and verification
- **Custom User Model**: Extended user model with campus-specific fields

### Safety & Trust
- **Review System**: Rate and review transactions and users
- **Reporting & Moderation**: Report inappropriate content and users
- **Admin Panel**: Comprehensive admin interface for platform management

### Additional Features
- **API Documentation**: Interactive Swagger/ReDoc documentation
- **Async Tasks**: Celery-based background task processing
- **Image Handling**: Support for image uploads and processing
- **Email Notifications**: Automated email notifications for important events

## 🛠️ Tech Stack

- **Framework**: Django 5.2.7
- **API**: Django REST Framework 3.16.1
- **Database**: PostgreSQL 15
- **Cache/Task Queue**: Redis 7
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Task Queue**: Celery 5.5.3
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Image Processing**: Pillow
- **Testing**: pytest, pytest-django, factory-boy
- **Code Quality**: black, flake8, pylint
- **Production Server**: Gunicorn
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis 7 or higher
- Docker and Docker Compose (optional, for containerized setup)
- Git

## 🔧 Installation

### Option 1: Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProjectX_Backend/campus_marketplace_backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv campus_marketplace_venv
   source campus_marketplace_venv/bin/activate  # On Windows: campus_marketplace_venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `campus_marketplace_backend` directory:
   ```env
   # Django Settings
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

   # Database Configuration
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=campus_marketplace
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=5432

   # JWT Configuration
   JWT_ACCESS_TOKEN_LIFETIME=60
   JWT_REFRESH_TOKEN_LIFETIME=1440
   JWT_SECRET_KEY=your-jwt-secret-key

   # CORS Configuration
   CORS_ALLOWED_ORIGINS=http://localhost:3000

   # Email Configuration
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password

   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0

   # Application Settings
   MAX_UPLOAD_SIZE=5242880
   LISTING_EXPIRY_DAYS=90
   ```

5. **Set up the database**
   ```bash
   # Create PostgreSQL database
   createdb campus_marketplace

   # Run migrations
   python manage.py migrate

   # Create superuser (optional)
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Start Redis** (required for Celery)
   ```bash
   redis-server
   ```

8. **Start Celery worker** (in a separate terminal)
   ```bash
   celery -A config worker -l info
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProjectX_Backend/campus_marketplace_backend
   ```

2. **Create `.env` file** (same as above)

3. **Build and start containers**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database on port 5432
   - Redis on port 6379
   - Django web server on port 8000
   - Celery worker

4. **Run migrations** (first time only)
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser** (optional)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run tests for a specific app
pytest apps/marketplace/tests.py

# Run with coverage
pytest --cov=apps --cov-report=html
```

## 📁 Project Structure

```
campus_marketplace_backend/
├── apps/
│   ├── admin_panel/          # Admin panel functionality
│   ├── marketplace/           # Core marketplace features (listings, categories)
│   ├── messaging/             # Messaging system
│   ├── reviews/               # Review and rating system
│   ├── safety/                # Safety and moderation features
│   ├── transactions/          # Transaction and offer management
│   └── users/                 # User authentication and profiles
├── config/                    # Django project configuration
│   ├── settings.py            # Main settings file
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI configuration
│   ├── asgi.py                # ASGI configuration
│   └── celery.py              # Celery configuration
├── media/                     # User-uploaded media files
├── static/                    # Static files
├── reset_scripts/             # Database reset scripts
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image configuration
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate:

1. **Register/Login** to get access and refresh tokens
2. **Include the token** in the Authorization header:
   ```
   Authorization: Bearer <your-access-token>
   ```
3. **Refresh tokens** using the `/api/v1/auth/refresh/` endpoint

## 🔄 Database Migrations

### Create migrations
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Reset migrations (if needed)
```bash
# Use the reset script
./reset_scripts/reset_migrations.sh
```

## 🌱 Seeding Data

Seed initial data for development:

```bash
python manage.py seed_data
```

## 🚀 Deployment

### Production Considerations

1. **Set `DEBUG=False`** in production
2. **Use a secure `SECRET_KEY`** (generate a new one)
3. **Configure proper `ALLOWED_HOSTS`**
4. **Set up SSL/HTTPS** (required for production)
5. **Use environment variables** for all sensitive data
6. **Configure proper database backups**
7. **Set up monitoring and logging**
8. **Use a production-ready WSGI server** (Gunicorn is included)

### Environment Variables for Production

Ensure all production environment variables are set:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- Database credentials
- Email service credentials
- Redis connection details

## 📝 Code Quality

The project includes code quality tools:

```bash
# Format code with black
black .

# Check code style with flake8
flake8 .

# Run pylint
pylint apps/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## 📧 Contact

For inquiries, contact: vchundru@purdue.edu

---

**Note**: This is a backend API. A frontend application is required to interact with the API endpoints. The API is designed to work with any frontend framework (React, Vue, Angular, etc.).

