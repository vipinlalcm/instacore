from django.conf.urls import url
from . import views

app_name = 'instacore_app'

urlpatterns = [
    url(r'^$', views.lamp, name='lamp'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<pk>[0-9]+)/$', views.DetailedView.as_view(),
        name='web_details'),
    url(r'^download/(?P<pk>[0-9]+)/$', views.download, name='download'),
    # url(r'^upload/$', views.upload, name='upload')
]
