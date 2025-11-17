from pathlib import Path
import os

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
    'UserApp',       # 🔹 ajoute cette ligne
    'ProfileApp'
    # Nos apps
    
]


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
        'DIRS': [BASE_DIR / 'SmartLibrary' / 'templates'],
  # dossier templates global
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
LOGIN_REDIRECT_URL = '/profile/'  # 🔹 redirige vers ta page profile
LOGOUT_REDIRECT_URL = '/accounts/login/'  # 🔹 redirige vers login après logout
