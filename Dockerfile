# ETAP 1: build_base - Budowanie zależności Pythona
FROM python:3.11-slim as builder

# Ustawienie zmiennych środowiskowych
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie tylko pliku zależności i instalacja ich (wykorzystuje cache)
# Wymaga, aby w requirements.txt znajdował się psycopg2-binary, a nie psycopg2
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ETAP 2: Produkcyjny obraz (Minimalistyczny)
FROM python:3.11-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zainstalowanych zależności Pythona (biblioteki)
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# KLUCZOWA POPRAWKA: Kopiowanie binarek (np. gunicorn, django-admin) do ścieżki $PATH
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Kopiowanie kodu aplikacji
COPY . /app/

# Otwarcie portu, na którym działa aplikacja
EXPOSE 8000

# Komenda uruchamiająca aplikację (serwer produkcyjny Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "elearning_prawo.wsgi:application"]