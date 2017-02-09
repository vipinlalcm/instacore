from django.conf.urls import url
from . import views

app_name = 'instacore_app'

urlpatterns = [
    url(r'^$', views.WebserverCreate.as_view(),
        name='webserver-add'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<pk>[0-9]+)/$', views.DetailView.as_view(),
        name='web_details'),
    # url(r'^upload/$', views.upload, name='upload')
]
