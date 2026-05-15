# Stamatolog

> Stomatologiya klinikasi uchun **Django REST API** — shifokorlar, xizmatlar, qabul va galereya.

---

## 1. Loyiha nima qiladi?

| Blok | Tavsif |
|------|--------|
| **Shifokorlar** | Ro‘yxat, bitta shifokor, uning sharhlari |
| **Xizmatlar** | Klinika xizmatlari ro‘yxati va tafsilotlari |
| **Qabul** | Bo‘sh vaqtlar, mavjud shifokorlar, yozuv yaratish / ko‘rish |
| **Galereya** | Rasmlar va kategoriyalar |
| **Admin** | Django admin orqali ma’lumotlarni boshqarish |

Asosiy API prefiksi: **`/api/v1/`**

---

## 2. Texnologiyalar

- **Python 3** + **Django 4.2+**
- **Django REST Framework** — JSON API
- **django-cors-headers** — frontend bilan ishlash uchun CORS
- **SQLite** — standart (development); production uchun **PostgreSQL** ga o‘tish mumkin (`requirements.txt` da `psycopg2-binary`)
- **python-decouple** — `.env` orqali sozlamalar

Oldindan yig‘ilgan **statik frontend** `netlify/` papkasida (Netlify uchun).

---

## 3. API marshrutlar (qisqacha)

| Yo‘l | Mazmuni |
|------|---------|
| `GET/POST` | `/api/v1/doctors/` — shifokorlar |
| `GET` | `/api/v1/doctors/<id>/` |
| `GET/POST` | `/api/v1/doctors/<id>/reviews/` — sharhlar |
| `GET` | `/api/v1/services/` va `/api/v1/services/<id>/` |
| `GET` | `/api/v1/appointments/available-slots/` |
| `GET` | `/api/v1/appointments/available-doctors/` |
| `POST` | `/api/v1/appointments/` — yozuv |
| `GET` | `/api/v1/appointments/<id>/` |
| `GET` | `/api/v1/gallery/` va `/api/v1/gallery/categories/` |
| — | `/admin/` — Django admin |
| Media | Yuklangan fayllar `/media/` ostida |

---

## 4. Mahalliy kompyuterda ishga tushirish

### Talablar

- Python **3.10+** (tavsiya etiladi)
- `git`

### Qadam 1 — repozitoriy va muhit

```bash
cd Stamatolog
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Qadam 2 — muhit o‘zgaruvchilari

```bash
cp .env.example .env
```

`.env` ichida kamida:

```env
SECRET_KEY=haqiqiy-uzun-maxfiy-kalit
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Qadam 3 — ma’lumotlar bazasi va superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Qadam 4 — serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerda:

- API asosiy joyi: **http://127.0.0.1:8000/api/v1/**
- Admin: **http://127.0.0.1:8000/admin/**

---

## 5. Ishlatish (amaliy)

1. **Admin** orqali shifokorlar, xizmatlar, galereya va boshqalarni to‘ldiring.
2. **Frontend** alohida joylashtirilgan bo‘lsa, API bazav URL manzilini shu serverga yo‘naltiring (masalan `http://127.0.0.1:8000`).
3. **Media** fayllar `media/` papkasida saqlanadi; development rejimida Django ularni xizmat qiladi.

---

## 6. Netlify (statik sahifa)

`netlify/` — tayyor HTML/CSS/JS. Netlify’da **publish directory** sifatida `netlify` ni tanlang yoki o‘sha papkadagi kontentni yuklang.

`_redirects.txt` SPA uslubida barcha yo‘llarni `index.html` ga yo‘naltirish uchun ishlatiladi.

---

## 7. Production (server)

- **`DEPLOYMENT.md`** — batafsil: Ubuntu, Nginx, Gunicorn, systemd, SSL.
- Loyihada mavjud: `deploy.sh`, `stamatolog.service`, `nginx_config.conf`, `gunicorn_config.py`.

Tezkor eslatma:

```bash
./deploy.sh
```

(virtual muhit, `migrate`, `collectstatic`, servislarni qayta ishga tushirish — skript ichida.)

Production uchun: **`DEBUG=False`**, kuchli **`SECRET_KEY`**, to‘g‘ri **`ALLOWED_HOSTS`**.

---

## 8. Loyiha tuzilmasi (qisqa)

```
config/          # settings, urls, WSGI
doctors/         # shifokorlar + sharhlar URL
services/        # xizmatlar
appointments/    # qabul
gallery/         # galereya
reviews/         # sharh modellari / view
netlify/         # statik frontend
manage.py
```

---

## 9. Foydali buyruqlar

| Buyruq | Vazifa |
|--------|--------|
| `python manage.py runserver` | Development server |
| `python manage.py migrate` | Migratsiyalar |
| `python manage.py createsuperuser` | Admin foydalanuvchi |
| `python manage.py collectstatic` | Statik fayllarni yig‘ish (production) |

---

**Savol yoki xato bo‘lsa**, `DEPLOYMENT.md` va `.env.example` fayllarini ham tekshiring.
