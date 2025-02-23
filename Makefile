.PHONY: all check run migrations migrate static lint test security clean help

# Project variables
PYTHON_INTERPRETER = $(shell pipenv run which python)
WORKSPACE_FOLDER = greenova

# Change to greenova directory before running commands
CD_CMD = cd $(WORKSPACE_FOLDER) &&

# Linting and formatting
lint-black:
    $(CD_CMD) pipenv run black .

lint-isort:
    $(CD_CMD) pipenv run isort .

lint-pylint:
    $(CD_CMD) pipenv run pylint --rcfile=.pylintrc --load-plugins=pylint_django --django-settings-module=greenova.settings .

lint-eslint:
    $(CD_CMD) npx eslint --config .eslintrc .

lint-shell:
    shellcheck --shell=sh --format=gcc scripts/*.sh

lint: lint-black lint-isort lint-pylint lint-eslint lint-shell

# Type checking
typecheck:
    $(CD_CMD) pipenv run mypy --config-file=mypy.ini .

# Security checks
security-bandit:
    $(CD_CMD) pipenv run bandit -c .bandit -r .

security-devskim:
    devskim analyze --config-path .devskim/config.json --output-file .devskim/scan-results.json --output-format json .

security: security-bandit security-devskim

# Django commands
check:
    $(CD_CMD) pipenv run python manage.py check

run:
    $(CD_CMD) pipenv run python manage.py runserver

migrations:
    $(CD_CMD) pipenv run python manage.py makemigrations

migrate:
    $(CD_CMD) pipenv run python manage.py migrate

static:
    $(CD_CMD) pipenv run python manage.py collectstatic --clear --noinput

test:
    $(CD_CMD) pipenv run python manage.py test

shell:
    $(CD_CMD) pipenv run python manage.py shell

# Combined commands
db: migrations migrate

all: lint typecheck security test

clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type d -name "node_modules" -exec rm -rf {} +
    find . -type d -name ".mypy_cache" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    rm -rf .coverage htmlcov

help:
    @echo "Available commands:"
    @echo "Development:"
    @echo "  make run          - Start development server"
    @echo "  make shell        - Start Django shell"
    @echo "Database:"
    @echo "  make migrations   - Create new migrations"
    @echo "  make migrate      - Apply migrations"
    @echo "  make db          - Run both migrations and migrate"
    @echo "Static files:"
    @echo "  make static       - Collect static files"
    @echo "Quality checks:"
    @echo "  make lint         - Run all linters"
    @echo "  make typecheck    - Run type checks"
    @echo "  make security     - Run security checks"
    @echo "  make test         - Run tests"
    @echo "  make all          - Run all checks"
    @echo "Cleanup:"
    @echo "  make clean        - Remove temporary files"
