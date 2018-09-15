import os
import sys
from pydb_webapp import my_constants
from pydb_webapp import models as myModels
import json

from Dj1 import settings
#BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#STATICFILES_DIRS1=os.path.join(BASE_DIR1, 'static')
# coding: utf-8

#========================================以下为数据库操作部分==================================================

#==========================================================================================
def db_add_main():  #the main function to add data to db
    print("add data to db")
    list_archs = []
    dic_json_files = {}  # 字典 list_json{"崔氏宗祠":"崔氏宗祠.json"},...}
    list_walk_results = []
    contents_of_json = {}
    dic_of_jpg ={}
    list_walk_arch_ret =[]
    dic_walk_to_json = {}
    list_dirs_files_item=[]
    list_list_dirs_files=[]

    list_archs=create_archs()
    print(list_archs)
    for str_arch in list_archs :
        list_tmp = os.listdir(my_constants.IMG_PATH+ str_arch)
        #===============================模块一，用于读取 “建筑群.json”文件======================================
        if (str_arch +'.json') in list_tmp :                #如果存在json文件，则将此信息保存在字典list_json，并打开文件，读取信息到contents_of_json
            #list_json.append({str_arch :str_arch + '.json' })
            dic_json_files[str_arch]=str_arch +'.json'
            with open(my_constants.IMG_PATH + str_arch + '\\'+ dic_json_files[str_arch], 'r') as f_json_obj:
                contents_of_json=json.load(f_json_obj)
                print(my_constants.IMG_PATH + str_arch + '\\'+ dic_json_files[str_arch] +'  opened! ')

        else:
            print("no "+ str_arch+'.json  file in '+ str_arch)
        #================================模块一结束，walk记录迭代开始===================================================================
        list_walk_results = os.walk(my_constants.IMG_PATH + str_arch)
        list_walk_record1 = list_walk_results.__next__()
        try:
            while list_walk_record1[0] != '' or list_walk_record1[1].__len__() > 0 or list_walk_record1[2].__len__() > 0: #这里只要还有记录，len应该恒等于3
                #==================将walk结果迭代数据集的一条数据进行处理，以便把目录结构信息保存成json文件=================
                str_path1 = str(list_walk_record1[0])
                int_index = str_path1.rfind('\\')
                str_root_dir = str_path1[int_index + 1:]  # 提取目录名，去掉路径信息
                #list_dirs_files_item.clear()
                list_dirs_files_item.append(str_root_dir)  # 将目录名、子目录列表、文件列表保存到list_item
                list_dirs_files_item.append(list_walk_record1[1])
                list_dirs_files_item.append(list_walk_record1[2])
                #print("list_dirs_files_item is : ", list_dirs_files_item)
                #print("list_list_dirs_files before appending is : ", list_list_dirs_files)
                #list1=[]
                #list1.extend(list_dirs_files_item) #此处不能直接用list_dirs_files_item,会导致list_list_dirs_files的之前append添加的内容都发生改变，很奇怪
                list_list_dirs_files.append(list_dirs_files_item)  # 保存每一条处理后的目录及其下子目录和文件信息，到一个列表的列表中
                list_dirs_files_item=[]               #此行比不可少，不然list_list_dirs_files已经append的内容，会随着list_dirs_files_item变化，有点奇怪

                #print("list_list_dirs_files after appending is: ", list_list_dirs_files)
                #====================================下面是入库，分析这条记录是否有目录信息，是否有文件==========================
                if list_walk_record1[1].__len__() >0: #如果存在子目录，执行将子目录信息入库
                    print("当前记录存在子目录，记录是： ", list_walk_record1)
                    #print("create subdir record: ",list_walk_record1)
                    create_directories(str_arch, list_walk_record1)
                if list_walk_record1[2].__len__() >0: #如果存在文件
                    print("当前记录存在文件，记录是： ", list_walk_record1)
                    #================================================================
                    #list_walk_record1格式['path',[subdirs],[files]]
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
                                #         "p_or_d": "测绘图",
                                #         "description": "广州市番禺区大学城崔氏宗祠的后座垂脊博古大样，由广州大学建筑与城市规划学院测绘于2018年。",
                                #         "测绘图原稿图号": ""
                                #       }
                                # str_path2 = str(list_walk_record1[0])  #这里三行可以去掉了，前面有一样的处理
                                # int_index = str_path2.rfind('\\')
                                # str_root_dir = str_path2[int_index + 1:]
                                create_imgfiles(str_arch= str_arch, root_dir1= str_root_dir ,filename= str_filename, dic_of_jpg= dic_of_jpg)
                            else:
                                print("缺乏 "+ str_filename + " 的json文件定义")
                                pass
                        else:
                            print(str_filename + "  不是jpg文件，忽略入库操作")
                            pass



                list_walk_record1 =list_walk_results.__next__()
        except StopIteration:
            print(str_arch + "  的 walk 记录遍历结束")
            pass   #迭代一个建筑结束，此处需要继续运行。用continue,后面的代码都会被忽略，返回for循环继续下一次运行
        #==============================一个建筑群遍历结束，这里对该建筑群的目录结构信息第一条记录（根目录信息进行处理）======
        #print("list_list_dirs_files 的内容是 ", list_list_dirs_files)
        if list_list_dirs_files[0][1].__len__() >0 and list_list_dirs_files[0][2].__len__() >0 :  # 这个列表的第一条记录，应该是“建筑群”的根目录，下面如果有文件列表，要清空。因为都不是测绘图和照片文件，是JSON文件，入库说明文档等
            list_list_dirs_files[0][2] = []  # 注意此处是个空列表，不能用''。将根目录的文件名从目录结构列表中剔除
        #==============================将一个建筑群的目录结构信息，写到字典dic_walk_to_json中。所有建筑群循环完毕，将dic_walk_to_json写入JSON文件========
        #print("list_list_dirs_files 的内容是 ", list_list_dirs_files)
        dic_walk_to_json[str_arch]=list_list_dirs_files
        list_list_dirs_files=[]
        #print("dic_walk_to_json 的内容是： ", dic_walk_to_json )
    #=================for循环结束，所有建筑群都已遍历=========================================
    #=================这里应该将dic_walk_to_json写到static静态目录里
    with open((settings.STATICFILES_DIRS[0] + "\\dirs_files.json"), 'w') as f_dirs_files_json:
        f_dirs_files_json.truncate()                        #以w方式打开，本来就会清空文件内容。这里再清空一次
        json.dump(dic_walk_to_json, f_dirs_files_json, ensure_ascii= False) #这里的中文是GBK格式




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
                if myModels.Archs.objects.get_or_create( arch_name=str_arch, root_dir="\\")[1]:
                    print(str_arch + "    created in table pydb_webapp_archs")
                else:
                    print(str_arch + "    exists in table pydb_webapp_archs")
            except:
                print("myModels.Archs.objects.get_or_create()  error")

    return list_dirs
