# syntax=docker/dockerfile:1
FROM alpine:3.18.2

EXPOSE 8000
WORKDIR /data
RUN mkdir /storage&& \
    apk update && \
    apk --no-cache add python3 py3-pip postgresql-client

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server ./server
COPY ./run.sh ./run.sh
RUN chmod +x ./run.sh

CMD ["./run.sh"]
