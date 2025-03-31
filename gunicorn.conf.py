import os

# Server socket settings
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")
backlog = int(os.environ.get("GUNICORN_BACKLOG", "1024"))  # Reduced from 2048

# Worker processes - optimized for t2.nano (1 CPU, 500MB RAM)
workers = int(os.environ.get("GUNICORN_WORKERS", "2"))  # 2 workers is optimal for t2.nano
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "sync")  # "sync" is best for low memory
worker_connections = int(os.environ.get("GUNICORN_WORKER_CONNECTIONS", "100"))  # Further reduced to save memory
threads = int(os.environ.get("GUNICORN_THREADS", "1"))  # Reduced threads to 1 for memory conservation
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "30"))
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", "2"))

# Worker restart strategy - conservative for memory stability
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "300"))  # Further reduced for stability
max_requests_jitter = int(os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "50"))

# Graceful timeout configuration
graceful_timeout = int(os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "30"))

# Memory optimization
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
chdir = os.environ.get("GUNICORN_CHDIR", "/workspaces/greenova/greenova")
preload_app = os.environ.get("GUNICORN_PRELOAD_APP", "False").lower() in ("true", "1")  # Changed default to False to save memory

# Disable optional monitoring to save resources
statsd_host = os.environ.get("GUNICORN_STATSD_HOST", None)
statsd_prefix = os.environ.get("GUNICORN_STATSD_PREFIX", "greenova")

# Minimal logging to reduce I/O
errorlog = os.environ.get("GUNICORN_ERRORLOG", "-")
loglevel = os.environ.get("GUNICORN_LOGLEVEL", "warning")  # Keep at warning level
accesslog = os.environ.get("GUNICORN_ACCESSLOG", None)  # No access logging to save resources
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = os.environ.get("GUNICORN_PROC_NAME", "greenova.wsgi")

# Disable auto-reload in production to save resources
reload = os.environ.get("GUNICORN_RELOAD", "False").lower() in ("true", "1")

# Server hooks - keep them minimal
def on_starting(server):
    """Log when server starts"""
    server.log.info("Starting Greenova server with Gunicorn")

def when_ready(server):
    """Log when server is ready"""
    server.log.info("Gunicorn server is ready. Listening at: %s" % bind)

def worker_abort(worker):
    """Log when a worker is aborted"""
    worker.log.warning("Worker aborted (pid: %s)", worker.pid)

def worker_exit(server, worker):
    """Clean up on worker exit"""
    server.log.info("Worker exited (pid: %s)", worker.pid)
