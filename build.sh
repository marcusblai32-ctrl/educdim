#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# ============================================
# AJOUTE KOLÒN KI MANKE YO NAN PROGRES
# ============================================
python manage.py shell << 'EOF'
import psycopg2
import os
from django.conf import settings

# Jwenn koneksyon baz done
db_settings = settings.DATABASES['default']
conn = psycopg2.connect(
    host=db_settings['HOST'],
    database=db_settings['NAME'],
    user=db_settings['USER'],
    password=db_settings['PASSWORD'],
    port=db_settings.get('PORT', 5432)
)
cursor = conn.cursor()

# Vérifye si kolòn date_debut egziste
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='progress_progrescours' 
    AND column_name='date_debut'
""")
if not cursor.fetchone():
    print("Ajoute kolòn date_debut...")
    cursor.execute("""
        ALTER TABLE progress_progrescours 
        ADD COLUMN date_debut timestamp with time zone
    """)
    cursor.execute("""
        UPDATE progress_progrescours 
        SET date_debut = NOW() 
        WHERE date_debut IS NULL
    """)
    print("Kolòn date_debut ajoute.")

# Vérifye si kolòn date_modification egziste
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='progress_progrescours' 
    AND column_name='date_modification'
""")
if not cursor.fetchone():
    print("Ajoute kolòn date_modification...")
    cursor.execute("""
        ALTER TABLE progress_progrescours 
        ADD COLUMN date_modification timestamp with time zone
    """)
    cursor.execute("""
        UPDATE progress_progrescours 
        SET date_modification = NOW() 
        WHERE date_modification IS NULL
    """)
    print("Kolòn date_modification ajoute.")

# Vérifye si kolòn date_debut nan ProgresLecon
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='progress_progreslecon' 
    AND column_name='date_debut'
""")
if not cursor.fetchone():
    print("Ajoute kolòn date_debut nan ProgresLecon...")
    cursor.execute("""
        ALTER TABLE progress_progreslecon 
        ADD COLUMN date_debut timestamp with time zone
    """)
    print("Kolòn date_debut ajoute nan ProgresLecon.")

# Vérifye si kolòn date_fin nan ProgresLecon
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='progress_progreslecon' 
    AND column_name='date_fin'
""")
if not cursor.fetchone():
    print("Ajoute kolòn date_fin nan ProgresLecon...")
    cursor.execute("""
        ALTER TABLE progress_progreslecon 
        ADD COLUMN date_fin timestamp with time zone
    """)
    print("Kolòn date_fin ajoute nan ProgresLecon.")

conn.commit()
cursor.close()
conn.close()
print("Tout kolòn ki manke yo ajoute avèk siksè!")
EOF

echo "Build terminé avec succès!"