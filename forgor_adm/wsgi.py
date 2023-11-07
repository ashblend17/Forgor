import os

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

from forgor_adm import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forgor_adm.settings")

if settings.STATIC_ENABLE_WSGI_HANDLER:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
