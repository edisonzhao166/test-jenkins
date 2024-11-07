FROM apache/airflow:2.10.3
COPY requirements.txt .
run pip install -r requirements.txt