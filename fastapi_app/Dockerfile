FROM python:3.12-slim

ARG APP_NAME=main.py

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python ${APP_NAME}
