#!/usr/bin/env bash
set -o errexit

echo "=== Installation des dépendances ==="
pip install -r requirements.txt

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --noinput

echo "=== Migrations subscription uniquement ==="
python manage.py makemigrations subscriptions --noinput
python manage.py migrate subscriptions --noinput

echo "=== Build terminé avec succès ==="