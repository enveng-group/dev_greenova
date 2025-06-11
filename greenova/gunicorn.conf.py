import os

# Server socket
# Use "unix:/run/gunicorn.sock" if you later add a reverse proxy like Nginx.
# For direct exposure, "0.0.0.0:PORT" is appropriate.
# Ensure the port (e.g., 8000) is open in your firewall if needed.
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8080")

# Worker processes
# Adhering to 88-char line limit
default_workers = 1
workers = int(os.environ.get("GUNICORN_WORKERS", default_workers))
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "sync")

# Worker timeout
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))

# Keep alive
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", 5))

# Logging
# If systemd handles log file redirection, Gunicorn should log to stdout/stderr.
# The special value '-' directs logs to stdout/stderr.
accesslog = os.environ.get("GUNICORN_ACCESSLOG", "-")
errorlog = os.environ.get("GUNICORN_ERRORLOG", "-")
loglevel = os.environ.get("GUNICORN_LOGLEVEL", "info")

# Process naming
proc_name = "greenova"

# Application directory
# This is redundant if WorkingDirectory is set in your systemd service file.
# You can comment it out if systemd handles it.
# chdir = "/home/ubuntu/greenova"

# Preload app for better performance, but can increase memory usage.
# Consider enabling if your app initialization is heavy and memory allows.
# preload_app = True

# Environment variables for Django worker processes.
# These ensure Django can find its settings and project modules.
# These can also be set in the systemd service file's Environment directive.
# If set there, these might be redundant but provide a fallback.
project_base_dir = os.path.dirname(os.path.abspath(__file__))
# Assuming gunicorn.conf.py is in the project root /home/ubuntu/greenova
# If not, adjust project_pythonpath accordingly.
default_pythonpath = os.environ.get("PYTHONPATH", project_base_dir)
default_django_settings = os.environ.get("DJANGO_SETTINGS_MODULE", "greenova.settings")

raw_env = [
    f"DJANGO_SETTINGS_MODULE={default_django_settings}",
    f"PYTHONPATH={default_pythonpath}",
]

# The os.environ.setdefault in your asgi.py/wsgi.py will also help ensure
# DJANGO_SETTINGS_MODULE is set when the application is loaded.


def post_fork(server, worker) -> None:
    """Called after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker) -> None:
    """Called before a worker is forked."""


def pre_exec(server) -> None:
    """Called before the master process is initialized."""
    server.log.info("Forked child, re-executing.")


def when_ready(server) -> None:
    """Called when the master process is initialized."""
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker) -> None:
    """Called when a worker received the SIGINT or SIGQUIT signal."""
    worker.log.info("Worker received INT or QUIT signal")


def worker_abort(worker) -> None:
    """Called when a worker received the SIGABRT signal,
    indicating a timeout or other error.
    """
    worker.log.warning("Worker received ABRT signal (timeout or error)")
