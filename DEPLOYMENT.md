# Server Deployment Guide - Stamatolog

## Production uchun kerakli fayllar

Loyihada quyidagi serverga joylashtirish fayllari mavjud:

### 1. ASGI/WSGI Configuration
- `config/wsgi.py` - WSGI konfiguratsiya (Gunicorn, uWSGI uchun)
- `config/asgi.py` - ASGI konfiguratsiya (async server uchun)
- `config/app.py` - Application entry point

### 2. Server Configuration Files
- `gunicorn_config.py` - Gunicorn sozlamalari
- `nginx_config.conf` - Nginx sozlamalari
- `stamatolog.service` - Systemd service fayli
- `deploy.sh` - Deployment script

### 3. Environment
- `.env.production` - Production environment o'zgaruvchilari

## Server Setup (Ubuntu/Debian)

### 1. Server yangilash
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Kerakli paketlar
```bash
sudo apt install python3-pip python3-venv nginx supervisor git -y
```

### 3. Loyihani ko'chirish
```bash
cd /var/www
sudo git clone <your-repo-url> stamatolog
cd stamatolog
```

### 4. Virtual environment yaratish
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 5. Environment o'rnatish
```bash
cp .env.production .env
# .env faylini tahrirlang va haqiqiy qiymatlar kiriting
nano .env
```

### 6. Django sozlash
```bash
# Migration
python manage.py migrate

# Static fayllar
python manage.py collectstatic --noinput

# Superuser yaratish
python manage.py createsuperuser
```

### 7. Gunicorn test
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 8. Systemd service o'rnatish
```bash
sudo cp stamatolog.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start stamatolog
sudo systemctl enable stamatolog
sudo systemctl status stamatolog
```

### 9. Nginx konfiguratsiya
```bash
sudo cp nginx_config.conf /etc/nginx/sites-available/stamatolog
sudo ln -s /etc/nginx/sites-available/stamatolog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. SSL (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d stamatolog.uz -d www.stamatolog.uz
```

## Deployment

Yangilanishlarni serverga yuklash uchun:
```bash
cd /var/www/stamatolog
./deploy.sh
```

yoki qo'lda:
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart stamatolog
```

## Foydali buyruqlar

### Service boshqarish
```bash
sudo systemctl status stamatolog
sudo systemctl restart stamatolog
sudo systemctl stop stamatolog
sudo systemctl start stamatolog
```

### Loglarni ko'rish
```bash
sudo journalctl -u stamatolog -f
sudo tail -f /var/log/nginx/error.log
```

### Database backup
```bash
python manage.py dumpdata > backup.json
```

## PostgreSQL (optional)

Agar PostgreSQL ishlatmoqchi bo'lsangiz:

```bash
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql

CREATE DATABASE stamatolog;
CREATE USER stamatolog_user WITH PASSWORD 'your-password';
ALTER ROLE stamatolog_user SET client_encoding TO 'utf8';
ALTER ROLE stamatolog_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE stamatolog_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE stamatolog TO stamatolog_user;
\q
```

settings.py da:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='stamatolog'),
        'USER': config('DB_USER', default='stamatolog_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

## Security Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY o'zgartirildi
- [ ] ALLOWED_HOSTS to'g'ri sozlandi
- [ ] SSL sertifikat o'rnatildi
- [ ] Firewall sozlandi
- [ ] Static/Media fayllar xavfsizligi
- [ ] Database backup sozlandi
- [ ] Log monitoring o'rnatildi
