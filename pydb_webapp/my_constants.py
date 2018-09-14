#=============================================================================
#        这个文件定义项目中用到的一些常量
#=============================================================================
# global MAX_NAME_LENGTH = 60
MAX_NAME_LENGTH = 60
MAX_SIMPLE_LENGTH = 10
MAX_DESCRIPTION_LENGTH =255

IMG_PATH=u"c:\\myWork\\DataSource\\"
#DB_NAME = u'd:\\myWork\\PycharmProjects\\Dj1\\db.sqlite3'


class myClass():
    """Just a test class"""
    def __init__(self, name):
        self.name = name
        print("you have got it ,myClass")

    def func2(self):
        print("myClass.func2()")

