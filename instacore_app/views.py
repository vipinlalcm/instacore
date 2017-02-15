from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
# from django.shortcuts import HttpResponse
from django.views import generic
# from django.http import Http404
from .models import Webserver
from .forms import Webserverftp


class HomeView(generic.ListView):
        template_name = 'instacore_app/home.html'
        context_object_name = 'all_details'

        def get_queryset(self):
            return Webserver.objects.all()


class DetailedView(generic.DetailView):
    model = Webserver
    template_name = 'instacore_app/details.html'


def lamp(request):
    form = Webserverftp(request.POST)
    if request.method == 'POST' and form.is_valid():
        form.save()
        if request.POST.get("download"):
            return HttpResponseRedirect('/download/' +
                                        str(form.instance.id) + '/')
        elif form.cleaned_data.get('ip_address'):
            return HttpResponseRedirect('/home/' + str(form.instance.id) + '/')
    else:
        form = Webserverftp()
    return render(request, 'instacore_app/webserver_form.html', {'form': form})


def download(request, pk):
    data = Webserver.objects.get(pk=pk)
    return render(request, 'instacore_app/download.html', {'data': data})
