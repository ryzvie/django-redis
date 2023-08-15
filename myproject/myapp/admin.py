from django.contrib import admin
from .models import *
# Register your models here.

class DataSourceCivilAdmin(admin.ModelAdmin):
    fields = ['alamat', 'telp', 'userid', 'group', 'status']
    list_display = ('alamat', 'telp', 'userid', 'group', 'status', 'created_dt', 'update_dt')
    list_filter = ['status']

class DataSourceGroupAdmin(admin.ModelAdmin):
    fields = ['namagroup', 'initial']
    list_display = ('namagroup', 'initial')
    list_filter = ['namagroup']

class DataSourceStatusAdmin(admin.ModelAdmin):
    fields = ['status']
    list_display = ('status',)
    list_filter = ['status']

admin.site.register(DataCivil, DataSourceCivilAdmin)
admin.site.register(DataGroup, DataSourceGroupAdmin)
admin.site.register(DataStatus, DataSourceStatusAdmin)