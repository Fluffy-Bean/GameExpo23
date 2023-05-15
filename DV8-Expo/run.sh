#!/bin/sh

# Check if migrastions folder exists
if [ ! -d "/data/storage/migrations" ];
then
    echo "Creating tables..."
    flask --app website db init
fi

# Check if there are any changes to the database
if ! $(flask --app website db check | grep -q "No changes in schema detected.");
then
    echo "Database changes detected! Migrating..."
    flask --app website db migrate
    flask --app website db upgrade
fi

# Start website!!!!
echo "Starting expo website..."
gunicorn --bind expo:5000 website:app
