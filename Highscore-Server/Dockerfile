# syntax=docker/dockerfile:1
FROM python:3.10-alpine

EXPOSE 8080
RUN apk add --no-cache postgresql-client build-base
WORKDIR /data

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /storage
COPY ./server .
RUN chmod +x ./run.sh

CMD ["./run.sh"]
