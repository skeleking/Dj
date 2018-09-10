from django.shortcuts import render

# Create your views here.
# coding:utf-8

#from django.conf import settings
#settings.configure()

import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from pydb_webapp import models as myModels
from pydb_webapp import my_constants

#===================================================================================
b_addtodb = True
#===================================================================================
#网页访问模块

def index(request):
    #return HttpResponse(u"Welcome to py's WebSite!...6")
    #if(b_addtodb):
    #    try:
    #        db_add_main()
    #   except:
    #        print("try db_add_main error!")
    archs_datasets=myModels.Archs.objects.all()
    #return render(request,'home.html',context={'建筑群':archs_datasets})
    #template1=loader.get_template(template_name='home.html')
    #tem_to_str= loader.render_to_string(template1,context={'建筑群s': archs_datasets})
    #return render(request ,template_name='home.html',context={'建筑群':archs_datasets})
    #return HttpResponse(tem_to_str)
    archs=['万木草堂','崔氏宗祠','梁氏大宗祠']
    return render(request, template_name='index.html', context={'arch_list': archs_datasets} )


def add(request):
    a = request.GET.get('a',4)
    # a = request.GET['a']
    b = request.GET.get('b', 5)
    # b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))

def add2(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(str(c))
#========================================以下为数据库操作部分==================================================
#数据库入库部分单独放了一个python文件中
#==========================================================================================

#=========================================================================================