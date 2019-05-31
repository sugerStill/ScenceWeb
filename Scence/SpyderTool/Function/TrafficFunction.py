from SpyderTool.Tool.BaiduTraffic import BaiduTraffic
from SpyderTool.Tool.GaodeTraffic import GaodeTraffic
from SpyderTool.setting import *
import time, csv,pymysql
from SpyderTool.setting import CityFilePath,Trafficdatabase

class TraffciFunction(object):
    
    def initDatabase(self):

        mysql = pymysql.connect(host=host, user=user, password=password, database=Trafficdatabase,
                                port=port)
        mysql.connect()
        cursor=mysql.cursor()
        with open('/Users/darkmoon/ScenceWeb/Scence/SpyderTool/DataFiles/CityInformation.csv', 'r') as f:

            read = csv.reader(f)
            read.__next__()
            for item in read:
                Name=item[0]
                Lat=float(item[1])
                Lon=float(item[2])
                CityCode=int(item[3])
                YearPid=int(item[4])
                sql="insert into MainTrafficInfo(name,cityCode,bounds_lat,bounds_lon,yearPid) values ('%s','%d','%f','%f','%d')"%(Name,CityCode,Lat,Lon,YearPid)

                try:
                    cursor.execute(sql)
                    mysql.commit()
                except Exception as e:
                    print("error:%s"%e)
                    mysql.rollback()
                    break
        cursor.close()
        mysql.close()
        return  True



        return True

    def RoadManager(self, cityCode):
        mysql = pymysql.connect(host=host, user=user, password=password, database=Trafficdatabase,
                                port=port)
        t = time.localtime()
        date = time.strftime("%Y-%m-%d", t)
        DetailTime = time.strftime("%H:%M", t)
        g = GaodeTraffic(mysql)
        result = g.RoadData(cityCode)
        for item in result:
            sql = "insert into  roadtraffic(pid_id,date,detailTime,name,direction,speed,data,bounds,flag) values('%d','%s','%s','%s','%s','%f','%s','%s',%s);" % (
                cityCode, date, DetailTime, item['RoadName'], item['Direction'], item['Speed'], item['Data'],
                item['Bounds'], True)

            self.LoadDatabase(mysql, sql)

    def LoadDatabase(self, mysql, sql):

        cursor = mysql.cursor()
        try:
            cursor.execute(sql)
            mysql.commit()
        except Exception as e:

            print("error:%s" % e)
            mysql.rollback()
            return False
        return True


TraffciFunction().initDatabase()
