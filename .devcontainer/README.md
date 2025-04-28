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
