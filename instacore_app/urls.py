from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^lamp/$', views.lamp, name='lamp'),
    url(r'^upload/$', views.upload, name='upload')
]
