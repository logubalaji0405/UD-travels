"""
Django settings for fullproject project.
"""

from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY SETTINGS
# ===============================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "ud-travels.onrender.com",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://ud-travels.onrender.com",
]

# ==============================
# APPLICATIONS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',  # your app
]


# ===============================
# MIDDLEWARE
# ===============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ADD THIS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# URL & TEMPLATES
# ===============================
ROOT_URLCONF = 'fullproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 👉 FIXED TEMPLATE PATH
        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fullproject.wsgi.application'


# ===============================
# DATABASE
# ===============================
DATABASES = { 
    'default': {
         'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# PASSWORD VALIDATION
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ===============================
# INTERNATIONAL SETTINGS
# ===============================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # 🇮🇳 India time

USE_I18N = True
USE_TZ = True


# ===============================
# STATIC FILES (VERY IMPORTANT)
# ===============================
STATIC_URL = '/static/'

# Your custom static folder
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 👉 REQUIRED for collectstatic (FIX YOUR ERROR)
STATIC_ROOT = BASE_DIR / "staticfiles"


# ===============================
# MEDIA FILES (UPLOADS)
# ===============================
MEDIA_URL = '/media/'
MEDIA_ROOT = "/opt/render/project/src/media"


# ===============================
# AUTH REDIRECT
# ===============================
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# ===============================
# DEFAULT PK
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===============================
# OPTIONAL (API KEY)
# ===============================
OPENAI_API_KEY = "your_api_key_here"


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}