#=========================================================================================
def create_directories(str_arch,list_walk_item): #list_walk_record['path',[subdirs],[files]]
    #eg: ('d:\\myWork\\DataSource\\崔氏宗祠', ['中厅', '后座', '头门', '平立剖'], ['崔氏宗祠.json'])
    print("create_directories")
    str_path=str(list_walk_item[0])
    int_index=str_path.rfind('\\')
    str_root_dir=str_path[int_index +1:]
    for str_dir in list_walk_item[1]:#此处如果有子目录重名，会引起无法入库。这里指的是在一个建筑中。str_arch范围内
        try:
            if myModels.Directories.objects.get_or_create(dir_name= str_dir, arch= str_arch, root_dir=str_root_dir)[1]:
                print(str_dir +"    created in table pydb_webapp_directories")
            else:
                print(str_dir +"    exists in table pydb_webapp_directories")
        except:
            print ("myModels.Directories.objects.get_or_create() error:" +str_dir)


#=========================================================================================
def create_imgfiles(str_arch, root_dir1, filename, dic_of_jpg):
    """根据属于建筑arch的名为filename的这个JPG文件的json文件信息，来进行此文件的入库。"""
    try:
        if myModels.Imgfiles.objects.get_or_create(file_name= filename,arch= str_arch, root_dir=root_dir1,
                                                   defaults={'outer':dic_of_jpg['outer'],'site':dic_of_jpg['site'],
                                                              'location':dic_of_jpg['location'],'content':dic_of_jpg['content'],
                                                              'nmch_type':dic_of_jpg['nmch_type'],'p_or_d':dic_of_jpg['p_or_d'],
                                                             'description':dic_of_jpg['description'],
                                                              'drawing_num':dic_of_jpg['测绘图原稿图号']})[1]:
            print(filename + "      created in table pydb_webapp_imgfiles")
        else:
            print(filename + "      exists in table pydb_webapp_imgfiles")
    except:
        print("myModels.Imgfiles.objects.get_or_create() error :"+ filename)

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


#=========================================将一个建筑群目录进行walk的列表结果进行处理，返回处理后的列表，不改变原列表===================
#===========================此函数也需要迭代一遍walk结果，和db_add_main()的迭代重复，故将处理代码改放到db_add_main()中===========
# def proc_list_walk(list_walk_iterable):
#     list_ret=[]
#     list_item=[]
#     list_walk_item = list_walk_iterable.__next__()
#     try:
#         while (list_walk_item[0]!='' or list_walk_item[1]!=''or list_walk_item[1]!=''):
#             str_path = str(list_walk_item[0])
#             int_index = str_path.rfind('\\')
#             str_root_dir = str_path[int_index + 1:]     #提取目录名，去掉路径信息
#             list_item.clear()
#             list_item.append(str_root_dir)              #将目录名、子目录列表、文件列表保存到list_item
#             list_item.append(list_walk_item[1])
#             list_item.append(list_walk_item[2])
#             list_ret.append(list_item)                  #保存每一条处理后的目录及其下子目录和文件信息，到一个列表中
#             list_walk_item = list_walk_iterable.__next__()
#     except StopIteration:
#         print("walk 记录遍历结束")
#         pass
#
#
#     if list_ret[0][1] != '' and list_ret[0][2] != '': #这个列表的第一条记录，应该是“建筑群”的根目录，下面如果有文件列表，要清空。因为都不是测绘图和照片文件，是JSON文件，入库说明文档等
#         list_ret[0][2] = []                             #注意此处是个空列表，不能用''
#
#     return list_ret                                 #是一个列表的列表[ [ 目录名1, [subdir1,subdir2,…], [filename1,filename2,…]],
#                                                                     # [ 目录名2, [subdir1,subdir2,…], [filename1,filename2,…]],
#                                                                     # ……],
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


