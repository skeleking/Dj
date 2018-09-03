from django.shortcuts import render

# Create your views here.
# coding:utf-8

#from django.conf import settings
#settings.configure()

import os
from django.http import HttpResponse
from django.shortcuts import render
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

    return render(request,'home.html')


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
#list_arch[]
id_of_archs=1
#==========================================================================================
#def db_add_main(request):  #the main function to add data to db
def db_add_main():
    print("add data to db")

    #return HttpResponse("ok!")

    #get_archs()

#==========================================================================================
def get_archs():  #由第一级目录生成建筑列表
    list_archs=os.listdir(my_constants.IMG_PATH)
    for str_arch in list_archs:
        if(os.path.isdir(my_constants.IMG_PATH+str_arch)):
            print(str_arch)
            myModels.Archs.objects.get_or_create(id_of_archs,str_arch,"\\")
    return list_archs

#==========================================================================================
if __name__ == '__main__':
    import sys
    print(sys.path)
    from django.conf import settings
    settings.configure()

    from pydb_webapp import models
    import dirfiles
    db_add_main()
    dirfiles.dirfiles_test()
#=========================================================================================