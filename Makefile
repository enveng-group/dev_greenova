.PHONY: check run migrations migrate static user db import

# Change to greenova directory before running commands
CD_CMD = cd greenova &&

check:
	$(CD_CMD) python manage.py check

run:
	$(CD_CMD) python manage.py runserver

migrations:
	$(CD_CMD) python manage.py makemigrations

migrate:
	$(CD_CMD) python manage.py migrate

static:
	$(CD_CMD) python manage.py collectstatic --clear --noinput

user:
	$(CD_CMD) python manage.py createsuperuser

import:
	$(CD_CMD) python manage.py import_obligations clean_output_with_nulls.csv

# Combined command for database updates
db: migrations migrate

# Help command to list available commands
help:
	@echo "Available commands:"
	@echo "  make check        - Run Django system check framework"
	@echo "  make run          - Start development server"
	@echo "  make migrations   - Create new migrations"
	@echo "  make migrate      - Apply migrations"
	@echo "  make static       - Collect static files (with --clear)"
	@echo "  make db           - Run both migrations and migrate"
	@echo "  make user         - Create superuser"
	@echo "  make import       - Import data from CSV file"
