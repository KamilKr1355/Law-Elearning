FROM python:3.11-slim

# Ustawienia Pythona
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Kopiowanie zależności
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu
COPY . /app/

# Port Django
EXPOSE 8000

# Uruchomienie Gunicorn
CMD gunicorn elearning_prawo.wsgi:application --bind 0.0.0.0:$PORT
