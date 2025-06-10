"""Gunicorn configuration for Greenova Django development server.

This configuration is optimized for development use with features like
auto-reloading and debugging support.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import multiprocessing
import os
from pathlib import Path

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Development settings
reload = True
reload_extra_files = []

# Add common file types to reload watch
project_root = Path(__file__).parent
for pattern in ["*.py", "*.html", "*.css", "*.js", "*.json"]:
    reload_extra_files.extend(project_root.rglob(pattern))

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "greenova_gunicorn"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn_greenova.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (for HTTPS development if needed)
keyfile = None
certfile = None

# Application
wsgi_module = "greenova.wsgi:application"
pythonpath = str(project_root)

# Development-specific settings
if os.environ.get("DJANGO_DEBUG", "False") == "True":
    # Single worker for debugging
    workers = 1
    # Increase timeout for debugging
    timeout = 300
    # Enable detailed error pages
    capture_output = True
