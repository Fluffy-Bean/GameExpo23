# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY server server
CMD ["flask", "run", "--port=5000", "--host=localhost"]