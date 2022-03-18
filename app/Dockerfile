# syntax=docker/dockerfile:1

FROM python:3.11.0a6-buster

WORKDIR app/
COPY . .
RUN pip3 install -r requirements.txt

# create tables if they don't exist
#CMD ["python3","create_sql_tables.py"]

# after table creation, fire up the server
#CMD ["python3", "main.py"]

CMD ["sh", "startup.sh"]
