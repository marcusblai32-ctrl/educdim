#!/bin/bash

# ============================================
# SCRIPT: Reset Locale Files
# Efase ansyen locale sou GitHub epi rekreye
# Korije Plural-Forms otomatikman
# ============================================

echo "============================================"
echo " RESET LOCALE FILES"
echo "============================================"

# Ale nan bon dosye
cd "$(dirname "$0")"

# ============================================
# 1. Efase ansyen locale/ sou GitHub
# ============================================
echo ""
echo "[1/8] Efase ansyen locale/ sou GitHub..."
git rm -r --cached locale/ 2>/dev/null || echo "Aucun locale/ à effacer"
git commit -m "Efase ansyen dosye locale" 2>/dev/null || echo "Rien à commit"
git push origin main

# ============================================
# 2. Rekòmanse makemessages
# ============================================
echo ""
echo "[2/8] Rekòmanse makemessages..."
python manage.py makemessages -l ht -l fr

# ============================================
# 3. Korije Plural-Forms pou Kreyòl
# ============================================
echo ""
echo "[3/8] Korije Plural-Forms pou Kreyòl..."

ht_file="locale/ht/LC_MESSAGES/django.po"
fr_file="locale/fr/LC_MESSAGES/django.po"

# Korije pou ht
if [ -f "$ht_file" ]; then
    # Chanje INTEGER ak EXPRESSION pou bon valè
    sed -i 's/nplurals=INTEGER; plural=EXPRESSION;/nplurals=2; plural=(n != 1);/' "$ht_file"
    sed -i 's/nplurals=INTEGER; plural=EXPRESSION;/nplurals=2; plural=(n != 1);/' "$ht_file"
    echo "✅ Plural-Forms ht korije"
else
    echo "⚠️ Fichye $ht_file pa egziste"
fi

# Korije pou fr (si bezwen)
if [ -f "$fr_file" ]; then
    sed -i 's/nplurals=INTEGER; plural=EXPRESSION;/nplurals=2; plural=(n > 1);/' "$fr_file"
    echo "✅ Plural-Forms fr korije"
else
    echo "⚠️ Fichye $fr_file pa egziste"
fi

# Verifye korèksyon an
echo ""
echo "Verifye Plural-Forms:"
grep "Plural-Forms" "$ht_file" 2>/dev/null || echo "ht: pa jwenn"
grep "Plural-Forms" "$fr_file" 2>/dev/null || echo "fr: pa jwenn"

# ============================================
# 4. Kouri script tradui_ht.py si li egziste
# ============================================
echo ""
echo "[4/8] Kouri script tradui_ht.py..."
if [ -f "tradui_ht.py" ]; then
    python tradui_ht.py
else
    echo "⚠️ tradui_ht.py pa egziste, sote etap sa a"
fi

# ============================================
# 5. Re-korije Plural-Forms apre tradui_ht.py
# ============================================
echo ""
echo "[5/8] Re-korije Plural-Forms apre tradiksyon..."

if [ -f "$ht_file" ]; then
    sed -i 's/nplurals=INTEGER; plural=EXPRESSION;/nplurals=2; plural=(n != 1);/' "$ht_file"
    echo "✅ Plural-Forms ht re-korije"
fi

if [ -f "$fr_file" ]; then
    sed -i 's/nplurals=INTEGER; plural=EXPRESSION;/nplurals=2; plural=(n > 1);/' "$fr_file"
    echo "✅ Plural-Forms fr re-korije"
fi

# ============================================
# 6. Konpile mesaj yo
# ============================================
echo ""
echo "[6/8] Konpile mesaj yo..."
python manage.py compilemessages

# ============================================
# 7. Ajoute nouvo locale/
# ============================================
echo ""
echo "[7/8] Ajoute nouvo locale/..."
git add locale/

# ============================================
# 8. Commit epi pouse
# ============================================
echo ""
echo "[8/8] Kreye commit epi pouse..."
git commit -m "Rekreye tradiksyon Kreyòl ak Franse ak korije Plural-Forms"
git push origin main

echo ""
echo "============================================"
echo " ✅ FINI! Tradiksyon yo te rekreye."
echo " ✅ Plural-Forms korije otomatikman."
echo "============================================"