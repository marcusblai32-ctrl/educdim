#!/usr/bin/env bash
set -o errexit

echo "=== Installation ==="
pip install -r requirements.txt

echo "=== Collect static ==="
python manage.py collectstatic --noinput

echo "=== Ajoute kolòn ki manke yo ==="
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    # duree_quiz nan quiz_quiz
    cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name = 'quiz_quiz' AND column_name = 'duree_quiz'\")
    if not cursor.fetchone():
        cursor.execute('ALTER TABLE quiz_quiz ADD COLUMN duree_quiz integer NOT NULL DEFAULT 15')
        print('duree_quiz ajoute')
    else:
        print('duree_quiz OK')
    
    # module_id nan quiz_quiz
    cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name = 'quiz_quiz' AND column_name = 'module_id'\")
    if not cursor.fetchone():
        cursor.execute('ALTER TABLE quiz_quiz ADD COLUMN module_id bigint NULL REFERENCES courses_module(id)')
        print('module_id ajoute')
    else:
        print('module_id OK')
    
    # lecon_id nan quiz_quiz
    cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name = 'quiz_quiz' AND column_name = 'lecon_id'\")
    if not cursor.fetchone():
        cursor.execute('ALTER TABLE quiz_quiz ADD COLUMN lecon_id bigint NULL REFERENCES courses_lecon(id)')
        print('lecon_id ajoute')
    else:
        print('lecon_id OK')
    
    print('Tout kolòn OK!')
"

echo "=== Migrations ==="
python manage.py migrate --noinput

echo "=== Build terminé ==="