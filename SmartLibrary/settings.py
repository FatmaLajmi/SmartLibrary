from pathlib import Path
import os
from decouple import config

# ----------------------------
#   BASE DIR
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
#   SECURITY
# ----------------------------
SECRET_KEY = 'django-insecure-r%)39f4mtmsj&o71c34yjle)ehnaoqun7f=3f@=vc)wej%=hf-'
DEBUG = True
ALLOWED_HOSTS = []

# ----------------------------
#   INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'LivreApp',
    'LivreAppApi',
    'AvisApp',
    'AvisAppApi',
    'PanierApp',
    'PanierAppApi',
    'UserApp',       
    'ProfileApp',
    'StockApp',
    'ChatApp',
    'ChatAppApi',
]
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
}


# ----------------------------
#   MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------
#   URL CONF
# ----------------------------
ROOT_URLCONF = 'SmartLibrary.urls'

# ----------------------------
#   TEMPLATE CONFIG
# ----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'SmartLibrary/template'],
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

# ----------------------------
#   WSGI
# ----------------------------
WSGI_APPLICATION = 'SmartLibrary.wsgi.application'

# ----------------------------
#   DATABASE
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_USER_MODEL = 'UserApp.Utilisateur'

# ----------------------------
#   PASSWORD VALIDATION
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------
#   LANGUAGE / TIME
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------
#   STATIC FILES
# ----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # dossier static global
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # dossier collectstatic

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ----------------------------
#   MEDIA FILES
# ----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------
#   DEFAULT AUTO FIELD
# ----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------
#   CUSTOM USER MODEL
# ----------------------------
AUTH_USER_MODEL = 'UserApp.Utilisateur'
# Redirection après login
LOGIN_REDIRECT_URL = 'index'  # page after login
LOGIN_URL = 'login'  # redirect here when login is required
LOGOUT_REDIRECT_URL = 'index'  # page after logout

# ----------------------------
#   EMAIL CONFIGURATION
# ----------------------------
# Toggle email integration (default: disabled)
# Set the environment variable or .env value `EMAIL_ENABLED=true` to enable SMTP.
EMAIL_ENABLED = config('EMAIL_ENABLED', default=False, cast=bool)

if EMAIL_ENABLED:
    # Configuration pour Gmail (production)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = 'SmartLibrary <noreply@smartlibrary.com>'
    SERVER_EMAIL = 'SmartLibrary <noreply@smartlibrary.com>'
else:
    # Backend pour le développement (affiche les emails en console)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'SmartLibrary <noreply@smartlibrary.com>'
    SERVER_EMAIL = 'SmartLibrary <noreply@smartlibrary.com>'

# Password reset timeout (1 jour = 86400 secondes)
PASSWORD_RESET_TIMEOUT = 86400


import os
from pathlib import Path

# BASE_DIR est déjà défini comme ceci dans Django 5+ :
BASE_DIR = Path(__file__).resolve().parent.parent


    
# Toggle Gemini AI integration (default: disabled)
# Set the environment variable or .env value `GEMINI_ENABLED=true` to enable.
GEMINI_ENABLED = config('GEMINI_ENABLED', default=False, cast=bool)


