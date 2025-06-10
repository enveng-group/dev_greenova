# Greenova Django Development Environment - Fish Shell Configuration
# Author: Adrian Gallo <agallo@enveng-group.com.au>
# License: AGPL-3.0

# Core environment variables
set -x EDITOR code
set -x BROWSER ""

# Project paths for Copilot context
set -x WORKSPACE_ROOT "/workspaces/greenova"
set -x DJANGO_PROJECT_ROOT "/workspaces/greenova/greenova"
set -x DJANGO_MANAGE_PY "/workspaces/greenova/greenova/manage.py"
set -x VENV_PATH "/workspaces/greenova/.venv"
set -x NODE_MODULES_PATH "/workspaces/greenova/node_modules"
set -x FRONTEND_DIST_DIR "/workspaces/greenova/greenova/static/dist"

# Django environment
set -x DJANGO_SETTINGS_MODULE "greenova.settings"
set -x DJANGO_DEBUG "True"
set -x DJANGO_LOG_LEVEL INFO
set -x PYTHONPATH "/workspaces/greenova/greenova"

# Gunicorn configuration
set -x GUNICORN_CONFIG_PATH "/workspaces/greenova/greenova/gunicorn.conf.py"
set -x GUNICORN_WSGI_MODULE "greenova.wsgi:application"

# Django Test Configuration
set -x DJANGO_TEST_RUNNER "django.test.runner.DiscoverRunner"
set -x DJANGO_TEST_DATABASE_NAME ":memory:"
set -x DJANGO_TEST_KEEPDB "True"
set -x DJANGO_TEST_PARALLEL "auto"

# Development tool paths
set -x AUTOPEP8_PATH "/usr/local/bin/autopep8"
set -x MYPY_PATH "/usr/local/bin/mypy"
set -x RUFF_PATH "/usr/local/bin/ruff"
set -x PYLINT_PATH "/usr/local/bin/pylint"
set -x PRECOMMIT_PATH "/usr/local/bin/pre-commit"
set -x BLACK_PATH "/usr/local/bin/black"
set -x VULTURE_PATH "/usr/local/bin/vulture"
set -x PROSELINT_PATH "/usr/local/bin/proselint"
set -x PROTOC_PATH "/usr/bin/protoc"
set -x BANDIT_PATH "/usr/local/bin/bandit"
set -x ISORT_PATH "/usr/local/bin/isort"

# Django server aliases
alias django-run "$VENV_PATH/bin/python $DJANGO_MANAGE_PY runserver 0.0.0.0:8000"
alias django-gunicorn "cd $DJANGO_PROJECT_ROOT && gunicorn --config $GUNICORN_CONFIG_PATH $GUNICORN_WSGI_MODULE"
alias django-manage "python $DJANGO_MANAGE_PY"
alias django-shell "cd $DJANGO_PROJECT_ROOT && python manage.py shell_plus"
alias django-test "cd $DJANGO_PROJECT_ROOT && python manage.py test --keepdb --verbosity=2"
alias django-test-fast "cd $DJANGO_PROJECT_ROOT && python manage.py test --keepdb --failfast --verbosity=1"
alias django-test-parallel "cd $DJANGO_PROJECT_ROOT && python manage.py test --keepdb --parallel auto --verbosity=2"
alias django-test-coverage "cd $DJANGO_PROJECT_ROOT && coverage run --source=. manage.py test --keepdb && coverage report"
alias django-migrate "cd $DJANGO_PROJECT_ROOT && python manage.py migrate"
alias django-makemigrations "cd $DJANGO_PROJECT_ROOT && python manage.py makemigrations"
alias django-check "cd $DJANGO_PROJECT_ROOT && python manage.py check"
alias django-collectstatic "cd $DJANGO_PROJECT_ROOT && python manage.py collectstatic --clear --noinput"

# Development tool aliases
alias ruff-check "$RUFF_PATH check"
alias ruff-format "$RUFF_PATH format"
alias mypy-check "$MYPY_PATH"
alias pylint-check "$PYLINT_PATH"
alias black-format "$BLACK_PATH"
alias isort-check "$ISORT_PATH"
alias bandit-check "$BANDIT_PATH"
alias autopep8-format "$AUTOPEP8_PATH"
alias pre-commit-run "$PRECOMMIT_PATH run"
alias pre-commit-install "$PRECOMMIT_PATH install"

# Prefer uv for pip if available
if type -q uv
    alias pip "uv pip"
    alias pip3 "uv pip"
    set -x UV_PYTHON_PREFERENCE system
end

