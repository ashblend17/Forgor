from django.urls import re_path, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import routers
from mtasks.serializers import TaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    re_path('^api/v1/', include(router.urls)),
]

if settings.ADMIN:
    urlpatterns = [
        re_path(r'^$', lambda r: HttpResponseRedirect('admin/')),   # Remove this redirect if you add custom views
        path('admin/', admin.site.urls),
    ] + urlpatterns

admin.site.site_title = admin.site.site_header = settings.SITE_HEADER
admin.site.index_title = settings.INDEX_TITLE
