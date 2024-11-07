FROM apache/airflow:2.10.3
COPY requirements.txt .
run pip install -r requirements.txt

FROM jenkins/jenkins:jdk17
EXPOSE 9090
ONBUILD ENV JENKINS_HTTP_PORT=9090

