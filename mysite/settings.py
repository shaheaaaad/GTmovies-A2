"""
Django settings for mysite project.
"""

from pathlib import Path
import os
import dj_database_url
import django_heroku

# ---------------------- Base Directory ----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------- Security Settings ----------------------
SECRET_KEY = os.getenv("SECRET_KEY", "default-insecure-key")  # Use environment variable in production
DEBUG = os.getenv("DEBUG", "False") == "True"  # Default to False in production

ALLOWED_HOSTS = ["*"]  # Change this to specific domain in production

# ---------------------- Installed Apps ----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'GT_Movies_Store.apps.GtMoviesStoreConfig',
]

# ---------------------- Middleware ----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Ensures static files work on Heroku
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------- URL Configuration ----------------------
ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# ---------------------- Database (Heroku Postgres) ----------------------
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# ---------------------- Password Validation ----------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------- Localization ----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------- Static Files (CSS, JavaScript, Images) ----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Required for Heroku
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # Use WhiteNoise

# ---------------------- Default Auto Field ----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------- Authentication ----------------------
LOGIN_URL = '/login/'

# ---------------------- Heroku Settings (Must Be at the End) ----------------------
django_heroku.settings(locals(), databases=False)  # ✅ Prevents override of DATABASES setting
