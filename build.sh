#!/usr/bin/env bash
set -o errexit

echo "=== Installation ==="
pip install -r requirements.txt

echo "=== Compile messages (sèlman ht ak fr) ==="
python manage.py compilemessages --locale ht --locale fr

echo "=== Collect static ==="
python manage.py collectstatic --noinput

echo "=== Migrations ==="
python manage.py migrate --noinput

echo "=== Build terminé ==="