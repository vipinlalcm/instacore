from django.http import Http404
from django.shortcuts import render
from .models import Webserver


def home(request):
    return render(request, 'instacore_app/layout.html')


def lamp(request):
    try:
        details = Webserver.objects.all()
    except Webserver.DoesNotExist:
        raise Http404("Webserver details does not exist")
    return render(request, 'instacore_app/lamp.html',
                  {'details': details})


def upload(request):
    return render(request, 'instacore_app/layout.html')
