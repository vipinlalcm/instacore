from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('instacore_app.urls')),
    url(r'^', include('favicon.urls')),
]
