#!/bin/sh

# Wait for database to start
until pg_isready -d $DB_NAME -h $DB_HOST -U $DB_USER
do
    echo "Waiting for database to start... (5s)"
    sleep 5
done

echo "Database is ready!"

# Check if migrastions folder exists
if [ ! -d "/data/storage/migrations" ];
then
    echo "Creating tables..."
    flask --app server db init
fi

# Check if there are any changes to the database
if ! $(flask --app server db check | grep -q "No changes in schema detected.");
then
    echo "Database changes detected! Migrating..."
    flask --app server db migrate
    flask --app server db upgrade
fi

# Start server!!!!
echo "Starting server..."
gunicorn --bind tfr:8000 server:app
# flask --app server run --port 8000 --host tfr
