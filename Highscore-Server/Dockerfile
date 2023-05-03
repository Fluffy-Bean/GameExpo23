# syntax=docker/dockerfile:1
FROM python:3.10-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /data/requirements.txt
WORKDIR /data
RUN pip install -r requirements.txt
RUN mkdir /highscore
COPY /highscore /highscore
WORKDIR /highscore
EXPOSE 5000
CMD ["gunicorn", "-b", "localhost:5000", "server:app"]
