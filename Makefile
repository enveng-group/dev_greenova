.PHONY: check run migrations migrate static user db import sync clean-csv lint-templates format-templates check-templates format-lint

# Change to greenova directory before running commands
CD_CMD = cd greenova &&

check:
	$(CD_CMD) python3.9 manage.py check

run:
	$(CD_CMD) python3.9 manage.py runserver

migrations:
	$(CD_CMD) python3.9 manage.py makemigrations

migrate:
	$(CD_CMD) python3.9 manage.py migrate

static:
	$(CD_CMD) python3.9 manage.py collectstatic --clear --noinput

user:
	$(CD_CMD) python3.9 manage.py createsuperuser

import:
	$(CD_CMD) python3.9 manage.py import_obligations clean_output_with_nulls.csv

sync:
	$(CD_CMD) python3.9 manage.py sync_mechanisms

clean-csv:
	$(CD_CMD) python manage.py clean_csv_to_import dirty.csv

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
	@echo "  make check        - Run Django system check framework"
	@echo "  make check-templates  - Check template formatting without changes"
	@echo "  make format-templates - Format Django template files"
	@echo "  make lint-templates   - Lint Django template files"
	@echo "  make import       - Import data from CSV file"
	@echo "  make sync          - Sync mechanisms"
	@echo "  make clean-csv     - Clean CSV file"
	@echo "  make user         - Create superuser"
	@echo "  make db           - Run both migrations and migrate"
	@echo "  make static       - Collect static files (with --clear)"
	@echo "  make migrate      - Apply migrations"
	@echo "  make migrations   - Create new migrations"
	@echo "  make run          - Start development server"
