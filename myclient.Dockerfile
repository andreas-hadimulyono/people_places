FROM python:latest

WORKDIR /app

COPY script.py .
COPY *.csv /data/

RUN pip install mysql-connector-python pandas

ENV MYSQL_HOST=mydb
ENV MYSQL_PORT=3306
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=password
ENV MYSQL_DB=people_places

