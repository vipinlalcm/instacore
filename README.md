Welcome to Instacore app
========================

"instacore" means INSTall And Configure Remotely. It is a control panel which allows you to provide the details of the packages and install those in a remote machine. 

Installation
=============
Packages required.
1) python 3.5.2
2) virtualenv
3) pip
```sh
$ virtualenv --python=python3.5 venv
$ source venv/bin/activate
$ git clone git@git.cygate.io:vipicm/instacore.git
$ cd instacore
$ pip install -r requirements.txt
```
How to run
============
```sh
$ source venv/bin/activate
$ cd instacore
$ celery -A instacore_app worker -l info &
$ python manager.py runserver
```