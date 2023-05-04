# syntax=docker/dockerfile:1
FROM python:3.10-alpine

EXPOSE 8080
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /data

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /storage
COPY /highscore/ .

CMD ["gunicorn", "--bind", "highscore:8080", "server:app"]
