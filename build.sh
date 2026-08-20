#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py makemigrations subscriptions --noinput
python manage.py migrate subscriptions --noinput