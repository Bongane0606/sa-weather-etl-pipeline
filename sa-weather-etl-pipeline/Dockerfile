FROM python:3.10-slim

WORKDIR /app

# Install dependencies first so this layer is cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual pipeline code (imports are flat, e.g. "from db import ...",
# so everything needs to live at the same level, matching how it's run locally)
COPY weather_etl/ .

CMD ["python", "pipeline.py"]