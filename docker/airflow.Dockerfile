FROM apache/airflow:2.9.3-python3.10
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 --retries 5 -r /requirements.txt