from django.contrib import admin

# Register your models here.

from django.contrib import admin
#from pydb_webapp.models import Archs

from pydb_webapp import models

class ArchsAdmin(admin.ModelAdmin):
    list_display = ('arch_name','root_dir')
class DirectoriesAdmin(admin.ModelAdmin):
    list_display = ('dir_name','arch','root_dir')


# class Imgfiles(models.Model):
#     file_name = models.ImageField(upload_to='img', default= 'none.img')
#     arch = models.CharField(max_length= my_constants.MAX_NAME_LENGTH, default='none')
#     outer = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH , default='none')
#     site = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
#     location = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
#     content = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
#     nmch_type= models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
#     description = models.CharField(max_length=my_constants.MAX_DESCRIPTION_LENGTH, default='none')
#     drawing_num = models.CharField(max_length=my_constants.MAX_SIMPLE_LENGTH, default='none')
class ImagefilesAdmin(admin.ModelAdmin):
    list_display = ('file_name','arch','outer','site','location','content','nmch_type','p_or_d','description','drawing_num')

#admin.AdminSite.register([models.Archs,models.Directories,models.Imgfiles]    )
admin.AdminSite.register(admin.site , model_or_iterable=models.Archs,admin_class= ArchsAdmin)
admin.AdminSite.register(admin.site, model_or_iterable=models.Directories, admin_class= DirectoriesAdmin)
admin.AdminSite.register(admin.site, model_or_iterable=models.Imgfiles, admin_class= ImagefilesAdmin)

