#coding uft-8
import os
import os.path
#import pydb_webapp.models
import pydb_webapp.my_constants
#from my_constants import MAX_NAME_LENGTH
#import my_constants

# print(my_constants.MAX_NAME_LENGTH)
list_arch=[]
index_archs=1

#============================================================================
class myClass():
    """Just a test class"""
    def __init__(self, name):
        self.name = name;
        print("you have got it ,myClass")

    def func2(self):
        print("myClass.func2()")
#===========================================================================
def get_files_func1():  #os.walk 遍历所有的目录和文件
    for root, dirs, files in os.walk(pydb_webapp.my_constants.IMG_PATH):
        print(root)

def db_add_archs(str_root_dir):
#    pydb_webapp.models.Archs.objects.get_or_create(index_archs,str_root_dir,"\\") #写入建筑物表格，index，name，‘\’
    print(str_root_dir)

def get_archs():  #由第一级目录生成建筑列表

    listArchs=os.listdir(pydb_webapp.my_constants.IMG_PATH)
    for str_arch in listArchs:
        #print(my_constants.IMG_PATH + strArch)
        if os.path.isdir(pydb_webapp.my_constants.IMG_PATH + str_arch):
            db_add_archs(str_arch)

#====================================调用测试函数============================================
def dirfiles_test():
    print("dirfiles_test(): you have got it ! ")

#===========================================================================================
if __name__ == '__main__':
#get_files_func1()
    get_archs()







