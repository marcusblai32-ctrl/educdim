#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🗄️  Exécution des migrations..."
python manage.py makemigrations
python manage.py migrate

# ============================================
# AJOUTE TAB ACTIVITEUTILISATEUR AVEC PYTHON
# ============================================
echo "🔧 Vérification de la table ActiviteUtilisateur..."
python manage.py shell << 'EOF'
from django.db import connection

def create_table_if_not_exists():
    with connection.cursor() as cursor:
        # Verifye si tab egziste
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='progress_activiteutilisateur'
            )
        """)
        exists = cursor.fetchone()[0]
        
        if not exists:
            print("Kreye tab progress_activiteutilisateur...")
            cursor.execute("""
                CREATE TABLE progress_activiteutilisateur (
                    id bigserial NOT NULL PRIMARY KEY,
                    utilisateur_id integer NOT NULL,
                    type_activite varchar(30) NOT NULL,
                    description text NOT NULL,
                    cours_id integer,
                    lecon_id integer,
                    date timestamp with time zone NOT NULL
                )
            """)
            
            # Foreign keys
            cursor.execute("""
                ALTER TABLE progress_activiteutilisateur ADD CONSTRAINT 
                progress_activiteutilisateur_utilisateur_id_fkey 
                FOREIGN KEY (utilisateur_id) REFERENCES accounts_customuser(id)
            """)
            
            cursor.execute("""
                ALTER TABLE progress_activiteutilisateur ADD CONSTRAINT 
                progress_activiteutilisateur_cours_id_fkey 
                FOREIGN KEY (cours_id) REFERENCES courses_course(id)
            """)
            
            cursor.execute("""
                ALTER TABLE progress_activiteutilisateur ADD CONSTRAINT 
                progress_activiteutilisateur_lecon_id_fkey 
                FOREIGN KEY (lecon_id) REFERENCES courses_lecon(id)
            """)
            
            # Index
            cursor.execute("""
                CREATE INDEX progress_activiteutilisateur_utilisateur_id_idx 
                ON progress_activiteutilisateur(utilisateur_id)
            """)
            cursor.execute("""
                CREATE INDEX progress_activiteutilisateur_cours_id_idx 
                ON progress_activiteutilisateur(cours_id)
            """)
            cursor.execute("""
                CREATE INDEX progress_activiteutilisateur_lecon_id_idx 
                ON progress_activiteutilisateur(lecon_id)
            """)
            cursor.execute("""
                CREATE INDEX progress_activiteutilisateur_date_idx 
                ON progress_activiteutilisateur(date)
            """)
            
            print("✅ Tab progress_activiteutilisateur kreye avèk siksè!")
        else:
            print("✅ Tab progress_activiteutilisateur deja egziste.")

create_table_if_not_exists()
print("✅ Tout tab vérifiées avèk siksè!")
EOF

echo "✅ Build terminé avec succès!"