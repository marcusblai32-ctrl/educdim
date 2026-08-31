#!/bin/bash

echo "============================================"
echo " RESET LOCALE FILES"
echo "============================================"

cd "$(dirname "$0")"

# 1. Efase ansyen locale sou GitHub
echo "[1/6] Efase ansyen locale..."
git rm -r --cached locale/ 2>/dev/null
git commit -m "Efase ansyen locale" 2>/dev/null
git push origin main

# 2. Rekòmanse makemessages
echo "[2/6] Rekòmanse makemessages..."
python manage.py makemessages -l ht -l fr

# 3. Korije Plural-Forms ak Python
echo "[3/6] Korije Plural-Forms..."
cat > /tmp/fix_plural.py << 'EOF'
import re

for lang, plural in [('ht', 'nplurals=2; plural=(n != 1);'), ('fr', 'nplurals=2; plural=(n > 1);')]:
    filepath = f'locale/{lang}/LC_MESSAGES/django.po'
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            contenu = f.read()
        contenu = re.sub(r'nplurals=INTEGER; plural=EXPRESSION;', plural, contenu)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print(f"✅ {lang} korije")
    except Exception as e:
        print(f"⚠️ {lang}: {e}")
EOF
python /tmp/fix_plural.py

# 4. Kouri tradui_ht.py
echo "[4/6] Kouri tradui_ht.py..."
if [ -f "tradui_ht.py" ]; then
    python tradui_ht.py
fi

# 5. Konpile
echo "[5/6] Konpile..."
python manage.py compilemessages

# 6. Pouse
echo "[6/6] Pouse..."
git add locale/
git commit -m "Rekreye tradiksyon ak korije Plural-Forms"
git push origin main

echo "✅ FINI!"