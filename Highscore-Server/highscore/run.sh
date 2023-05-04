#!/bin/sh

# Wait for database to start
until pg_isready -d $DB_NAME -h $DB_HOST -p $DB_PORT -U $DB_USER
do
    echo "Waiting for database to start... (5s)"
    sleep 5
done

echo "Database is ready!"

# Check if migrastions folder exists
if [ ! -d "migrations" ]
then
    echo "Creating tables..."
    flask --app server db init
fi

# Check if there are any changes to the database
if -n flask --app server db check
then
    echo "Database changes detected! Migrating..."
    flask --app server db migrate
    flask --app server db upgrade
fi

# Start server!!!!
echo "Starting server..."
gunicorn --bind highscore:8080 server:app
