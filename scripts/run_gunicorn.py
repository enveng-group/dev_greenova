#!/usr/bin/env python3
"""Run Gunicorn with environment variable checks for Greenova.

Checks for GUNICORN_CONFIG_PATH and GUNICORN_WSGI_MODULE, prints a clear error
if missing, and runs Gunicorn with the correct arguments.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import os
import subprocess
import sys


def main() -> None:
    """Main function to validate environment variables and run Gunicorn.

    Checks for required environment variables GUNICORN_CONFIG_PATH and
    GUNICORN_WSGI_MODULE, then executes Gunicorn with proper configuration.

    Raises:
        SystemExit: When required environment variables are missing or
                   when Gunicorn fails to start.

    """
    config_path = os.environ.get("GUNICORN_CONFIG_PATH")
    wsgi_module = os.environ.get("GUNICORN_WSGI_MODULE")
    venv_python = os.environ.get(
        "PYTHON_INTERPRETER", "/workspaces/greenova/.venv/bin/python"
    )

    if not config_path:
        sys.exit(1)
    if not wsgi_module:
        sys.exit(1)

    cmd = [
        venv_python,
        "-m",
        "gunicorn",
        "--config",
        config_path,
        wsgi_module,
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)


if __name__ == "__main__":
    main()
