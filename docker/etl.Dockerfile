FROM python:3.10-slim

WORKDIR /app

# Install dependencies first so this layer is cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --retries 5 -r requirements.txt

# The ETL modules import each other flat ("from db import ..."), so the
# contents of backend/etl/ are copied directly into /app.
COPY backend/etl/ .

CMD ["python", "pipeline.py"]
