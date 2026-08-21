#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

# Fè migrasyon
python manage.py makemigrations
python manage.py migrate

# Ajoute kolòn nan si li pa egziste
python manage.py dbshell << EOF
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='quiz_reponseutilisateur' 
                   AND column_name='points_attribues') THEN
        ALTER TABLE quiz_reponseutilisateur ADD COLUMN points_attribues decimal(5,2) NULL;
    END IF;
END \$\$;
EOF