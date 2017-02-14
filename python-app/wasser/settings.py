"""
Settings for water project.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import os

from django.utils.translation import ugettext_lazy as _

from wasser.utils import json_config

# Json config for Jenkins/Dev/Prod
CONFIG = json_config.JsonConfig.read()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = CONFIG.get(
    'BASE_DIR',
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get_bool('SECRET_KEY', False)
if SECRET_KEY is False:
    import platform
    SECRET_KEY = str(list(platform.uname()._asdict().values()))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get_bool('DEBUG', True)
if DEBUG:
    import logging
    logging.warning(
        "SECURITY WARNING: don't run with debug turned on in production!")

ALLOWED_HOSTS = CONFIG.get_list('ALLOWED_HOSTS', [])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wasser',
    'wasser.tapwater',
    'wasser.users',
    'wasser.administration',
    'wasser.login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wasser.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'wasser/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'wasser.wsgi.WSGI_APPLICATION'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': CONFIG.get(
            'DATABASE_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': CONFIG.get('DATABASE_NAME', ''),
        'USER': CONFIG.get('DATABASE_USER', ''),
        'PASSWORD': CONFIG.get('DATABASE_PASSWORD', ''),
        'HOST': CONFIG.get('DATABASE_HOST', ''),
        'PORT': CONFIG.get('DATABASE_PORT', 5432),
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization

# Accepted languages
LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'de'  # Set the default language
TIME_ZONE = CONFIG.get('TIME_ZONE', 'UTC')
USE_TZ = True  # Enable and coordinate universal time
USE_I18N = True  # Enable Internationalization
USE_L10N = True  # Enable Localization


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
LOGIN_URL = '/admin/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = CONFIG.get('DEFAULT_FROM_EMAIL', 'localhost')
EMAIL_USE_SSL = CONFIG.get_bool('EMAIL_USE_SSL', False)
EMAIL_USE_TLS = CONFIG.get_bool('EMAIL_USE_TLS', False)
EMAIL_HOST = CONFIG.get('EMAIL_HOST', 'mail')
EMAIL_HOST_USER = CONFIG.get('EMAIL_USER', 'localhost')
EMAIL_HOST_PASSWORD = CONFIG.get('EMAIL_PASSWORD', '')
EMAIL_PORT = CONFIG.get('EMAIL_PORT', 25)

# Setting google maps api key
GOOGLE_JAVASCRIPT_API_KEY = CONFIG.get('GOOGLE_JAVASCRIPT_API_KEY', "")
GOOGLE_GEO_API_KEY = CONFIG.get('GOOGLE_GEO_API_KEY', "")
HERE_MAPS_GEO_APP_CODE = CONFIG.get('HERE_MAPS_GEO_APP_CODE', "")
HERE_MAPS_GEO_APP_ID = CONFIG.get('HERE_MAPS_GEO_APP_ID', "")

# Free API without google keys. Set on True if you don't have an api key
USE_GOOGLE_API = CONFIG.get_bool('USE_GOOGLE_API', True)

SESSION_EXPIRES_SECONDS = 600  # 10 minutes
