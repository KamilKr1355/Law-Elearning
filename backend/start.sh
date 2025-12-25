#!/bin/bash

# Zatrzymuje skrypt, jeśli jakakolwiek komenda się nie uda
set -e

echo "==> Uruchamianie migracji..."
python manage.py migrate --noinput

echo "==> Tworzenie superużytkownika (jeśli nie istnieje)..."
python manage.py createsuperuser --noinput || true

echo "==> Scrapowanie danych..."
python manage.py scrapuj_dane

echo "==> Integracja z ChatGPT..."
python manage.py chat_gtp_api

echo "==> Zbieranie plików statycznych..."
python manage.py collectstatic --noinput

echo "==> Uruchamianie serwera Gunicorn..."
exec gunicorn elearning_prawo.wsgi:application --bind 0.0.0.0:$PORT