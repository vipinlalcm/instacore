from django.db import models
from multiselectfield import MultiSelectField
# from django.core.urlresolvers import reverse
webserver_choices = [('apache2', 'Apache2'),
                     ('nginx', 'Nginx')]

ftpserver_choices = [('pure-ftpd', 'Pure-FTPd'),
                     ('proftpd', 'Pro-FTPd'),
                     ('ftp', 'FTP'),
                     ('vsftpd', 'VsFTPd')]

os_choices = [('U16', 'Ubuntu 16')]

php_ver_choices = [('php7.0', 'PHP 7.0')]

php56_modules = [('php5.6-cgi', 'php5.6-cgi'),
                 ('php5.6-cli', 'php5.6-cli'),
                 ('php5.6-common', 'php5.6-common'),
                 ('php5.6-curl', 'php5.6-curl'),
                 ('php5.6-dbg', 'php5.6-dbg'),
                 ('php5.6-dev', 'php5.6-dev'),
                 ('php5.6-gd', 'php5.6-gd'),
                 ('php5.6-json', 'php5.6-json'),
                 ('php5.6-ldap', 'php5.6-ldap'),
                 ('php5.6-mysql', 'php5.6-mysql'),
                 ('php5.6-xmlrpc', 'php5.6-xmlrpc'),
                 ('php5.6-mysql', 'php5.6-mysql'),
                 ('php5.6-fpm', 'php5.6-fpm'),
                 ('php5.6-geoip', 'php5.6-geoip'),
                 ('php5.6-imagick', 'php5.6-imagick'),
                 ('php5.6-mcrypt', 'php5.6-mcrypt'),
                 ('php5.6-memcached', 'php5.6-memcached'),
                 ('php5.6-memcache', 'php5.6-memcache')]

php5mod_choices = [('php5-cgi', 'php5-cgi'),
                   ('php5-cli', 'php5-cli'),
                   ('php5-common', 'php5-common'),
                   ('php5-curl', 'php5-curl'),
                   ('php5-dbg', 'php5-dbg'),
                   ('php5-dev', 'php5-dev'),
                   ('php5-gd', 'php5-gd'),
                   ('php5-json', 'php5-json'),
                   ('php5-ldap', 'php5-ldap'),
                   ('php5-mysql', 'php5-mysql'),
                   ('php5-xmlrpc', 'php5-xmlrpc'),
                   ('php5-mysql', 'php5-mysql'),
                   ('php5-fpm', 'php5-fpm'),
                   ('php5-geoip', 'php5-geoip'),
                   ('php5-imagick', 'php5-imagick'),
                   ('php5-mcrypt', 'php5-mcrypt'),
                   ('php5-memcached', 'php5-memcached'),
                   ('php5-memcache', 'php5-memcache')]


sqldatabase_choices = [('mysql-server-5.6', 'mysql-server-5.6'),
                       ('mysql-server-5.7', 'mysql-server-5.7'),
                       ('percona-server-server-5.6',
                        'percona-server-server-5.6')]


class Webserver(models.Model):
    php70mod_choices = [('php7.0-cgi', 'php7.0-cgi'),
                        ('php7.0-cli', 'php7.0-cli'),
                        ('php7.0-common', 'php7.0-common'),
                        ('php7.0-fpm', 'php7.0-fpm'),
                        ('php7.0-mcrypt', 'php7.0-mcrypt'),
                        ('php7.0-curl', 'php7.0-curl'),
                        ('php7.0-dev', 'php7.0-dev'),
                        ('php7.0-gd', 'php7.0-gd'),
                        ('php7.0-gmp', 'php7.0-gmp'),
                        ('php7.0-json', 'php7.0-json'),
                        ('php7.0-ldap', 'php7.0-ldap'),
                        ('php7.0-mysql', 'php7.0-mysql'),
                        ('php7.0-odbc', 'php7.0-odbc'),
                        ('php7.0-opcache', 'php7.0-opcache'),
                        ('php7.0-pgsql', 'php7.0-pgsql'),
                        ('php7.0-pspell', 'php7.0-pspell'),
                        ('php7.0-readline', 'php7.0-readline'),
                        ('php7.0-recode', 'php7.0-recode'),
                        ('php7.0-snmp', 'php7.0-snmp'),
                        ('php7.0-sqlite3', 'php7.0-sqlite3'),
                        ('php7.0-tidy', 'php7.0-tidy'),
                        ('php7.0-xml', 'php7.0-xml'),
                        ('php7.0-xmlrpc', 'php7.0-xmlrpc'),
                        ('php7.0-bcmath', 'php7.0-bcmath'),
                        ('php7.0-bz2', 'php7.0-bz2'),
                        ('php7.0-enchant', 'php7.0-enchant'),
                        ('php7.0-imap', 'php7.0-imap'),
                        ('php7.0-interbase', 'php7.0-interbase'),
                        ('php7.0-intl', 'php7.0-intl'),
                        ('php7.0-mbstring', 'php7.0-mbstring'),
                        ('php7.0-phpdbg', 'php7.0-phpdbg'),
                        ('php7.0-soap', 'php7.0-soap'),
                        ('php7.0-sybase', 'php7.0-sybase'),
                        ('php7.0-xsl', 'php7.0-xsl'),
                        ('php7.0-zip', 'php7.0-zip'),
                        ('php7.0-dba', 'php7.0-dba')]
    ip_address = models.GenericIPAddressField(max_length=20)
    selectos = models.CharField(max_length=20,
                                choices=os_choices, default='U16')
    user = models.CharField(max_length=20, default='root')
    rootpassword = models.CharField(max_length=40,default='')
    port = models.CharField(max_length=6, default=22)
    webserver = models.CharField(max_length=20, choices=webserver_choices,
                                 default='apache2')
    documentroot = models.CharField(max_length=100,default='')
    sitecount = models.IntegerField()
    sitename = models.CharField(max_length=100,default='')
    ftpserver = models.CharField(max_length=20, choices=ftpserver_choices,
                                 default='vsftpd')
    ftpuser = models.CharField(max_length=20,default='')
    ftppassword = models.CharField(max_length=40,default='')
    phpversion = models.CharField(max_length=20, choices=php_ver_choices,
                                  default='php7.0')
    phpmod = MultiSelectField(max_length=255, choices=php70mod_choices,
                              default='')
    sqlserver = models.CharField(max_length=20,
                                 choices=sqldatabase_choices,
                                 default='mysql-server-5.7')
    databasename = models.CharField(max_length=20,default='' )
    sqlusername = models.CharField(max_length=20,default='')
    dbuserpassword = models.CharField(max_length=40,default='')
    sqlrootpassword = models.CharField(max_length=40,default='')

    # def get_absolute_url(self):
    #     return reverse('instacore_app:web_details', kwargs={'pk': self.pk})

    # def __str__(self):
    #    return self.ip_address + ' ' + self.webserver + ' ' + self.sitename
