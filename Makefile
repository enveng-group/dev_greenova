.PHONY: app install venv dotenv-pull dotenv-push check run run-django run-tailwind compile-proto check-tailwind tailwind tailwind-install update update-recurring-dates normalize-frequencies clean-csv prod lint-templates format-templates check-templates format-lint

# Change to greenova directory before running commands
CD_CMD = cd greenova &&

# Define the virtual environment path
VENV = .venv

# Define the pthon and pip path
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

#Variables
REQUIREMENTS=requirements.txt
CONSTRAINTS=constraints.txt
SETUP_SCRIPT=setup.py

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV)
	@echo "Virtual environment created."
	@echo "To activate it, run: source .venv/bin/activate"

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS) -c $(CONSTRAINTS)
	@echo "Dependencies installed."

#Freeze installed dependencies to requirements.txt
freeze:
	@echo "Freezing dependencies..."
	$(VENV)/bin/pip freeze > $(REQUIREMENTS)
	@echo "Dependencies frozen."

#Create a Django new app
app:
	@if [ -z "$(name)" ]; then echo "Error: Please provide app name with 'make app name=yourappname'"; exit 1; fi
	$(CD_CMD) python3 manage.py startapp $(name)

#pull .env file from dotenv-vault
dotenv-pull:
	@echo "Pulling .env file from dotenv-vault"
	@npx dotenv-vault@latest pull

#push .env file to dotenv-vault
dotenv-push:
	@echo "Pushing .env file to dotenv-vault"
	@npx dotenv-vault@latest push

#run django system check
check:
	$(CD_CMD) python3 manage.py check

# Updated run command with better process management and gunicorn config
run:
	@echo "Starting Tailwind CSS and Django server..."
	@mkdir -p logs
	@$(CD_CMD) (python3 manage.py tailwind start > ../logs/tailwind.log 2>&1 & echo "Tailwind started (logs in logs/tailwind.log)") && \
	python3 manage.py runserver

# Alternative approach with separate commands
#start only Django server
run-django:
	$(CD_CMD) gunicorn greenova.wsgi -c ../gunicorn.conf.py

#Start only Tailwind CSS
run-tailwind:
	$(CD_CMD) python3 manage.py tailwind start

# Check Tailwind installation status
check-tailwind:
	$(CD_CMD) python3 manage.py tailwind check-updates

# Tailwind commands
#Build tailwind CSS
tailwind-build:
	$(CD_CMD) python3 manage.py tailwind build

# Add a tailwind install command
tailwind-install:
	$(CD_CMD) python3 manage.py tailwind install

#Update data from CSV file
update:
	$(CD_CMD) python3 manage.py import_obligations dummy_data.csv --force-update

#Update recurring inspection dates
update-recurring-dates:
	$(CD_CMD) python3 manage.py update-recurring-inspection-dates

#Normalize existing frequencies
normalize-frequencies:
	$(CD_CMD) python3 manage.py normalize_existing_frequencies

#Clean CSV file
clean-csv:
	$(CD_CMD) python3 manage.py clean_csv_to_import dirty.csv

# Compile proto file
compile-proto:
	$(CD_CMD) python3 manage.py compile_proto

#Run production server
prod:
	$(CD_CMD) /bin/sh scripts/prod_urls.sh

# Used to pre-compile tailwind CSS before running the application (we should maybe use this in run later)
tailwind:
	$(CD_CMD) python3 manage.py tailwind start

# Template linting commands
#Lint Django template files
lint-templates:
	djlint greenova/**/templates --lint

#Format Django template files
format-templates:
	djlint greenova/**/templates --reformat

#Check template formatting without changes
check-templates:
	djlint greenova/**/templates --check

# Combined command for formatting and linting
format-lint: format-templates lint-templates


# Remove virtual environment and temporary files
clean:
	@echo "Removing virtual environment and temporary files..."
	@rm -rf $(VENV)
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@echo "Clean completed."

#install the package with setup.py
setup:
	@echo "Running setup.py..."
	$(PYTHON) $(SETUP_SCRIPT) install

#run python start up script
pythonstartup:
	@echo "Setting up Python startup..."
	$(PYTHON) -M pythonstartup

#install setuptools
setuptools:
	@echo "Installing setuptools..."
	$(PYTHON) -m pip install setuptools

# Help command to list available commands
help:
	@echo "Available commands:"
	@echo "  make app name=appname - Create a new Django app with the specified name"
	@echo "  make check        - Run Django system check framework"
	@echo "  make check-templates  - Check template formatting without changes"
	@echo "  make format-templates - Format Django template files"
	@echo "  make prod         - Run production server"
	@echo "  make lint-templates   - Lint Django template files"
	@echo "  make update       - Update data from CSV file"
	@echo "  make update-recurring-dates - Update recurring inspection dates"
	@echo "  make normalize-frequencies - Normalize existing frequencies"
	@echo "  make clean-csv     - Clean CSV file"
	@echo "  make tailwind     - Start Tailwind CSS server"
	@echo "  make venv           - Create virtual environment"
	@echo "  make install        - Install dependencies"
	@echo "  make clean          - Remove virtual environment and clean temporary files"
	@echo "  make freeze		 - Freeze dependencies"
	@echo "  make dotenv-pull	 - Pull .env file from dotenv-vault"
	@echo "  make dotenv-push	 - Push .env file to dotenv-vault"
	@echo "  make setup			 - Install the package with setup.py"
	@echo "  make pythonstartup	 - Run python start up script"
	@echo "  make setuptools	 - Install setuptools"
