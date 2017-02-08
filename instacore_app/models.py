from django.db import models


class Webserver(models.Model):
    ip_address = models.GenericIPAddressField(max_length=140)
    webserver = models.CharField(max_length=50)
    documentroot = models.TextField(max_length=255)
    sitecount = models.IntegerField()
    sitename = models.TextField()
    ftpserver = models.CharField(max_length=50)
    ftpuser = models.CharField(max_length=60)
    ftppassword = models.CharField(max_length=255)

    def __str__(self):
        return self.ip_address + ' ' + self.webserver + ' ' + self.sitename
