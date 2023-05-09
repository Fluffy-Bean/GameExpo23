# syntax=docker/dockerfile:1
FROM ubuntu:22.04

EXPOSE 8080
RUN apt update && apt install -y python3 python3-pip postgresql-client
WORKDIR /data

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /storage
COPY ./server ./server
COPY ./run.sh ./run.sh
RUN chmod +x ./run.sh

CMD ["./run.sh"]
