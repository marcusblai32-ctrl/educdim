#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=config.settings

echo "🔧 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️  Creating migrations for all apps..."
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py makemigrations enrollments
python manage.py makemigrations subscriptions
python manage.py makemigrations progress
python manage.py makemigrations quiz
python manage.py makemigrations attendance
python manage.py makemigrations badges
python manage.py makemigrations ranking
python manage.py makemigrations chat
python manage.py makemigrations notifications
python manage.py makemigrations theme_manager
python manage.py makemigrations ads
python manage.py makemigrations dashboard
python manage.py makemigrations todo
python manage.py makemigrations

echo "🗄️  Running migrations for all apps..."
python manage.py migrate accounts
python manage.py migrate courses
python manage.py migrate enrollments
python manage.py migrate subscriptions
python manage.py migrate progress
python manage.py migrate quiz
python manage.py migrate attendance
python manage.py migrate badges
python manage.py migrate ranking
python manage.py migrate chat
python manage.py migrate notifications
python manage.py migrate theme_manager
python manage.py migrate ads
python manage.py migrate dashboard
python manage.py migrate todo
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
