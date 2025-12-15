# Django Store Management System - Installation Guide

## Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

## Installation Steps

### 1. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install django pillow
```

### 3. Create Django project (if starting fresh)
```bash
django-admin startproject mystore
cd mystore
python manage.py startapp store
```

### 4. Add to settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',  # Add this
]

# Media files (for product images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Language
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
```

### 5. Update main urls.py
```python
# mystore/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 6. Create templates directory
```bash
# Create templates folder structure
mkdir -p store/templates/store
```

### 7. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create superuser
```bash
python manage.py createsuperuser
```

### 9. Run development server
```bash
python manage.py runserver
```

### 10. Access the application
- Main interface: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

## Template Files Structure

Place the HTML templates in the following structure:
```
store/
├── templates/
│   └── store/
│       ├── base.html
│       ├── dashboard.html
│       ├── product_list.html
│       ├── product_form.html
│       ├── product_confirm_delete.html
│       ├── category_list.html
│       ├── category_form.html
│       ├── customer_list.html
│       ├── customer_form.html
│       ├── sale_list.html
│       ├── sale_form.html
│       ├── sale_detail.html
│       ├── stock_movements.html
│       └── stock_adjustment.html
```

## Features Included

✅ **Dashboard** with sales statistics  
✅ **Product Management** with image upload  
✅ **Category Management**  
✅ **Customer Management**  
✅ **Sales System** with multiple payment methods  
✅ **Stock Control** with automatic updates  
✅ **Low Stock Alerts**  
✅ **Stock Movement History**  
✅ **Reports and Statistics**  
✅ **Responsive Design** with Bootstrap 5  

## Default Login
After creating superuser, login at `/admin/` first, then access the main interface at `/`

## Production Deployment

For production (Railway, Heroku, etc.):

1. Install additional packages:
```bash
pip install gunicorn whitenoise python-decouple dj-database-url psycopg2-binary
```

2. Create `requirements.txt`:
```bash
pip freeze > requirements.txt
```

3. Create `Procfile`:
```
web: gunicorn mystore.wsgi --log-file -
```

4. Update settings for production (use environment variables)

## Support
For issues or questions, check Django documentation at https://docs.djangoproject.com/