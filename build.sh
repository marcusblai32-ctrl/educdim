#!/usr/bin/env bash
set -o errexit

echo "=== Installation ==="
pip install -r requirements.txt

echo "=== Collect static ==="
python manage.py collectstatic --noinput

echo "=== Ajoute kolòn quiz ki manke yo ==="
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    # Ajoute module_id nan quiz_quiz
    cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name = 'quiz_quiz' AND column_name = 'module_id'\")
    if not cursor.fetchone():
        cursor.execute('ALTER TABLE quiz_quiz ADD COLUMN module_id bigint NULL REFERENCES courses_module(id) DEFERRABLE INITIALLY DEFERRED')
        print('module_id ajoute')
    else:
        print('module_id OK')
    
    # Ajoute lecon_id nan quiz_quiz
    cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name = 'quiz_quiz' AND column_name = 'lecon_id'\")
    if not cursor.fetchone():
        cursor.execute('ALTER TABLE quiz_quiz ADD COLUMN lecon_id bigint NULL REFERENCES courses_lecon(id) DEFERRABLE INITIALLY DEFERRED')
        print('lecon_id ajoute')
    else:
        print('lecon_id OK')
    
    # Fè cours_id nullable
    cursor.execute('ALTER TABLE quiz_quiz ALTER COLUMN cours_id DROP NOT NULL')
    print('cours_id nullable')
    
    # Kreye indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS quiz_quiz_module_id_idx ON quiz_quiz (module_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS quiz_quiz_lecon_id_idx ON quiz_quiz (lecon_id)')
    print('Indexes kreye')
    
    print('Tout kolòn quiz OK!')
"

echo "=== Migrations ==="
python manage.py migrate --noinput

echo "=== Build terminé ==="