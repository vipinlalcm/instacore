from django import forms
from .models import Webserver


class Webserverftp(forms.ModelForm):
    php70mod_choices = [('php7.0-cgi', 'php7.0-cgi'),
                        ('php7.0-cli', 'php7.0-cli'),
                        ('php7.0-common', 'php7.0-common'),
                        ('php7.0-curl', 'php7.0-curl'),
                        ('php7.0-dbg', 'php7.0-dbg'),
                        ('php7.0-dev', 'php7.0-dev'),
                        ('php7.0-gd', 'php7.0-gd'),
                        ('php7.0-json', 'php7.0-json'),
                        ('php7.0-ldap', 'php7.0-ldap'),
                        ('php7.0-mysql', 'php7.0-mysql'),
                        ('php7.0-xmlrpc', 'php7.0-xmlrpc'),
                        ('php7.0-fpm', 'php7.0-fpm'),
                        ('php7.0-geoip', 'php7.0-geoip'),
                        ('php7.0-imagick', 'php7.0-imagick'),
                        ('php7.0-mcrypt', 'php7.0-mcrypt'),
                        ('php7.0-memcached', 'php7.0-memcached'),
                        ('php7.0-memcache', 'php7.0-memcache')]
    rootpassword = forms.CharField(widget=forms.PasswordInput, min_length=8,
                                   max_length=60)
    ftppassword = forms.CharField(widget=forms.PasswordInput, min_length=8,
                                  max_length=60)
    dbuserpassword = forms.CharField(widget=forms.PasswordInput, min_length=8,
                                     max_length=60)
    sqlrootpassword = forms.CharField(widget=forms.PasswordInput,
                                      min_length=8, max_length=60)
    phpmod = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                       choices=php70mod_choices)

    class Meta:
        model = Webserver
        fields = ['ip_address',
                  'selectos',
                  'user',
                  'rootpassword',
                  'webserver',
                  'phpversion',
                  'phpmod',
                  'ftpserver',
                  'sqlserver',
                  'documentroot',
                  'sitecount',
                  'sitename',
                  'ftpuser',
                  'ftppassword',
                  'databasename',
                  'sqlusername',
                  'dbuserpassword',
                  'sqlrootpassword']
