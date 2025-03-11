.PHONY: app check run run-django run-tailwind dev check-tailwind tailwind tailwind-install migrations migrate static user db import update sync update-update_recurring-inspection-dates normalize-frequencies clean-csv prod lint-templates format-templates check-templates format-lint

# Change to greenova directory before running commands
CD_CMD = cd greenova &&

app:
	@if [ -z "$(name)" ]; then echo "Error: Please provide app name with 'make app name=yourappname'"; exit 1; fi
	$(CD_CMD) python3 manage.py startapp $(name)

check:
	$(CD_CMD) python3 manage.py check

# Updated run command with better process management
run:
	@echo "Starting Tailwind CSS and Django server..."
	@$(CD_CMD) (python manage.py tailwind start > logs/tailwind.log 2>&1 & echo "Tailwind started (logs in logs/tailwind.log)") && python manage.py runserver

# Alternative approach with separate commands
run-django:
	$(CD_CMD) python manage.py runserver

run-tailwind:
	$(CD_CMD) python manage.py tailwind start

# Run command for development - opens two terminal tabs (for Mac/Linux)
dev:
	@echo "Starting development environment..."
	@gnome-terminal --tab -- bash -c "$(CD_CMD) python manage.py tailwind start; bash" 2>/dev/null || \
	xterm -e "$(CD_CMD) python manage.py tailwind start" 2>/dev/null || \
	osascript -e 'tell app "Terminal" to do script "cd $(shell pwd)/greenova && python manage.py tailwind start"' 2>/dev/null || \
	echo "Could not open terminal automatically. Please run 'make run-tailwind' in a separate terminal."
	@$(CD_CMD) python manage.py runserver

# Check Tailwind installation status
check-tailwind:
	$(CD_CMD) python manage.py tailwind check-updates

# Tailwind commands
tailwind:
	$(CD_CMD) python manage.py tailwind build

# Add a tailwind install command
tailwind-install:
	$(CD_CMD) python manage.py tailwind install

migrations:
	$(CD_CMD) python3 manage.py makemigrations

migrate:
	$(CD_CMD) python3 manage.py migrate

static:
	$(CD_CMD) python3 manage.py collectstatic --clear --noinput

user:
	$(CD_CMD) python3 manage.py createsuperuser

import:
	$(CD_CMD) python3 manage.py import_obligations clean_output_with_nulls.csv

update:
	$(CD_CMD) python3 manage.py import_obligations clean_output_with_nulls.csv --force-update

sync:
	$(CD_CMD) python3 manage.py sync_mechanisms

update-recurring-dates:
	$(CD_CMD) python3 manage.py update-recurring-inspection-dates

normalize-frequencies:
	$(CD_CMD) python3 manage.py normalize_existing_frequencies

clean-csv:
	$(CD_CMD) python3 manage.py clean_csv_to_import dirty.csv

prod:
	$(CD_CMD) /bin/sh scripts/prod_urls.sh

# Used to pre-compile tailwind CSS before running the application (we should maybe use this in run later)
tailwind:
	$(CD_CMD) python3 manage.py tailwind start

# Combined command for database updates
db: migrations migrate

# Template linting commands
lint-templates:
	djlint greenova/**/templates --lint

format-templates:
	djlint greenova/**/templates --reformat

check-templates:
	djlint greenova/**/templates --check

# Combined command for formatting and linting
format-lint: format-templates lint-templates

# Help command to list available commands
help:
	@echo "Available commands:"
	@echo "  make app name=appname - Create a new Django app with the specified name"
	@echo "  make check        - Run Django system check framework"
	@echo "  make check-templates  - Check template formatting without changes"
	@echo "  make format-templates - Format Django template files"
	@echo "  make prod         - Run production server"
	@echo "  make lint-templates   - Lint Django template files"
	@echo "  make import       - Import data from CSV file"
	@echo "  make update       - Update data from CSV file"
	@echo "  make sync          - Sync mechanisms"
	@echo "  make update-recurring-dates - Update recurring inspection dates"
	@echo "  make normalize-frequencies - Normalize existing frequencies"
	@echo "  make clean-csv     - Clean CSV file"
	@echo "  make user         - Create superuser"
	@echo "  make db           - Run both migrations and migrate"
	@echo "  make static       - Collect static files (with --clear)"
	@echo "  make migrate      - Apply migrations"
	@echo "  make migrations   - Create new migrations"
	@echo "  make run          - Start development server"
	@echo "  make tailwind     - Start Tailwind CSS server"
