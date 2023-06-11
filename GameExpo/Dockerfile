# syntax=docker/dockerfile:1
FROM alpine:latest

EXPOSE 5000
RUN apk update && apk add python3 py3-pip
WORKDIR /data

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /storage
COPY ./website ./website
COPY ./run.sh ./run.sh
RUN chmod +x ./run.sh

CMD ["./run.sh"]
