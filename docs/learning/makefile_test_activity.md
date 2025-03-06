### Test Activity: Automating a Python Project with a Makefile

#### Objective:
Create a Makefile to automate common tasks in a Python project, including setting up a virtual environment, installing dependencies, running tests, and cleaning up build artifacts.

#### Project Structure:
Here is a simple Python project structure to use:

```
my_python_project/
├── Makefile
├── requirements.txt
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
└── README.md
```

#### Tasks:

1. **Setup Virtual Environment:**
   - Create a target in the Makefile to set up a virtual environment using `venv`.
   - Ensure the virtual environment is activated before running any other commands.

2. **Install Dependencies:**
   - Create a target to install dependencies listed in `requirements.txt` using `pip`.

3. **Run Tests:**
   - Create a target to run tests using `pytest`.
   - Ensure the tests are run within the virtual environment.

4. **Clean Up:**
   - Create a target to clean up build artifacts (e.g., `__pycache__`, `.pytest_cache`, etc.).

5. **Help:**
   - Create a help target that lists all available Makefile targets and their descriptions.

#### Example Makefile:

```makefile
# Makefile for automating Python project tasks

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest

.PHONY: all venv install test clean help

all: help

venv:
	python3 -m venv $(VENV_DIR)

install: venv
	$(PIP) install -r requirements.txt

test: install
	$(PYTEST)

clean:
	rm -rf $(VENV_DIR) __pycache__ .pytest_cache

help:
	@echo "Available targets:"
	@echo "  venv    - Set up virtual environment"
	@echo "  install - Install dependencies"
	@echo "  test    - Run tests"
	@echo "  clean   - Clean up build artifacts"
	@echo "  help    - Show this help message"
```

#### Instructions:
1. Provide the intern with the project structure and the tasks.
2. Ask them to implement the Makefile based on the tasks outlined.
3. Review their Makefile to ensure it meets the requirements and runs correctly.

---

This activity should give you a good sense of their understanding and ability to automate tasks in a Python project using a Makefile.
