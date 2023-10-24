import os

from . import env


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', 'f*)$)fay97180m+ti%xi8si##u__h(8%(ipr1z-*lsjbucooz&')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

# Disable admin
ADMIN = env.bool('DJANGO_ADMIN', True)

ALLOWED_HOSTS = [ '*' ]


# Application definition

INSTALLED_APPS = [
    'mtasks.apps.MtasksConfig',
    'partner.apps.PartnerConfig',
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

ROOT_URLCONF = 'coleman.urls'

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

WSGI_APPLICATION = 'coleman.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#
# Database config is passed in environment variable DATABASE_URL
# as string connection like postgresql://dcoleman:postgres@localhost/dcoleman_dev,
# otherwise the default SQLite database below is used.
# See more options at https://github.com/kennethreitz/dj-database-url
#
DATABASES = {
    'default': env.dj_db_url('DATABASE_URL',
                             'sqlite:///%s/db.sqlite3' % BASE_DIR,
                             conn_max_age=env.int('CONN_MAX_AGE', 600)),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR + '/static/'

# Whether to enable or not the StaticFilesHandler
# to serve the static resources from the WSGI
# server. Enabled by default if DEBUG = True,
# in production environmets it's recommended
# to serve the static resources with a reverse
# proxy like Nginx, unless little workloads
STATIC_ENABLE_WSGI_HANDLER = env.bool('STATIC_ENABLE_WSGI_HANDLER', DEBUG)


from .settings_logging import *


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


#
# Custom configurations
#

APP_NAME = env('APP_NAME', 'Forgor')
APP_EMAIL = env('APP_EMAIL', 'no-reply@localhost')
SITE_HEADER = env('SITE_HEADER', 'Forgor')
INDEX_TITLE = env('INDEX_TITLE', 'Manage Tasks')

ADMINS = (
    (APP_NAME, APP_EMAIL)
)

from .settings_emails import *
