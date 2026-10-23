FROM python:3.14-slim

WORKDIR /app

# Primero solo las dependencias: así Docker reutiliza esta capa
# si no cambió requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]