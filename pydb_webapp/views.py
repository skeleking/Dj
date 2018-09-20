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
import json
from Dj1 import settings

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

    #return render(request,'home.html',context={'建筑群':archs_datasets})

    #template1=loader.get_template(template_name='home.html')
    #tem_to_str= loader.render_to_string(template1,context={'建筑群s': archs_datasets})
    #return HttpResponse(tem_to_str)

    # archs_datasets = myModels.Archs.objects.all()
    # archs=['万木草堂','崔氏宗祠','梁氏大宗祠']

    #================================从静态资源中加载dirs_files.json===========================
    with open((settings.STATICFILES_DIRS[0] + "\\dirs_files.json"), 'r', encoding='utf-8') as f_dirs_files_json:
        dic_dirs_files=json.load(f_dirs_files_json)
    #return render(request, template_name='index.html', context={'arch_list': archs_datasets} )
    return render(request, template_name='index.html', context={"pydb_structure": dic_dirs_files} )


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