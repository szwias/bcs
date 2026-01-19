FROM python:3.12-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (psycopg2, pillow, graphviz)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY bcs/requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY bcs /app

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn bcs.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
