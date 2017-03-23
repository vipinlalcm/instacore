import shutil
# import subprocess
import os
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from .models import Webserver
from .forms import Webserverftp
from .ansible_config import Generate, Ansible_Config
from .tasks import run_task
from celery.result import AsyncResult
import json
# from django.core.urlresolvers import reverse


class HomeView(generic.ListView):
        template_name = 'instacore_app/home.html'
        context_object_name = 'all_details'

        def get_queryset(self):
            return Webserver.objects.all()


class DetailedView(generic.DetailView):
    model = Webserver
    template_name = 'instacore_app/details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailedView, self).get_context_data(**kwargs)
        context['form'] = submit
        return context


def submit(request, pk):
    get_path = Ansible_Config.Get_Values(pk)
    playbook_file = (get_path.instance_path + '/playbook.yml')
    inventory_file = (get_path.inventory_path + 'production')
    log_path = (os.getcwd() + '/' + get_path.log_path + 'instance.log')
    cookbook_path = (os.getcwd() + '/' + get_path.instance_path)
    ansible_config_path = (get_path.instance_path + '/ansible.cfg')
    data = Webserver.objects.get(pk=pk)
    if request.method == 'POST' and request.POST.get("cancel"):
        return redirect('/')
    elif request.method == 'POST' and request.POST.get("install"):
        if not os.path.exists(get_path.instance_path):
            Generate(pk)
            job = run_task.delay(ansible_config_path, log_path, inventory_file,
                                 playbook_file)
            return redirect("/run/" + '?job=' + job.id)
        else:
            job = run_task.delay(ansible_config_path, log_path, inventory_file,
                                 playbook_file)
            return redirect("/run/" + '?job=' + job.id)
    else:
        messages.info(request,
                      'We are ready to\
                       continue with installation of  the ipaddress %s \n \
                       Click Install button to start the installation.'
                      % data.ip_address,
                      extra_tags='safe')
        messages.info(request,
                      'You can find the corresponded ansible cookbook here:\
                      %s' % cookbook_path,
                      extra_tags='safe')
        messages.info(request,
                      'You can find the current playbook execution logs in the \
                      following file:\
                      %s' % log_path,
                      extra_tags='safe')
        return render(request, 'instacore_app/submit_form.html',
                      {'data': data.ip_address})


def run(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.state or job.result
        context = {
            'data': data,
            'task_id': job_id,
        }
        return render(request, "instacore_app/show_status.html", context)
    else:
        return HttpResponse('No job id given.')


# Create your views here.
def run_state(request):

    """ A view to report the progress to the user """
    task_id = request.POST['task_id']
    task = AsyncResult(task_id)
    data = task.get()
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            state = task.get()
            if "SYNTAX_FAIL" in state:
                json_data = json.dumps({"message": "Syntax error!", "state": "SYNTAX_FAIL"})
                return HttpResponse(json_data, content_type='application/json')
            elif "PING_FAIL" in state:
                json_data = json.dumps({"message": "Ping failed!", "state": "PING_FAIL"})
                return HttpResponse(json_data, content_type='application/json')
            elif "EXECUTION_FAIL" in state:
                json_data = json.dumps({"message": "Playbook execution failed!", "state": "EXECUTION_FAIL"})
                return HttpResponse(json_data, content_type='application/json')
            elif "SUCCESS" in state:
                json_data = json.dumps({"message": "Completed installation!", "state": "SUCCESS"})
                return HttpResponse(json_data, content_type='application/json')
            else:
                data = task.result or task.state
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type='application/json')
        else:
            data = 'No task_id in the request'
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
    else:
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def sitecount_check(sitecount, sitename):
    if sitecount > 1:
        if ',' in sitename:
            s = sitename.split(',')
            f = [str(x) for x in s]
            split = list(map(str.strip, f))
            print(split)
            length = len(split)
            if sitecount == length:
                return True
            else:
                return False
        else:
            return False
    elif sitecount == 1 and ',' not in sitename:
        return True
    else:
        return False


def status(request):
    return render(request, 'instacore_app/status.html')


def lamp(request):
    if request.method == 'POST':
        form = Webserverftp(request.POST)
        if form.is_valid():
            sitecount = form.cleaned_data.get('sitecount')
            sitename = form.cleaned_data.get('sitename')
            form.save(commit=False)
            if request.POST.get("download"):
                if sitecount_check(sitecount, sitename):
                    form.save()
                    Generate(form.instance.id)
                    return redirect('/download/' + str(form.instance.id) + '/')
                else:
                    messages.error(request,
                                   'Sitecount did not match with given\
                                    Sitenames',
                                   extra_tags='safe')
                    return redirect('/status/')
            elif request.POST.get("continue"):
                if sitecount_check(sitecount, sitename):
                    form.save()
                    Generate(form.instance.id)
                    return redirect('/submit/' + str(form.instance.id) + '/')

                else:
                    messages.error(request,
                                   'Sitecount did not match with given\
                                    Sitenames',
                                   extra_tags='safe')
                    return redirect('/status/')
    else:
        form = Webserverftp()
    return render(request, 'instacore_app/webserver_form.html',
                  {'form': form})


def download(request, pk):
    get_path = Ansible_Config.Get_Values(pk)
    source = get_path.instance_path
    download_path = (os.getcwd() + '/download/')
    dst_filename = (download_path + source)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(source):
        Generate(pk)
        shutil.make_archive(dst_filename, 'zip', source)
    else:
        shutil.make_archive(dst_filename, 'zip', source)
    file_path = (dst_filename + '.zip')
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper,
                            content_type="application/x-zip-compressed")
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = 'attachment; \
                                       filename="%s.zip"' % source
    response['X-Sendfile'] = file_path
    return response
