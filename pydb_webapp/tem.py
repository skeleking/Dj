import os
import sys
from pydb_webapp import my_constants
from pydb_webapp import models as myModels
import json
import dirfiles


#========================================以下为数据库操作部分==================================================

#==========================================================================================
def db_add_main():  #the main function to add data to db
    print("add data to db")
    list_archs = []
    list_json = {}  # 字典 list_json{"崔氏宗祠":"崔氏宗祠.json"},...}
    list_walk_results = []
    contents_of_json = {}
    dic_of_jpg={}

    list_archs=create_archs()
    print(list_archs)
    for str_arch in list_archs :
        list_tmp=os.listdir(my_constants.IMG_PATH+ str_arch)
        if (str_arch +'.json') in list_tmp :                #如果存在json文件，则将此信息保存在字典list_json，并打开文件，读取信息到contents_of_json
            #list_json.append({str_arch :str_arch + '.json' })
            list_json[str_arch]=str_arch +'.json'
            with open(my_constants.IMG_PATH+ str_arch+ '\\'+ list_json[str_arch], 'r') as f_json_obj:
                contents_of_json=json.load(f_json_obj)
        else:
            print("no "+ str_arch+'.json  file in '+ str_arch)

        list_walk_results =os.walk(my_constants.IMG_PATH + str_arch)
        list_walk_record1=list_walk_results.__next__()
        try:
            while list_walk_record1.__len__()>0 : #这里只要还有记录，len应该恒等于3
                if list_walk_record1[1].__len__() >0: #如果存在子目录，执行将子目录信息入库
                    print("当前记录存在子目录，记录是： ", list_walk_record1)
                    #print("create subdir record: ",list_walk_record1)
                    create_directories(str_arch,list_walk_record1)
                if list_walk_record1[2].__len__() >0: #如果存在文件
                    print("当前记录存在文件，记录是： ", list_walk_record1)
                    #================================================================
                    #list_walk_record格式['path',[subdirs],[files]]
                    #list_walk_record1[2]是一个文件名列表['file1.ext','file2.ext',...]
                    #================================================================
                    for str_filename in list_walk_record1[2]:
                        print(str_filename)
                        if(str_filename.rfind('.jpg')!=-1):#如果确认是.jpg文件
                            print("found "+str_filename)
                            #======读取文件对应的json信息，传递给入库函数======
                            #如果存在此JPG文件的json文件，则入库
                            if str_filename in contents_of_json.keys():
                                dic_of_jpg=contents_of_json[str_filename]#临时存放JPG文件的json信息
                                print(dic_of_jpg)
                                # dic_of_jpg的格式是{
                                #         "arch": "崔氏宗祠",
                                #         "outer": "室内",
                                #         "site": "后座",
                                #         "location": "屋顶",
                                #         "content": "屋脊",
                                #         "nmch_type": "灰塑",
                                #         "description": "广州市番禺区大学城崔氏宗祠的后座垂脊博古大样，由广州大学建筑与城市规划学院测绘于2018年。",
                                #         "测绘图原稿图号": ""
                                #       }
                                create_imgfiles(str_arch, str_filename, dic_of_jpg)
                            else:
                                print("缺乏 "+ str_filename + " 的json文件")
                                pass
                        else:
                            print(str_filename + "  不是jpg文件，忽略入库操作")
                            pass



                list_walk_record1 =list_walk_results.__next__()
        except:
            continue   #迭代一个建筑结束，此处需要继续for循环。用pass效果相同

        # list_temp = get_subdirs_and_files(my_constants.IMG_PATH + str_arch)
        # print('subdirs of '+ str_arch + ' is : ')
        # print(list_temp[0] )
        #
        # print("files of " + str_arch + " is : ")
        # print(list_temp[1])

#==========================================================================================
def create_archs():
    """由第一级目录生成建筑列表。此目录下不应该有别的文件，忽略其他文件。"""

    list_archs2=os.listdir(my_constants.IMG_PATH)
    list_dirs=[]
    for str_arch in sorted(list_archs2):
        if(os.path.isdir(my_constants.IMG_PATH+str_arch)):
            #print(str_arch)
            list_dirs.append(str_arch)
            try:
                #myModels.Archs.objects.get_or_create(defaults={'id_archs':id_of_archs},arch_name=str_arch,root_dir="\\") #注意此处defaults用法
                if myModels.Archs.objects.get_or_create( arch_name=str_arch,root_dir="\\")[1]:
                    print(str_arch + "    created in table pydb_webapp_archs")
                else:
                    print(str_arch + "    exists in table pydb_webapp_archs")
            except:
                print("myModels.Archs.objects.get_or_create()  error")

    return list_dirs
