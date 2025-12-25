#!/bin/bash
set -e

echo "==> Uruchamianie migracji..."
python manage.py migrate --noinput

echo "==> Tworzenie superużytkownika..."
python manage.py createsuperuser --noinput || true

# Uruchamiamy skrypty jeden po drugim, ale całą grupę wysyłamy w tło
run_scripts() {
    echo "==> Start scrapowania..."
    python manage.py scrapuj_dane
    echo "==> Start AI..."
    python manage.py chat_gtp_api
}

run_scripts & # To uruchomi oba skrypty po kolei w tle

echo "==> Uruchamianie serwera Gunicorn..."
exec gunicorn elearning_prawo.wsgi:application --bind 0.0.0.0:$PORT