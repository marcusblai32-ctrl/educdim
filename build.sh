#!/usr/bin/env bash
set -o errexit

echo "=============================================="
echo "  EDUCIM - Build & Reset Subscription"
echo "=============================================="

echo ""
echo "=== 1/3: Installation des dépendances ==="
pip install -r requirements.txt

echo ""
echo "=== 2/3: Collecte des fichiers statiques ==="
python manage.py collectstatic --noinput

echo ""
echo "=== 3/3: Reset done subscription + kreye kolòn ==="
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    # ===== EFASE DONE SUBSCRIPTION YO =====
    print('Efase SubscriptionCourseSelection...')
    try:
        cursor.execute('DELETE FROM subscriptions_subscriptioncourseselection')
    except Exception as e:
        print(f'  - Table pa ekziste, sote')
    
    print('Efase SubscriptionAccess...')
    try:
        cursor.execute('DELETE FROM subscriptions_subscriptionaccess')
    except Exception as e:
        print(f'  - Table pa ekziste, sote')
    
    print('Efase Subscription...')
    try:
        cursor.execute('DELETE FROM subscriptions_subscription')
    except Exception as e:
        print(f'  - Table pa ekziste, sote')
    
    print('Efase SubscriptionPlan.cours...')
    try:
        cursor.execute('DELETE FROM subscriptions_subscriptionplan_cours')
    except Exception as e:
        print(f'  - Table pa ekziste, sote')
    
    print('Efase SubscriptionPlan...')
    try:
        cursor.execute('DELETE FROM subscriptions_subscriptionplan')
    except Exception as e:
        print(f'  - Table pa ekziste, sote')
    
    print('')
    print('=== Kreye kolòn ki manke yo ===')
    
    cursor.execute('ALTER TABLE subscriptions_subscriptionplan ADD COLUMN IF NOT EXISTS max_courses integer NOT NULL DEFAULT 0')
    print('✅ max_courses ajoute')
    
    cursor.execute('ALTER TABLE subscriptions_subscription ADD COLUMN IF NOT EXISTS courses_selectionnes boolean NOT NULL DEFAULT false')
    print('✅ courses_selectionnes ajoute')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions_subscriptioncourseselection (
            id bigserial PRIMARY KEY,
            date_selection timestamp with time zone NOT NULL,
            course_id bigint NOT NULL REFERENCES courses_course(id) DEFERRABLE INITIALLY DEFERRED,
            subscription_id bigint NOT NULL REFERENCES subscriptions_subscription(id) DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT subscriptions_subscriptioncourseselection_unique 
            UNIQUE (subscription_id, course_id)
        )
    ''')
    print('✅ Table SubscriptionCourseSelection kreye')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS subscriptions_subscriptioncourseselection_subscription_id_idx ON subscriptions_subscriptioncourseselection (subscription_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS subscriptions_subscriptioncourseselection_course_id_idx ON subscriptions_subscriptioncourseselection (course_id)')
    print('✅ Indexes kreye')
    
    print('')
    print('✅ Done subscription efase ak kolòn kreye!')
"

echo ""
echo "=============================================="
echo "  BUILD TERMINÉ AVEC SUCCÈS"
echo "=============================================="