#==========================================================================================
# def create_directories(arch): #此处约等于重现了一次os.walk
#     # print("the arch is :",arch)
#     # list_dir1=os.listdir(my_constants.IMG_PATH+ arch)
#     # for str_dir_or_file in sorted(list_dir1):
#     #     if(os.path.isdir(my_constants.IMG_PATH+ arch + '\\'+ str_dir_or_file)):#如果读到的是目录
#     #         try:
#     #             if myModels.Directories.objects.get_or_create(dir_name= str_dir_or_file, arch= arch, root_dir=arch)[1]:
#     #                 print(str_dir_or_file +"    created in table pydb_webapp_directories")
#     #             else:
#     #                 print(str_dir_or_file +"    exists in table pydb_webapp_directories")
#     #         except:
#     #             print ("myModels.Directories.objects.get_or_create() error")
#     #     elif 'json' in str_dir_or_file:
#     #         list_json.append(str_dir_or_file)
#     #         print(list_json)
#     print("the arch is :", arch)                      #arch=建筑名
#     list_iterator=[]                  #一个可以动态生长的迭代器list[[dir_name,parent_dir_name,path],...]
#     str_parent_dir=arch                                       #开始的父目录名，即arch
#     str_parent_path= my_constants.IMG_PATH                                      #初始的父目录标记为测绘图片所在总路径
#     # while len(get_subdirs_and_files(str_parent_path + str_parent_dir)[0])!=0:         #只要下一级还有子目录
#     #     list_tmp1=get_subdirs_and_files(my_constants.IMG_PATH+ str_parent_dir)        #获取子目录和文件二维列表
#     #     for str_sub_dir in list_tmp1[0]:                                           #list_tmp1[0]存放的是子目录列表
#     #         directories_get_or_create(str_sub_dir,arch,str_parent_dir)
#     list_tmp1 = get_subdirs_and_files(str_parent_path + str_parent_dir)#先获得“建筑名”下面的一级目录，没有则终止
#     for str_tmp1 in list_tmp1:
#         list_tmp2=[str_tmp1,str_parent_dir,str_parent_path +str_parent_dir] #按[dir_name,parent_dir_name,path]格式
#         list_iterator.append(list_tmp2)
#
#     list_tmp3 = iter(list_iterator).__next__()              #获得迭代列表的第一个元素
#     while len(list_tmp3)==3 :                               #此元素如果正确，应该有[dir_name,parent_dir_name,path]结构
#         directories_get_or_create(list_tmp3[0], arch , list_tmp3[1])    #结构正确，则入库
#         list_tmp4= get_subdirs_and_files(list_tmp3[2]+'\\'+list_tmp3[0]) #构建下一级目录，动态生长
#         if len(list_tmp4[0])>0 :                            #如果存在下一级目录
#             for str_tmp2 in list_tmp4[0]:
#                 list_iterator.append([str_tmp2,list_tmp3[0],list_tmp3[2]+'\\'+list_tmp3[0]])#将下一级目录添加到迭代器后面
#         list_tmp3 = iter(list_iterator).__next__()          #进行迭代
#
#
#

#=========================================================================================
# def directories_get_or_create(dir_name1, arch_name1, root_dir1):
#     """给定三个参数，实现对directories表的入库，查询是否已经存在，不存在则新增一条记录到表格中"""
#     try:
#         if myModels.Directories.objects.get_or_create(dir_name= dir_name1, arch= arch_name1, root_dir=root_dir1)[1]:
#             print(dir_name1 +"    created in table pydb_webapp_directories")
#         else:
#             print(dir_name1 +"    exists in table pydb_webapp_directories")
#     except:
#         print ("myModels.Directories.objects.get_or_create() error")

#=========================================================================================
def create_directories(str_arch,list_walk_item): #list_walk_record['path',[subdirs],[files]]
    #eg: ('d:\\myWork\\DataSource\\崔氏宗祠', ['中厅', '后座', '头门', '平立剖'], ['崔氏宗祠.json'])
    print("create_directories")
    str_path=str(list_walk_item[0])
    int_index=str_path.rfind('\\')
    str_roo_dir=str_path[int_index +1:]
    for str_dir in list_walk_item[1]:#此处如果有子目录重名，会引起无法入库。这里指的是在一个建筑中。str_arch范围内
        try:
            if myModels.Directories.objects.get_or_create(dir_name= str_dir, arch= str_arch, root_dir=str_roo_dir)[1]:
                print(str_dir +"    created in table pydb_webapp_directories")
            else:
                print(str_dir +"    exists in table pydb_webapp_directories")
        except:
            print ("myModels.Directories.objects.get_or_create() error:" +str_dir)


#=========================================================================================
def create_imgfiles(str_arch, filename, dic_of_jpg):
    """根据属于建筑arch的名为filename的这个JPG文件的json文件信息，来进行此文件的入库。"""
    try:
        if myModels.Imgfiles.objects.get_or_create(file_name= filename,arch= str_arch, defaults={'outer':dic_of_jpg['outer'],'site':dic_of_jpg['site'],
                                                                                          'location':dic_of_jpg['location'],'content':dic_of_jpg['content'],
                                                                                          'nmch_type':dic_of_jpg['nmch_type'],'description':dic_of_jpg['description'],
                                                                                          'drawing_num':dic_of_jpg['测绘图原稿图号']})[1]:
            print(filename + "      created in table pydb_webapp_imgfiles")
        else:
            print(filename + "      exists in table pydb_webapp_imgfiles")
    except:
        print("myModels.Imgfiles.objects.get_or_create() error :"+ filename)



#=========================================================================================
# def get_subdirs_and_files(str_dir):
#     """用来获取一个目录下的所有子目录和文件，分别放在两个list中，再将二者组合成一个二维列表list[ subdir_list[], files_list[] ] """
#     #这里的参数str_dir = 全路径名，eg: my_constants.IMG_PATH + subdirs
#     #返回一个二维列表
#     list_subdirs=[]
#     list_files=[]
#     list_subdirs_and_files=[]
#     list_str=os.listdir(str_dir)
#     for str_1 in list_str:
#         if os.path.isdir(str_dir + '\\' + str_1):
#             list_subdirs.append(str_1)
#         elif os.path.isfile(str_dir+ '\\'+str_1 ):
#             list_files.append(str_1)
#     list_subdirs_and_files.append(list_subdirs)
#     list_subdirs_and_files.append(list_files)
#     return list_subdirs_and_files


#==========================================================================================
#try:
db_add_main()
#except:
#    print("call db_add_main error!")


