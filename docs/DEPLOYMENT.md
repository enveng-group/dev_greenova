# Deployment Guide

## Architecture Overview

This guide outlines deploying a Django application with the following secure architecture:

```
User → HTTPS → Cloudflare Edge → HTTPS → Nginx Server → Gunicorn → Django
```

**Benefits of this approach:**
- End-to-end encryption (HTTPS everywhere)
- DDoS protection via Cloudflare
- Performance optimization through Cloudflare's edge network
- Proper separation of concerns (Nginx handles static files, Gunicorn handles Python)

## Prerequisites

- Python 3.9.21
- SQLite3 (or your preferred database)
- Nginx web server
- Virtual environment tool
- Domain name registered and accessible
- Server with root access (Ubuntu/Debian recommended)
- Cloudflare account

## Installation Steps

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install required packages:
   ```bash
   pip install django==4.2.20 gunicorn==23.0.0 psycopg2-binary==2.9.9
   ```

3. Clone your Django project:
   ```bash
   git clone https://github.com/yourusername/greenova.git
   cd greenova
   ```

4. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure Django settings for production:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS` with your domain
   - Configure `STATIC_ROOT` and `MEDIA_ROOT`
   - Set secure cookies and CSRF settings

## Django Production Settings

Edit your `settings.py` file to include these production-ready configurations:

```python
# Security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS/SSL settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files
STATIC_ROOT = '/path/to/your/static/files'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/path/to/your/media/files'
MEDIA_URL = '/media/'
```

## Django Deployment Checklist

Run the Django deployment checklist to identify any issues:

```bash
python manage.py check --deploy
```

Address any warnings or errors reported by this command.

## Setting Up Gunicorn

1. Test Gunicorn locally:
   ```bash
   gunicorn --bind 0.0.0.0:8000 yourproject.wsgi
   ```

2. Create a systemd service file for Gunicorn:
   ```bash
   sudo nano /etc/systemd/system/gunicorn.service
   ```

3. Add the following configuration:
   ```ini
   [Unit]
   Description=gunicorn daemon for greenova
   Requires=gunicorn.socket
   After=network.target

   [Service]
   Type=notify
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/greenova
   ExecStart=/path/to/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/run/gunicorn.sock \
             --access-logfile /var/log/gunicorn/access.log \
             --error-logfile /var/log/gunicorn/error.log \
             yourproject.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

4. Create a socket file:
   ```bash
   sudo nano /etc/systemd/system/gunicorn.socket
   ```

5. Add the following configuration:
   ```ini
   [Unit]
   Description=gunicorn socket

   [Socket]
   ListenStream=/run/gunicorn.sock
   SocketUser=www-data
   SocketGroup=www-data
   SocketMode=0660

   [Install]
   WantedBy=sockets.target
   ```

6. Create log directories:
   ```bash
   sudo mkdir -p /var/log/gunicorn
   sudo chown www-data:www-data /var/log/gunicorn
   ```

7. Enable and start the Gunicorn socket:
   ```bash
   sudo systemctl enable gunicorn.socket
   sudo systemctl start gunicorn.socket
   ```

## Setting Up Nginx

1. Install Nginx:
   ```bash
   sudo apt-get update
   sudo apt-get install nginx
   ```

2. Create a new Nginx site configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/greenova
   ```

3. Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       # Static files
       location /static/ {
           root /path/to/greenova;
           expires 30d;
           add_header Cache-Control "public, max-age=2592000";
       }
       
       # Media files
       location /media/ {
           root /path/to/greenova;
       }
       
       location / {
           proxy_set_header Host $http_host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_pass http://unix:/run/gunicorn.sock;
       }
   }
   ```

4. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/greenova /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

## Setting Up SSL with Let's Encrypt

1. Install Certbot:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. Obtain an SSL certificate:
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. Follow the prompts to complete the certificate setup.

4. Certbot will automatically update your Nginx configuration to use HTTPS.

## Cloudflare Configuration

1. Add your domain to Cloudflare:
   - Create a Cloudflare account if you don't have one
   - Add your domain and follow the instructions to update nameservers

2. Configure SSL/TLS settings:
   - Go to SSL/TLS tab in Cloudflare dashboard
   - Set SSL mode to "Full (strict)" since you have a valid certificate on your origin server

3. Configure SSL/TLS settings:
   - Enable "Always Use HTTPS" under SSL/TLS > Edge Certificates
   - Enable HSTS under SSL/TLS > Edge Certificates > HSTS
   
4. Set up Page Rules (optional):
   - Create rules for caching static content
   - Force HTTPS for all URLs

5. Configure Firewall settings:
   - Set up WAF rules to protect your application
   - Enable bot protection

## Collect Static Files

Collect your Django static files:

```bash
python manage.py collectstatic
```

## Finalizing Deployment

1. Set proper file permissions:
   ```bash
   sudo chown -R www-data:www-data /path/to/greenova
   sudo chmod -R 755 /path/to/greenova
   ```

2. Restart all services:
   ```bash
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

3. Test your deployment by visiting your domain.

## Monitoring and Maintenance

### Log Rotation

Create a logrotate configuration for Gunicorn logs:

```bash
sudo nano /etc/logrotate.d/gunicorn
```

Add the following configuration:

```
/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload gunicorn.service > /dev/null 2>/dev/null || true
    endscript
}
```

### Backup Strategy

1. Database backups:
   ```bash
   sqlite3 /path/to/db.sqlite3 .dump > backup_$(date +%Y%m%d).sql
   ```

2. Media files backup:
   ```bash
   tar -czf media_backup_$(date +%Y%m%d).tar.gz /path/to/media/
   ```

3. Transfer backups to a secure location.

### Updating Your Application

1. Pull the latest code:
   ```bash
   cd /path/to/greenova
   git pull origin main
   ```

2. Activate the virtual environment:
   ```bash
   source /path/to/venv/bin/activate
   ```

3. Install any new dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

6. Restart services:
   ```bash
   sudo systemctl restart gunicorn
   ```

## Troubleshooting

### Check Gunicorn Status
```bash
sudo systemctl status gunicorn
```

### Check Nginx Status
```bash
sudo systemctl status nginx
```

### Check Logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/gunicorn/error.log
```

### Common Issues

1. **502 Bad Gateway**
   - Check if Gunicorn is running
   - Verify socket permissions
   - Check firewall settings

2. **Static files not loading**
   - Verify STATIC_ROOT path
   - Check Nginx configuration
   - Run collectstatic again

3. **Permission issues**
   - Check file ownership and permissions
   - Ensure www-data can access all necessary files

## Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/en/latest/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Cloudflare Documentation](https://developers.cloudflare.com/fundamentals/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
