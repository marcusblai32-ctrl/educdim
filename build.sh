#!/usr/bin/env bash
set -o errexit

# 1. Enstale depandans yo
pip install -r requirements.txt

# 2. Kolekte fich statik yo
python manage.py collectstatic --no-input

# 3. Fè migrasyon baz done a
python manage.py migrate --no-input

# 4. Kreye superuser (si li pa egziste)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@educdim.com').exists() or User.objects.create_superuser('admin@educdim.com', 'Admin', 'EducDim', 2000, 'admin12345')" | python manage.py shell
