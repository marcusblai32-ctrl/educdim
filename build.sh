#!/bin/bash

echo "==========================================="
echo "BUILD: Kòmanse pwosesis build"
echo "==========================================="

# ==========================================
# 1. ENSTALE DEPANDANS
# ==========================================
echo "==========================================="
echo "BUILD: Enstale depandans"
echo "==========================================="
pip install -r requirements.txt

# ==========================================
# 2. EFASE ANSYEN DOSYE LOCALE
# ==========================================
echo "==========================================="
echo "BUILD: Efase ansyen dosye locale"
echo "==========================================="
rm -rf locale/
echo "Ansyen dosye locale efase!"

# ==========================================
# 3. KREYE NOUVO FICHYE TRADIKSYON
# ==========================================
echo "==========================================="
echo "BUILD: Kreye nouvo fichye tradiksyon"
echo "==========================================="
python manage.py makemessages -l fr -l ht --keep-pot

# ==========================================
# 4. KORIJE PLURAL-FORMS
# ==========================================
echo "==========================================="
echo "BUILD: Korije Plural-Forms"
echo "==========================================="
python -c "
import os

for lang in ['fr', 'ht']:
    po_file = f'locale/{lang}/LC_MESSAGES/django.po'
    
    if not os.path.exists(po_file):
        print(f'Fichye {po_file} pa egziste, sote...')
        continue
    
    print(f'Korije: {po_file}')
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Korije Plural-Forms
    content = content.replace(
        'Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;',
        'Plural-Forms: nplurals=2; plural=(n != 1);'
    )
    
    # Retire flag fuzzy ki ka kreye pwoblèm
    content = content.replace('#, fuzzy\n', '')
    
    # Korije Language field
    content = content.replace(
        'Language: \\\\n',
        f'Language: {lang}\\\\n'
    )
    
    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Korije ak siksè: {po_file}')
"

# ==========================================
# 5. KONPILE TRADIKSYON YO
# ==========================================
echo "==========================================="
echo "BUILD: Konpile tradiksyon yo"
echo "==========================================="
python manage.py compilemessages

# ==========================================
# 6. KOLEKTE STATIK
# ==========================================
echo "==========================================="
echo "BUILD: Kolekte fichye statik yo"
echo "==========================================="
python manage.py collectstatic --noinput

echo "==========================================="
echo "BUILD: Pwosesis build fini ak siksè!"
echo "==========================================="