FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante que a pasta existe
RUN mkdir -p /app/data

EXPOSE 8000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "wsgi:app"]
