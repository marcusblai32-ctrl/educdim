#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=config.settings

echo "🔧 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️  Creating accounts migrations..."
python manage.py makemigrations accounts

echo "🗄️  Forcing accounts migration..."
python manage.py migrate accounts --fake-initial

echo "🗄️  Running all migrations..."
python manage.py migrate

echo "👤 Making first user superuser..."
python manage.py shell <<EOF
from accounts.models import CustomUser
user = CustomUser.objects.first()
if user:
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"{user.email} se superuser kounye a!")
else:
    print("Pa gen itilizatè. Kreye yon kont an premye.")
EOF

STATIC_ROOT_PATH="${STATIC_ROOT:-$(pwd)/staticfiles}"
mkdir -p "$STATIC_ROOT_PATH"

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build completed successfully!"
