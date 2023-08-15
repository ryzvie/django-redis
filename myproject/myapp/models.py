from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DataGroup(models.Model):
    namagroup = models.TextField("Nama Group", null=True, blank=True)
    initial = models.TextField("Initial", null=True, blank=True)

    class Meta:

        verbose_name = 'Data Group'
        verbose_name_plural = 'Data Group'

    def __str__(self):
        return self.namagroup

class DataStatus(models.Model):
    status = models.TextField("Status", null=True, blank=True)

    class Meta:

        verbose_name = 'Data Status'
        verbose_name_plural = 'Data Status'

    def __str__(self):
        return self.status
    
class DataCivil(models.Model):

    userid = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    alamat = models.TextField('Alamat')
    status = models.ForeignKey(DataStatus, on_delete=models.CASCADE)
    telp = models.TextField('Telp', null=True, blank=True)
    group = models.ForeignKey(DataGroup, on_delete=models.CASCADE)
    created_dt = models.DateTimeField('Created Date', auto_now=False, auto_now_add=True)
    update_dt = models.DateTimeField('Update Date', null=True, blank=True, auto_now=False, auto_now_add=False)

    class Meta:

        verbose_name = 'Data CIvil'
        verbose_name_plural = 'Data Civil'

    def __str__(self):
        return self.userid.username
    
