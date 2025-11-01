#!/bin/bash

echo "🔄 Resetting migrations..."

# Stop containers
echo "Stopping containers..."
docker-compose down

# Delete migration files
echo "Deleting old migrations..."
find apps -path "*/migrations/*.py" -not -name "__init__.py" -delete
find apps -path "*/migrations/*.pyc" -delete

# Ensure migration directories exist
echo "Creating migration directories..."
for app in users marketplace messaging transactions reviews safety admin_panel; do
    mkdir -p apps/$app/migrations
    touch apps/$app/migrations/__init__.py
done

# Start database
echo "Starting database..."
docker-compose up -d db
sleep 5

# Reset database
echo "Resetting database..."
docker-compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS campus_marketplace;"
docker-compose exec db psql -U postgres -c "CREATE DATABASE campus_marketplace;"

# Stop and restart all services
echo "Restarting all services..."
docker-compose down
docker-compose up -d
sleep 10

# Create migrations in order
echo "Creating migrations..."
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations marketplace
docker-compose exec web python manage.py makemigrations messaging
docker-compose exec web python manage.py makemigrations transactions
docker-compose exec web python manage.py makemigrations reviews
docker-compose exec web python manage.py makemigrations safety
docker-compose exec web python manage.py makemigrations admin_panel

# Apply migrations
echo "Applying migrations..."
docker-compose exec web python manage.py migrate

echo "✅ Done! Now create a superuser:"
echo "docker-compose exec web python manage.py createsuperuser"