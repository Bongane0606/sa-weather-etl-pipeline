FROM python:3.11-slim
WORKDIR /app

COPY backend/api/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --retries 5 -r requirements.txt

COPY backend/api/app.py .
# The frontend is served by Flask from /app/static
COPY frontend/ ./static/

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