# Auto-activate venv in project directory
function auto_activate_venv --on-variable PWD
    if test -z "$VIRTUAL_ENV"
        if string match -q "/workspaces/greenova*" $PWD
            if test -f $VENV_PATH/bin/activate.fish
                source $VENV_PATH/bin/activate.fish
                echo "🐍 Auto-activated virtual environment: .venv"
            end
        end
    end
end

# Set iPython as default python shell if available
if type -q ipython
    alias python ipython
    alias python3 ipython
end

# Unset SSH agent variables for Dropbear compatibility
set -e SSH_AUTH_SOCK
set -e SSH_AGENT_PID

# Enhanced history settings
set -x fish_history greenova
set -x HISTSIZE 50000
set -x HISTFILESIZE 100000

# Quick navigation function
function cdp
    cd (find . -type d -name "*$argv*" | head -1)
end

# Django-specific quick navigation
function cdg
    cd $DJANGO_PROJECT_ROOT
end

function cdw
    cd $WORKSPACE_ROOT
end

# Extract function
function extract
    set file $argv[1]
    if test -f $file
        switch $file
            case "*.tar.bz2"
                tar xjf $file
            case "*.tar.gz"
                tar xzf $file
            case "*.bz2"
                bunzip2 $file
            case "*.rar"
                unrar x $file
            case "*.gz"
                gunzip $file
            case "*.tar"
                tar xf $file
            case "*.tbz2"
                tar xjf $file
            case "*.tgz"
                tar xzf $file
            case "*.zip"
                unzip $file
            case "*.Z"
                uncompress $file
            case "*.7z"
                7z x $file
            case "*"
                echo "'$file' cannot be extracted via extract()"
        end
    else
        echo "'$file' is not a valid file"
    end
end

# Development workflow functions
function dev-setup
    echo "🔧 Setting up development environment..."
    cd $WORKSPACE_ROOT
    source $VENV_PATH/bin/activate.fish
    pre-commit-install
    echo "✅ Development environment ready!"
end

function dev-check
    echo "🔍 Running development checks..."
    cd $WORKSPACE_ROOT
    ruff-check .
    mypy-check greenova/
    django-check
    echo "✅ All checks completed!"
end

function dev-format
    echo "🎨 Formatting code..."
    cd $WORKSPACE_ROOT
    ruff-format .
    isort-check --diff greenova/
    echo "✅ Code formatting completed!"
end

function dev-test
    echo "🧪 Running Django tests..."
    django-test-parallel
    echo "✅ Tests completed!"
end

# Load local customizations if present
if test -f ~/.config/fish/config.local
    source ~/.config/fish/config.local
end

# Welcome message with comprehensive project info
function fish_greeting
    echo "🌿 Welcome to Greenova development environment!"
    echo "=== Project Status ==="
    echo "Working directory: "(pwd)
    echo "Git branch: "(git branch --show-current ^/dev/null; or echo 'Not a git repo')
    echo "Git status:"
    git status --porcelain ^/dev/null; or echo "Not a git repository"
    echo ""

    # Environment info
    echo "=== Environment ==="
    if type -q python3
        echo "Python version: 3.12.10"
    end
    if type -q ipython
        echo "iPython version: "(ipython --version)
    end
    echo "Virtual environment: "$VIRTUAL_ENV
    echo "PYTHONPATH: "$PYTHONPATH
    echo "Django settings: "$DJANGO_SETTINGS_MODULE
    echo "Django debug: "$DJANGO_DEBUG
    echo "Test runner: "$DJANGO_TEST_RUNNER
    echo ""

    # Project paths
    echo "=== Project Paths ==="
    echo "Workspace: $WORKSPACE_ROOT"
    echo "Django project: $DJANGO_PROJECT_ROOT"
    echo "Virtual env: $VENV_PATH"
    echo "Node modules: $NODE_MODULES_PATH"
    echo ""

    # Available commands
    echo "=== Quick Commands ==="
    echo "🚀 django-gunicorn      - Start Gunicorn server (production-like)"
    echo "🔧 django-run           - Start Django development server"
    echo "🐚 django-shell         - Open Django shell with shell_plus"
    echo "🧪 django-test          - Run Django tests (keepdb, verbose)"
    echo "⚡ django-test-fast      - Run Django tests (fast, failfast)"
    echo "� django-test-parallel - Run Django tests (parallel, keepdb)"
    echo "📊 django-test-coverage - Run tests with coverage report"
    echo "�📦 django-migrate       - Run database migrations"
    echo "🎨 dev-format           - Format all code"
    echo "🔍 dev-check            - Run all development checks"
    echo "🧪 dev-test             - Run parallel Django tests"
    echo "⚡ cdg                   - Navigate to Django project root"
    echo "🏠 cdw                   - Navigate to workspace root"
    echo ""
end
