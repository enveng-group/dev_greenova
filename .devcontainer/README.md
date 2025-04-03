## 📦 Requirements

- Docker must be installed and running
- VS Code with the following extensions:
  - `Dev Containers`
  - Recommended: `Docker`

---

## 🚀 Quick Start

1. **Clone the project**

   ```bash
   git clone https://github.com/your-org/greenova.git
   cd greenova
   ```

2. **Open the project in VS Code**

   Open VS Code, then open the project directory.

3. **Start the DevContainer**

   > 🔄 **Important:**  
   If any changes are made to the `.devcontainer` folder (such as updates to `devcontainer.json` or `Dockerfile`), you must run  
   **"Rebuild and Reopen in Container"** to apply them.

   - Click the bottom-left blue icon in VS Code → Select `Reopen in Container`  
   - Or press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) and search for `Reopen in Container`

4. **Start coding**

   All dependencies and development tools will be installed automatically within the container.

---

## 🧰 DevContainer Configuration

- Uses a custom `Dockerfile` to build the environment
- Runs as the `vscode` user (non-root) to avoid permission issues
- Automatically installs:
  - Python dependencies (`requirements.txt`)
  - Node.js dependencies (`npm install`)
  - Development tools: Prettier, Pylint, djLint, etc.
- Python virtual environment is managed via `.venv` (auto-created and activated)

---

## 🐍 Python Virtual Environment

- The virtual environment is automatically created at `./.venv`
- If `.venv` is accidentally created as `root`, it will be cleaned during container setup
- All dependencies from `requirements.txt` will be installed, including dev tools like `pylint`, `djlint`, and `autopep8`
