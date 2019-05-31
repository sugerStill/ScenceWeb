from SpyderTool.Function.ScenceFunction import ScenceFunction
import pymysql
from SpyderTool.setting import *
from SpyderTool.Function.TrafficFunction import TraffciFunction
def initScenceDatabase():

    d = ScenceFunction()
    d._ScenceFunction__initDatabase()
def initTraffivDatabase():
    t = TraffciFunction()
    t._TraffciFunction__initdatabase()

'''初始化数据库'''
if __name__ == "__main__":
    print("请输入操作选项：1.初始化景区数据库  2.初始化交通数据库")
    state = input()
    if state==1:
        initScenceDatabase()
    if state==2:
        initTraffivDatabase()
    else:
        print("输入有误！")


