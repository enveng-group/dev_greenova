# Gunicorn WSGI Server

## What is Gunicorn?

Gunicorn (Green Unicorn) is a Python WSGI HTTP Server for UNIX systems. It's a
pre-fork worker model, ported from Ruby's Unicorn project. The Gunicorn server
is broadly compatible with various web frameworks, simply implemented, light on
server resources, and fairly speedy.

## Why Use Gunicorn in Greenova?

Greenova uses Gunicorn as its production application server for several
reasons:

1. **Production-Ready**: Unlike Django's built-in development server, Gunicorn
   is designed for production use
2. **Resource Efficiency**: Optimized for the t2.nano AWS instances that
   Greenova uses (1 CPU, 500MB RAM)
3. **Process Management**: Provides worker process management, automatic
   restarts, and graceful reloads
4. **Scalability**: Can handle multiple concurrent connections through its
   worker model
5. **Integration**: Seamlessly works with Django's WSGI application

## Installation

```bash
pip install gunicorn
```

Add to your requirements.txt:

```txt
gunicorn==20.1.0  # Use the version that matches your project needs
```

## Running Gunicorn with Greenova

### Basic Command

```bash
cd /workspaces/greenova
gunicorn greenova.wsgi:application
```

### Using Configuration File

```bash
gunicorn -c gunicorn.conf.py greenova.wsgi:application
```

## Greenova's Gunicorn Configuration

Greenova's `gunicorn.conf.py` is optimized for low-resource environments:

```python
# Key settings from our configuration
bind = "0.0.0.0:8000"  # Where to listen
workers = 2            # Optimized for t2.nano (1 CPU)
worker_class = "sync"  # Best for low memory situations
max_requests = 300     # Restart workers after handling 300 requests
preload_app = False    # Save memory by not preloading application
loglevel = "warning"   # Minimal logging to reduce I/O
```

## Environment Variables

Gunicorn in Greenova can be configured through environment variables:

| Variable                | Description                | Default        |
| ----------------------- | -------------------------- | -------------- |
| `GUNICORN_BIND`         | Server binding address     | `0.0.0.0:8000` |
| `GUNICORN_WORKERS`      | Number of worker processes | `2`            |
| `GUNICORN_WORKER_CLASS` | Type of worker processes   | `sync`         |
| `GUNICORN_TIMEOUT`      | Request timeout            | `30`           |
| `GUNICORN_LOGLEVEL`     | Log level                  | `warning`      |

## Production Deployment

### Recommended Architecture

For production deployment, Greenova uses:

```txt
Client → Nginx (as reverse proxy) → Gunicorn → Django Application
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /workspaces/greenova/staticfiles/;
    }

    location /media/ {
        alias /workspaces/greenova/greenova/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Memory Optimization

Greenova's Gunicorn configuration is specifically optimized for low-memory
environments:

1. **Worker Count**: Limited to 2 workers to avoid memory exhaustion
2. **Sync Workers**: Using synchronous workers which have lower memory
   footprint
3. **Preload Disabled**: Application code isn't preloaded in the master process
4. **Minimal Logging**: Access logs disabled to reduce I/O operations
5. **Request Limits**: Workers restart after 300 requests to prevent memory
   leaks

## Systemd Service Example

For production deployment, create a systemd service:

```ini
[Unit]
Description=Greenova Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/workspaces/greenova
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn.conf.py greenova.wsgi:application
Restart=on-failure
Environment="DJANGO_SETTINGS_MODULE=greenova.settings"
Environment="DJANGO_SECRET_KEY=your-secret-key"
Environment="DJANGO_DEBUG=False"
Environment="DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com"

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **Worker Timeouts**: If you see worker timeout errors, adjust the `timeout`
   parameter

   ```python
   timeout = 60  # Increase from default 30 seconds
   ```

2. **Connection Refused**: Make sure the `bind` address is correct and the port
   is available

   ```python
   bind = "0.0.0.0:8000"  # Bind to all interfaces
   ```

3. **Memory Issues**: If you encounter memory errors, reduce the number of
   workers

   ```python
   workers = 1  # Minimum setting for very limited memory
   ```

4. **Slow Response**: For improved performance (on better hardware), consider
   async workers

   ```python
   worker_class = "uvicorn.workers.UvicornWorker"  # Requires uvicorn to be installed
   ```

## Additional Resources

- [Django Documentation on Gunicorn](https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/gunicorn/)
- [Gunicorn Official Documentation](https://docs.gunicorn.org/en/stable/)
- [Gunicorn Deployment Guide](https://docs.gunicorn.org/en/latest/deploy.html)
- [Gunicorn Settings Reference](https://docs.gunicorn.org/en/latest/settings.html)
