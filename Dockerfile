FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8080

# FIXED: Changed "app:app" to "main:app" so Gunicorn boots from main.py
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8080"]