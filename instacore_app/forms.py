from django import forms
from .models import Webserver
webserver_choices = [('apache2', 'apache2'), ('nginx', 'nginx')]
ftpserver_choices = [('pure-ftpd', 'pure-ftpd'), ('proftpd', 'proftpd'),
                     ('ftp', 'ftp'), ('vsftpd', 'vsftpd')]


class Webserverftp(forms.ModelForm):
    ftppassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Webserver
        fields = ['webserver', 'documentroot', 'sitecount', 'sitename',
                  'ftpserver', 'ftpuser', 'ftppassword']
