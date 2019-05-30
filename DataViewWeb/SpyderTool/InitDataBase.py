from SpyderTool.Function import DataBaseInit
import pymysql
from SpyderTool.setting import *
'''初始化数据库'''
if __name__ == "__main__":

    db = pymysql.connect(host=host, user=user, password=password, database=database,
                         port=port)
    db.connect()
    d = DataBaseInit()
    d._DataBaseInit__test_LoadIntoDatabase()
