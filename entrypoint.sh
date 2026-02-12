#!/bin/bash
set -e

echo "Waiting for database..."
while ! pg_isready -h db -p 5432 > /dev/null 2>&1; do
  sleep 1
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Creating superuser if not exists..."
python manage.py shell << END
from apps.account.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
END

echo "Starting application..."
exec "$@"
