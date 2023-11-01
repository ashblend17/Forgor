import os
from . import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env('SECRET_KEY', 'f*)$)fay97180m+ti%xi8si##u__h(8%(ipr1z-*lsjbucooz&')
DEBUG = env.bool('DEBUG', True)

ADMIN = env.bool('DJANGO_ADMIN', True)

ALLOWED_HOSTS = [ '*' ]

INSTALLED_APPS = [
    'mtasks.apps.MtasksConfig',
    'django_admin_listfilter_dropdown',
    'adminfilters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
]

REST_ENABLED = env.bool('REST_ENABLED', False)
if REST_ENABLED:
    INSTALLED_APPS += ['rest_framework']

if not REST_ENABLED and not ADMIN:
    raise ValueError('You either have to enable REST_ENABLED or DJANGO_ADMIN')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'forgor_adm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'forgor_adm.wsgi.application'

#Database

DATABASES = {
    'default': env.dj_db_url('DATABASE_URL',
                             'sqlite:///%s/db.sqlite3' % BASE_DIR,
                             conn_max_age=env.int('CONN_MAX_AGE', 600)),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


#Pass validation

AUTH_PASSWORD_VALIDATORS_ENABLED = env.bool('AUTH_PASSWORD_VALIDATORS_ENABLED', True)
if AUTH_PASSWORD_VALIDATORS_ENABLED:
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


# Internationalization

LANGUAGE_CODE = env('LANGUAGE_CODE', 'en-us')

TIME_ZONE = env('TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True


from django.conf.locale.es import formats as es_formats
es_formats.DATETIME_FORMAT = 'd M Y, H:i'
es_formats.DATE_FORMAT = 'd M, Y'


from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = 'M d Y, H:i'
en_formats.DATE_FORMAT = 'M d, Y'

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR + '/static/'

STATIC_ENABLE_WSGI_HANDLER = env.bool('STATIC_ENABLE_WSGI_HANDLER', DEBUG)

from .settings_logging import *


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

APP_NAME = env('APP_NAME', 'Forgor')
APP_EMAIL = env('APP_EMAIL', 'no-reply@localhost')
SITE_HEADER = env('SITE_HEADER', 'Forgor')
INDEX_TITLE = env('INDEX_TITLE', 'Manage Tasks')

ADMINS = (
    (APP_NAME, APP_EMAIL)
)

from .settings_emails import *
