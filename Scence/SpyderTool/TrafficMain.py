import pymysql
from SpyderTool.Function.TrafficFunction import TraffciFunction
from SpyderTool.setting import host, user, password, trafficdatabase, port

if __name__ == "__main__":
    traffic = TraffciFunction()
    db = pymysql.connect(host=host, user=user, password=password, database=trafficdatabase,
                         port=port)
    db.connect()
    cursor = db.cursor()
    sql = "select CityCode from trafficdatabase.MainTrafficInfo;"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
    result = cursor.fetchall()
    for item in result:
        citycode = item[0]
        # traffic.gettraffic(citycode)
        # traffic.yeartraffic(citycode)
        traffic.road_manager(citycode)
