FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8080

# FIX: Removed threads to eliminate thread contention/GIL locking during bcrypt hashing.
# Increased timeout to 120 seconds just in case Cloud Run experiences cold start lag.
CMD ["gunicorn", "app.main:app", "-b", "0.0.0.0:8080", "--workers=1", "--timeout=120"]