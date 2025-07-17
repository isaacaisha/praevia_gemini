# /home/siisi/praevia_gemini/praevia_core/settings.py

import os
import dotenv
import dj_database_url
from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load ENVIRONMENT from system or default to "dev"
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

# Load correct .env file
dotenv_file = BASE_DIR / f".env.{ENVIRONMENT}"
dotenv.load_dotenv(dotenv_path=dotenv_file)

# -----------------------------------------------------------------------------
# SECURITY
# -----------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Trusted domains
CSRF_TRUSTED_ORIGINS = [
    'https://praevia-gemini.siisi.online',
    'https://www.praevia-gemini.siisi.online',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# --- CORS Settings ---
CORS_ALLOWED_ORIGINS = [
    'https://praevia-gemini.siisi.online',
    'https://www.praevia-gemini.siisi.online',
]
CORS_ALLOW_CREDENTIALS = True # If your frontend sends cookies/auth headers

# Proxy support
PROXY = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

# Admins (for 500 error notifications)
#ADMINS = [('Medusa', 'medusadbt@gmail.com')]

# SSL & Security settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_AGE = 3600
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

# To handle large files
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'praevia_api',
    'rest_framework',
    'rest_framework.authtoken', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'praevia_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'praevia_core.wsgi.application'


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=os.getenv('DB_SSL_REQUIRE', 'False').lower() == 'true'
    )
}

## Database
## https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


# -----------------------------------------------------------------------------
# Django REST framework
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication', # Keep for browsable API
        #'praevia_api.authentication.JWTAuthentication',         # For Postman/Frontend
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # Protect all views by default
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES_FOR_BROWSABLE_API': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# --- IMPORTANT: Custom Authentication Backend for Django's Auth System ---
AUTHENTICATION_BACKENDS = [
    #'praevia_api.backends.CustomAuthBackend', # <--- NEW: Your custom backend
    'django.contrib.auth.backends.ModelBackend', # Default Django backend, keep it too
]

# --- Important URLs for Authentication Flow ---
LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'


# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'praevia_api.User'

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en')
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('pt', _('Portuguese')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static & Media
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'django.log'),
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'two_factor': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
    #'loggers': {
    #    'django': {
    #        'handlers': ['file'],
    #        'level': 'DEBUG' if DEBUG else 'WARNING',
    #        'propagate': True,
    #    },
    #},
}

# -----------------------------------------------------------------------------
# Third-party settings
# -----------------------------------------------------------------------------
# Email configuration: console in dev, SMTP in prod
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'medusadbt@gmail.com')

else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
