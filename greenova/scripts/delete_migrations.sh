#!/bin/sh

# Directories containing migration files
MIGRATION_DIRS="
greenova/chatbot/migrations
greenova/company/migrations
greenova/mechanisms/migrations
greenova/obligations/migrations
greenova/projects/migrations
greenova/procedures/migrations
greenova/responsibility/migrations
greenova/users/migrations
"

# Loop through each directory
for dir in $MIGRATION_DIRS; do
  if [ -d "$dir" ]; then
    echo "Cleaning migration files in $dir"
    find "$dir" -type f ! -name "__init__.py" -name "*.py" -delete
    find "$dir" -type f -name "*.pyc" -delete
  else
    echo "Directory $dir does not exist, skipping."
  fi
done

echo "Migration cleanup completed."
