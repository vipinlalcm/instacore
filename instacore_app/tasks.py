from __future__ import absolute_import
from celery import task
import celery
# from numpy import random
# from scipy.fftpack import fft
# alternative https://djangosnippets.org/snippets/2898/
# reference http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/
import os
import subprocess


@task
def run_task(ansible_config_path, log_path, inventory_file, playbook_file):
    os.environ["ANSIBLE_CONFIG"] = str(ansible_config_path)
    os.environ["ANSIBLE_LOG_PATH"] = str(log_path)
    if not os.path.exists(playbook_file) or not os.path.exists(inventory_file):
        return celery.states.FAILURE
    else:
        synt_check_cmd = ['ansible-playbook',
                          '--syntax-check', '-i',
                          inventory_file,
                          playbook_file]
        syntcheck = subprocess.Popen(synt_check_cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        pingresult, err = syntcheck.communicate()
        syntcheck_satus = syntcheck.returncode
        if syntcheck_satus > 0:
            return 'SYNTAX_FAIL'
        else:
            cmd = ['ansible', '-i', inventory_file, 'all', '-m' 'ping']
            ping = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            pingresult, err = ping.communicate()
            pingstatus = ping.returncode
            if pingstatus > 0:
                return 'PING_FAIL'
            else:
                run_cmd = ['ansible-playbook', '-v', '-i',
                           inventory_file,
                           playbook_file]
                pb_run = subprocess.Popen(run_cmd,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
                playbookresult, err = pb_run.communicate()
                playstatus = pb_run.returncode
                if playstatus > 0:
                    return 'EXECUTION_FAIL'
                else:
                    return 'SUCCESS'
