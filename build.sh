#!/usr/bin/env bash
set -o errexit

echo "=== Installation des dépendances ==="
pip install -r requirements.txt

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --noinput

echo "=== Exécution des migrations ==="
python manage.py migrate --noinput

echo "=== Build terminé avec succès ==="