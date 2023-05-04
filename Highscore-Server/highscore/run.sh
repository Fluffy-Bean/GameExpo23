#!/bin/sh

until pg_isready -d $DB_NAME -h $DB_HOST -p $DB_PORT -U $DB_USER
do
    echo "Waiting for database to start... (5s)"
    sleep 5
done

echo "Database is ready! Creating tables..."
flask --app server db init

if [ -n flask --app server db check ]; then
    echo "Database changes detected! Migrating..."
    flask --app server db migrate
    flask --app server db upgrade
fi

echo "Starting server..."
gunicorn --bind highscore:8080 server:app
