#!/bin/bash

set -e

echo "🔥 COMPLETE DATABASE AND MIGRATION RESET"
echo "This will delete all data!"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "1️⃣  Stopping all containers..."
docker-compose down

echo ""
echo "2️⃣  Removing database volume..."
docker volume rm campus_marketplace_backend_postgres_data 2>/dev/null || echo "Volume already removed"

echo ""
echo "3️⃣  Starting database..."
docker-compose up -d db redis
sleep 15

echo ""
echo "4️⃣  Creating fresh database..."
# Terminate any existing connections
docker-compose exec -T db psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'campus_marketplace';" 2>/dev/null || true

# Drop if exists
docker-compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS campus_marketplace;" 2>/dev/null || true

# Create new
docker-compose exec -T db psql -U postgres -c "CREATE DATABASE campus_marketplace;"

echo ""
echo "5️⃣  Starting web and celery..."
docker-compose up -d web celery
sleep 15

echo ""
echo "6️⃣  Verifying migration files in container..."
docker-compose exec web ls -la /app/apps/users/migrations/

echo ""
echo "7️⃣  Showing migration status..."
docker-compose exec web python manage.py showmigrations

echo ""
echo "8️⃣  Applying migrations..."
docker-compose exec web python manage.py migrate

echo ""
echo "9️⃣  Verifying migrations applied..."
docker-compose exec web python manage.py showmigrations

echo ""
echo "🔟 Checking web logs..."
docker-compose logs web --tail 30

echo ""
echo "✅ RESET COMPLETE!"
echo ""
echo "Container status:"
docker-compose ps

echo ""
echo "Next steps:"
echo "1. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "2. Seed data: docker-compose exec web python manage.py seed_data"
echo "3. Access admin: http://localhost:8000/admin/"
echo ""