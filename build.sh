#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=config.settings

echo "🔧 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️  Forcing ads migration..."
python manage.py makemigrations ads
python manage.py migrate ads --fake-initial
python manage.py migrate ads

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
