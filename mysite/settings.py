"""
Django settings for mysite project.
"""

from pathlib import Path
import os
import dj_database_url
#import django_heroku

# ---------------------- Base Directory ----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------- Security Settings ----------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "default-insecure-key")  # ✅ Secure fallback
DEBUG = os.environ.get("DEBUG", "True") == "True"  # ✅ Default to False in production

# ✅ Set allowed hosts securely for production
ALLOWED_HOSTS = ['*']

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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Static files for Heroku
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
        'DIRS': [BASE_DIR / 'GT_Movies_Store/Templates'],  # ✅ Fix Template Directory
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
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
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
TIME_ZONE = 'EST'
USE_I18N = True
USE_TZ = True

# ---------------------- Static Files (CSS, JavaScript, Images) ----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # ✅ Required for Heroku
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # ✅ Use WhiteNoise

# ---------------------- Default Auto Field ----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------- Authentication ----------------------
LOGIN_URL = '/login/'

# ---------------------- Heroku Settings (Must Be at the End) ----------------------
#django_heroku.settings(locals(), databases=False)  # ✅ Prevents override of DATABASES setting
