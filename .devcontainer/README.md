## 📦 Requirements

- Docker must be installed and running
- VS Code with the following extensions:
  - `Dev Containers`
  - Recommended: `Docker`

---

## 🚀 Quick Start

> ⚠️ **Important Notice Before You Begin**

Before using this project, please follow the steps below to ensure a smooth setup and prevent any loss of your local code:

1. Backup your existing code

If you have any local changes, **make sure to push your current project to a remote repository (e.g., GitHub)** before cloning this one. This prevents any accidental data loss during the setup process.

2. Update the clone URL in `post_start.sh`

Before launching the DevContainer, you must **edit line 14 of the `.devcontainer/post_start.sh` file**:

```bash
git clone https://github.com/your-org/greenova.git

3. **Open the project in VS Code**

   Open VS Code, then open the project directory.

4. **Start the DevContainer**

   > 🔄 **Important:**  
   If any changes are made to the `.devcontainer` folder (such as updates to `devcontainer.json` or `Dockerfile`), you must run  
   **"Rebuild and Reopen in Container"** to apply them.

   - Click the bottom-left blue icon in VS Code → Select `Reopen in Container`  
   - Or press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) and search for `Reopen in Container`

5. **Start coding**

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
- Automatically fix django hyperscript
- Automatically npx
- Automatically run make commands

---

## 🐍 Python Virtual Environment

- The virtual environment is automatically created at `./.venv`
- If `.venv` is accidentally created as `root`, it will be cleaned during container setup
- All dependencies from `requirements.txt` will be installed, including dev tools like `pylint`, `djlint`, and `autopep8`
