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
# AJOUTE KOLÒN KI MANKE YO AK DJANGO
# ============================================
python manage.py shell << 'EOF'
from django.db import connection

def add_column_if_not_exists(table, column, column_type):
    with connection.cursor() as cursor:
        # Verifye si kolòn egziste
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name=%s AND column_name=%s
        """, [table, column])
        if not cursor.fetchone():
            print(f"Ajoute kolòn {column} nan {table}...")
            cursor.execute(f"""
                ALTER TABLE {table} ADD COLUMN {column} {column_type}
            """)
            
            # Mete valè default pou kolòn yo
            if column in ['date_debut', 'date_modification']:
                cursor.execute(f"""
                    UPDATE {table} SET {column} = NOW() WHERE {column} IS NULL
                """)
            
            print(f"Kolòn {column} ajoute.")

# Kolòn nan ProgresCours
add_column_if_not_exists('progress_progrescours', 'date_debut', 'timestamp with time zone')
add_column_if_not_exists('progress_progrescours', 'date_modification', 'timestamp with time zone')

# Kolòn nan ProgresLecon
add_column_if_not_exists('progress_progreslecon', 'date_debut', 'timestamp with time zone')
add_column_if_not_exists('progress_progreslecon', 'date_fin', 'timestamp with time zone')

print("Tout kolòn ki manke yo ajoute avèk siksè!")
EOF

echo "Build terminé avec succès!"