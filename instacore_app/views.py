from django.views import generic
from django.views.generic.edit import CreateView
from .models import Webserver


class HomeView(generic.ListView):
        template_name = 'instacore_app/home.html'
        context_object_name = 'all_details'

        def get_queryset(self):
            return Webserver.objects.all()


class DetailView(generic.DetailView):
    model = Webserver
    template_name = 'instacore_app/details.html'


class WebserverCreate(CreateView):
    model = Webserver
    fields = ['ip_address', 'webserver', 'documentroot', 'sitecount',
              'sitename', 'ftpserver', 'ftpuser', 'ftppassword']
