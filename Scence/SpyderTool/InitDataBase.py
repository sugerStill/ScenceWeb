from SpyderTool.Function.ScenceFunction import ScenceFunction
import pymysql
from SpyderTool.setting import *
'''初始化数据库'''
if __name__ == "__main__":

    db = pymysql.connect(host=host, user=user, password=password, database=database,
                         port=port)
    db.connect()
    d = ScenceFunction()
    d._ScenceFunction__test_LoadIntoDatabase()
