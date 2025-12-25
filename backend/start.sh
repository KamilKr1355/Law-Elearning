#!/bin/bash
set -e

echo "==> Uruchamianie migracji..."
python manage.py migrate --noinput

echo "==> Tworzenie superużytkownika..."
python manage.py createsuperuser --noinput || true

# KLUCZOWA ZMIANA: Uruchamiamy ciężkie skrypty w tle za pomocą '&'
echo "==> Uruchamianie skryptów w tle (aby nie blokować startu)..."
python manage.py scrapuj_dane &
python manage.py chat_gpt_api &

echo "==> Uruchamianie serwera Gunicorn..."
# exec sprawia, że Gunicorn staje się głównym procesem kontenera
exec gunicorn elearning_prawo.wsgi:application --bind 0.0.0.0:$PORT