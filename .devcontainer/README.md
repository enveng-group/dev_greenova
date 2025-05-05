# Dev Container Setup for Greenova

## 📦 Requirements

- Docker must be installed and running
- VS Code with the following extensions:
  - `Dev Containers`
  - Recommended: `Docker`

---

## 🚀 Getting Started

1. **Clone the project**

   ```bash
   git clone https://github.com/your-org/greenova.git
   cd greenova
   ```

2. **Open the project in VS Code**

   Open VS Code, then open the project directory.

3. **Install Dependencies**:

   - Run `make install` to set up Python and Node.js dependencies.

4. **Set up Database**:

   - Run `make migrate` to apply Django database migrations.
   - Optionally, run `make import-data` to load initial dummy data.

5. **Run the Development Server**:
   - Execute `make run` to start the Django development server.
   - Access the application at [http://localhost:8000](http://localhost:8000).

---

## 🧰 DevContainer Configuration

- Uses a custom `Dockerfile` to build the environment
- Runs as the `vscode` user (non-root) to avoid permission issues
- Automatically installs:
  - Python dependencies (`requirements.txt`)
  - Node.js dependencies (`npm install`)
  - Development tools: Prettier, Pylint, djLint, etc.
- Python virtual environment is managed via `.venv` (auto-created and
  activated)

---

## 🐍 Python Virtual Environment

- The virtual environment is automatically created at `./.venv`
- If `.venv` is accidentally created as `root`, it will be cleaned during
  container setup
- All dependencies from `requirements.txt` will be installed, including dev
  tools like `pylint`, `djlint`, and `autopep8`

---

# Greenova Development Container

This directory contains the configuration for the VS Code Development Container
used in the Greenova project. The container provides a consistent development
environment across different platforms.

## Features

- Python 3.12.9 with virtual environment
- Node.js 20.19.1 and npm 11.3.0
- Fish shell as the default shell
- SQLite database
- Automatic dependency installation
- Persistent volumes for data and dependencies

## Key Files

- `devcontainer.json`: Main configuration file for VS Code Dev Container
- `Dockerfile`: Defines the container image with all required dependencies
- `docker-compose.yml`: Sets up container services and volume mappings
- `post_start.sh`: Script that runs after container creation to set up the
  environment
- `entrypoint.sh`: Container entry point script that initializes the
  environment

## Volume Configuration

The setup uses several Docker volumes to persist data between container
rebuilds:

- `greenova-venv-volume`: Stores the Python virtual environment
- `greenova-home-volume`: Persists the home directory for the `vscode` user
- `dotfiles-volume`: Stores your personal dotfiles configuration
- SSH keys are mounted read-only from your host machine

## Development Workflow

When working with this dev container:

1. **First-time setup**: VS Code will build the container automatically when
   you open the workspace
2. **Rebuilding**: Use the VS Code command "Rebuild Container" if you need to
   update the configuration
3. **Fish shell helpers**: Use the `greenova` command to access helper
   functions:
   - `greenova setup`: Set up the development environment
   - `greenova run`: Start the Django development server
   - `greenova makemigrations`: Create new migrations
   - `greenova migrate`: Apply migrations
   - `greenova shell`: Open the Django shell
   - `greenova test`: Run the test suite
   - `greenova help`: Show all available commands

## Troubleshooting

If you encounter issues:

1. **Missing files**: Your workspace should be properly persisted in volumes.
   If files are missing, check the Docker volumes.
2. **Permission issues**: The `post_start.sh` script fixes permissions, but if
   you encounter issues, run:

   ```bash
   sudo chown -R vscode:vscode /workspaces/greenova
   ```

3. **SSH/Dotfiles**: If SSH keys or dotfiles aren't working, check the volume
   mounts in `docker-compose.yml`.

## Customizing

To customize this setup:

1. Modify `.devcontainer/Dockerfile` to add dependencies
2. Update `.devcontainer/docker-compose.yml` to change volume mappings
3. Edit `.devcontainer/devcontainer.json` to change VS Code settings and
   extensions
4. Modify `.devcontainer/post_start.sh` for custom initialization steps
