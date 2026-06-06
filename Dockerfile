FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8080

# FIXED: Added 2 workers and 4 threads to stop database connections from blocking the server
CMD ["gunicorn", "app.main:app", "-b", "0.0.0.0:8080", "--workers=1", "--threads=2", "--timeout=90"]