# ETAP 1: Budowanie (dla zależności)
FROM python:3.11-slim as builder

# Ustawienie zmiennych środowiskowych
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie tylko pliku zależności i instalacja ich (wykorzystuje cache)
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ETAP 2: Produkcyjny obraz
FROM python:3.11-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zainstalowanych zależności z etapu budowania
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Kopiowanie kodu aplikacji
COPY . /app/

# Otwarcie portu, na którym działa aplikacja (standardowo Django)
EXPOSE 8000

# Komenda uruchamiająca aplikację (w środowisku produkcyjnym często używa się Gunicorn lub uWSGI)
# Przykład z Gunicorn:
# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "nazwa_twojego_projektu.wsgi:application"]

# Przykład dla developmentu (z użyciem runserver):
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "elearning_prawo.wsgi:application"]