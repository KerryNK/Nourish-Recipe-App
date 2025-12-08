# Deployment Guide - Nourish Recipe App

This guide covers deploying the Nourish Recipe App to production.

## Quick Start Deployment

### 1. Clone Repository

```bash
git clone https://github.com/KerryNK/Nourish-Recipe-App.git
cd Nourish-Recipe-App
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your production settings
nano .env
```

**Critical settings to update in `.env`:**

- **SECRET_KEY** - Generate a new one:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  
- **DEBUG=False** - Never run with DEBUG=True in production

- **ALLOWED_HOSTS** - Set to your domain names:
  ```
  ALLOWED_HOSTS=example.com,www.example.com
  ```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Production Server Setup

### Option A: Gunicorn + Nginx (Recommended)

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 django_project.wsgi:application
```

### Option B: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 django_project.wsgi:application
```

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `SECRET_KEY` | Django secret key | Generate with command above |
| `DEBUG` | Debug mode (False for production) | `False` |
| `ALLOWED_HOSTS` | Allowed domain names | `example.com,www.example.com` |

## Security Checklist

- [ ] Generate new SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS/SSL certificate
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity

---

**Last Updated:** December 8, 2025
