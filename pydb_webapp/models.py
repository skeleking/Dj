from django.db import models

from PIL import Image
#import my_constants
from pydb_webapp import my_constants
# Create your models here.

#MAX_NAME_LENGTH = 60
#class ItemObj(models.Model):
#    index=models.IntegerField()
#    name=models.CharField(max_length= constants.MAX_NAME_LENGTH)

class Archs(models.Model):
    #id_archs = models.IntegerField()  #不需要id，入库分配麻烦，而且没什么用
    #arch_name = models.CharField(max_length = my_constants.MAX_NAME_LENGTH)
    arch_name = models.CharField(max_length= my_constants.MAX_NAME_LENGTH,primary_key=True, default='no_arch')
    root_dir = models.CharField(max_length= my_constants.MAX_NAME_LENGTH ,default='\\')

    def __str__(self):
        return self.arch_name

class Directories(models.Model):
    #dir_name = models.CharField(max_length= my_constants.MAX_NAME_LENGTH,primary_key=True, default='no_dir')#设为主键，但是不同的建筑群，可能有相同的结构名称，如“中厅”，引起UNIQE constraints 错误

    dir_name = models.CharField(max_length=my_constants.MAX_NAME_LENGTH, default='none')
    arch =models.CharField(max_length= my_constants.MAX_NAME_LENGTH, default='none')
    root_dir = models.CharField(max_length= my_constants.MAX_NAME_LENGTH, default= 'none')

    def __str__(self):
        return self.dir_name + 'belongs to : '+ self.arch +' ,'+ '父节点是 ' + self.root_dir


class Imgfiles(models.Model):
    file_name = models.ImageField(upload_to='img', default= 'none.img')
    arch = models.CharField(max_length= my_constants.MAX_NAME_LENGTH, default='none')
    outer = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH , default='none')
    site = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
    location = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
    content = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
    nmch_type= models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
    p_or_d = models.CharField(max_length= my_constants.MAX_SIMPLE_LENGTH, default='none')
    description = models.CharField(max_length=my_constants.MAX_DESCRIPTION_LENGTH, default='none')
    drawing_num = models.CharField(max_length=my_constants.MAX_SIMPLE_LENGTH, default='none')

    #def __init__(self):
     #   """初始化类"""
    def __str__(self):
        return (self.file_name , self.arch, self.outer, self.site, self.location, self.content, self.nmch_type, self.p_or_d, self.description, '测绘原图编号'+ self.drawing_num)



