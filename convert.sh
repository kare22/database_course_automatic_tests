#!/bin/bash
echo $DB_HOST
echo $DB_NAME
# Go to desired directory
cd "$1"

# Cleanup
rm -rf temp
rm -f *.sql

# Create temp folder
mkdir temp

# Find all files in the current directory that don't end with ".md" or ".sh" or ".sql", and apply pg_restore to each file
find . -maxdepth 1 -type f ! -name '*.sh' ! -name '*.md' ! -name '*.sql' -exec sh -c 'pg_restore -f "temp/${1%.backup}.sql" "$1"' sh {} \;

cd temp

# Loop through all SQL files in the current directory
for file in *.sql
do
  # Generate a unique database name
  DB_NAME="new_$(date +%s%N)"

  # Set dump file location
  PSQL_DUMP_FILE="$file"

  # Set backup file name
  BACKUP_FILE="../${file%.*}.sql"

  # Create new database
  createdb -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -w "$DB_NAME"

  # Restore data from psql dump
  psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -w "$DB_NAME" < "$PSQL_DUMP_FILE"

  # Create backup using inserts only
  pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -w --inserts "$DB_NAME" > "$BACKUP_FILE"

  # Delete the database
  dropdb -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -w "$DB_NAME"
done