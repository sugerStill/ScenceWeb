from multiprocessing import Pool
from SpyderTool.Function.ScenceFunction import ScenceFunction
import pymysql
from SpyderTool.setting import *
if __name__ == "__main__":
    pool = Pool(processes=3)
    db = pymysql.connect(host=host, user=user, password=password, database=Scencedatabase,
                         port=port)
    db.connect()
    cursor = db.cursor()
    sql = "select PeoplePid,WeatherPid,CityCode from ScenceInfoData;"
    try:
        cursor.execute(sql)
    except Exception as e:
        print("error:%s" % e)
    d = ScenceFunction()
    PeoplePidList = []
    WeatherPidList = []
    CityCodeList = []
    for PeoplePid, WeatherPid, CityCode in cursor.fetchall():
        PeoplePidList.append(PeoplePid)
        WeatherPidList.append(WeatherPid)
        CityCodeList.append(CityCode)
    CityCodeList = list(set(CityCodeList))
    WeatherPidList = list(set(WeatherPidList))

    pool.apply_async(func=d.PeopleFlow, args=(PeoplePidList, ))
    pool.apply_async(func=d.Weather, args=(WeatherPidList,))
    pool.apply_async(func=d.Traffic, args=(CityCodeList,))
    pool.close()
    pool.join()
