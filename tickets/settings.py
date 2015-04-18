"""
Django settings for tickets project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.templatetags.static import static

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.contrib.messages import constants as messages_constants
from django.utils.translation import ugettext as _

MESSAGE_TAGS = {
    messages_constants.ERROR: 'danger',
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5ns0a$tliisetv_f-nr_4-re%clfxk9mz20@$02v6u@+9w3h=d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'bootstrap3',
    'rest_framework',
    'rest_framework.authtoken',
    'django_bootstrap_breadcrumbs',
    # 'modeltranslation',
    'simplemathcaptcha',
    'django_countries',
    'common',
    'login',
    'ticketing',
    'dashboard',
    'restserver',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = {
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'tickets.urls'

WSGI_APPLICATION = 'tickets.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'login.TicketsUser'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

gettext = lambda s: s

LANGUAGES = (
    ('en', 'English'),
    ('fr', 'Français'),
)

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# SESSIONS
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600 # 10 minutes

# CONFIG DE L'EMAIL SORTANT
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "ticketing.platform@gmail.com"
EMAIL_HOST_PASSWORD = "aK#7s8%P"
EMAIL_PORT = 587

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# Settings personnalisés
# Définit le lien inclus dans les emails envoyés par le site aux users. (défaut: "127.0.0.1/home/")
MY_EMAIL_SITE_LINK = "http://ticketplatform.no-ip.org:2337"
# Est-ce que les nouveaux comptes créés manuellement sont acceptés? (défaut: False)
MY_REGISTRATION_ENABLED = True
# PATH du dossier racine pour les images tickets postées via Android
MY_ANDROID_PICTURES_PATH = os.path.join(BASE_DIR, "media")
# print(MY_ANDROID_PICTURES_PATH)