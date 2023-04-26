#!/bin/bash

# Load environment variables
source .env

# Get a list of all databases that begin with 'temp_'
databases=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -t -c "SELECT datname FROM pg_database WHERE datname LIKE 'temp_%'")

# Loop over the databases and drop them
for db in $databases; do
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "DROP DATABASE $db"
done
