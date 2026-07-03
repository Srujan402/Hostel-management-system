# Advanced Installation and Deployment Guide

## Table of Contents
1. [Development Setup](#development-setup)
2. [Production Deployment](#production-deployment)
3. [Database Configuration](#database-configuration)
4. [Email Configuration](#email-configuration)
5. [Security Settings](#security-settings)
6. [Performance Optimization](#performance-optimization)
7. [Backup and Recovery](#backup-and-recovery)
8. [Troubleshooting](#troubleshooting)

## Development Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Git (optional)
- SQLite3

### Detailed Installation Steps

1. **Clone/Extract Repository**
   ```bash
   cd hostel_management_system
   ```

2. **Create and Activate Virtual Environment**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Linux/macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Environment Variables File**
   
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Generate Sample Data (Optional)**
   ```bash
   python manage.py generate_sample_data --students 50 --rooms 25
   ```

8. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   Access at: `http://localhost:8000`

## Production Deployment

### Using Gunicorn and Nginx

#### 1. Install Production Dependencies

```bash
pip install gunicorn whitenoise
pip freeze > requirements-prod.txt
```

#### 2. Update Settings for Production

Modify `hostel_config/settings.py`:

```python
# Production Settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = 'your-secure-secret-key-here'

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = '/path/to/static/'
```

#### 3. Configure Gunicorn

Create `gunicorn_config.py`:

```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
max_requests = 1000
timeout = 30
```

Run with:
```bash
gunicorn -c gunicorn_config.py hostel_config.wsgi:application
```

#### 4. Configure Nginx

Create `/etc/nginx/sites-available/hostel`:

```nginx
upstream hostel {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /path/to/static/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://hostel;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/hostel /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Database Configuration

### Using PostgreSQL for Production

1. **Install PostgreSQL**
   ```bash
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Create Database and User**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE hostel_db;
   CREATE USER hostel_user WITH PASSWORD 'secure_password';
   ALTER ROLE hostel_user SET client_encoding TO 'utf8';
   ALTER ROLE hostel_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE hostel_user SET default_transaction_deferrable TO on;
   ALTER ROLE hostel_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE hostel_db TO hostel_user;
   \q
   ```

3. **Update Django Settings**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'hostel_db',
           'USER': 'hostel_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Install psycopg2**
   ```bash
   pip install psycopg2-binary
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

## Email Configuration

### Gmail SMTP Setup

1. **Enable 2-Factor Authentication on Gmail**

2. **Generate App Password**
   - Go to myaccount.google.com
   - Select Security
   - Generate App Password

3. **Update Settings**
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
   ```

4. **Test Email**
   ```bash
   python manage.py shell
   from django.core.mail import send_mail
   send_mail('Test', 'This is a test email', 'from@example.com', ['to@example.com'])
   ```

## Security Settings

### Essential Security Checklist

1. **Update SECRET_KEY**
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Enable HTTPS**
   - Obtain SSL certificate (Let's Encrypt)
   - Update settings:
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   ```

3. **Setup CORS Headers**
   ```bash
   pip install django-cors-headers
   ```

4. **Configure CSRF Settings**
   ```python
   CSRF_COOKIE_HTTPONLY = True
   CSRF_COOKIE_SECURE = True
   ```

5. **Implement Rate Limiting**
   ```bash
   pip install django-ratelimit
   ```

## Performance Optimization

### Database Optimization

1. **Add Indexes**
   ```python
   class Meta:
       indexes = [
           models.Index(fields=['roll_number']),
           models.Index(fields=['status']),
       ]
   ```

2. **Use select_related() and prefetch_related()**
   ```python
   students = Student.objects.select_related('user', 'room').all()
   fees = Fee.objects.prefetch_related('student__complaints').all()
   ```

3. **Enable Database Connection Pooling**
   ```bash
   pip install django-db-connection-pool
   ```

### Caching

1. **Setup Redis Cache**
   ```bash
   sudo apt-get install redis-server
   pip install django-redis
   ```

2. **Configure in settings.py**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

### Frontend Optimization

1. **Compress Static Files**
   ```bash
   pip install django-compressor
   ```

2. **Enable GZIP Compression** (Nginx)
   ```nginx
   gzip on;
   gzip_types text/plain text/css text/xml text/javascript 
              application/x-javascript application/xml+rss;
   gzip_min_length 1000;
   ```

## Backup and Recovery

### Automated Backup Script

Create `backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backups/hostel"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup Database
pg_dump hostel_db > $BACKUP_DIR/db_backup_$DATE.sql

# Backup Media Files
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /path/to/media/

# Backup Settings
cp hostel_config/settings.py $BACKUP_DIR/settings_$DATE.py

# Keep only last 30 days of backups
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Restore from Backup

```bash
# Restore Database
psql hostel_db < db_backup_DATE.sql

# Restore Media
tar -xzf media_backup_DATE.tar.gz
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Migration Errors
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

#### 2. Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

#### 3. Permission Denied on Database
```bash
sudo chown -R www-data:www-data /path/to/db.sqlite3
```

#### 4. Memory Issues
```bash
# Increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 5. Port Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill the process
sudo kill -9 <PID>
```

### Debugging

Enable detailed logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/hostel/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## System Monitoring

### Install Monitoring Tools

```bash
pip install django-health-check
pip install sentry-sdk
```

### Health Check URL

Access at: `http://your-domain.com/health/`

## Scaling Considerations

### For High Traffic

1. **Implement Caching Layer**
   - Redis for session and query caching

2. **Database Replication**
   - Master-slave PostgreSQL setup

3. **Load Balancing**
   - Use HAProxy or Nginx load balancing

4. **CDN Integration**
   - CloudFlare for static assets

5. **Async Task Queue**
   ```bash
   pip install celery redis
   ```

---

**For Support**: Contact system administrator
**Last Updated**: May 2024
