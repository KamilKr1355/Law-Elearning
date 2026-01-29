# Law-Elearning 
Login admina: administrator
haslo: admin1234

Login usera: user1
haslo: user1234

Projekt składa się z:

backend/ – Django + Gunicorn

frontend/ – React (budowany i serwowany przez Nginx)

PostgreSQL – baza danych

docker

# Wymagania
   
Docker Desktop

Git

# Plik .env (w katalogu głównym projektu)

Utwórz .env i wklej:

POSTGRES_DB=elearning

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

DB_HOST=db

DB_PORT=5432

SECRET_KEY=zmien_to_na_swoj - pip install django, python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"


OpenAI (jeśli używasz komend scrapingowych)
OPENAI_API_KEY=sk-xxxxx

# Uruchamianie projektu
Pierwsze uruchomienie 
docker-compose up --build -d

Kolejne uruchomienia 
docker-compose up -d

Zatrzymywanie:
docker-compose down

# Migracje bazy danych
docker-compose exec web python manage.py migrate

# Tworzenie superusera

docker-compose exec web python manage.py createsuperuser

# Uruchamianie komend Django (np. scraping)

Każda komenda z management/commands:

docker-compose exec web python manage.py nazwa_komendy


Przykład:

docker-compose exec web python manage.py scrapuj_dane

# Dostęp do aplikacji

Frontend (React + Nginx):
http://localhost

Backend (Django API):
http://localhost:8000



