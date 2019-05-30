from SpyderTool.Tool.BaiduTraffic import BaiduTraffic
from SpyderTool.Tool.GaodeTraffic import GaodeTraffic
from SpyderTool.setting import *
import pymysql
import time

class TraffciFunction(object):

    def RoadManager(self,cityCode):
        mysql = pymysql.connect(host=host, user=user, password=password, database="trafficdatabase",
                                port=port)

        t= time.localtime()
        date =time.strftime("%Y-%m-%d",t)
        DetailTime=time.strftime("%H:%M",t)
        g = GaodeTraffic(mysql)
        result=g.RoadData(cityCode)
        for item in result:

            sql = "insert into  roadtraffic(pid_id,date,detailTime,name,direction,speed,data,bounds,flag) values('%d','%s','%s','%s','%s','%f','%s','%s',%s);" % (
                cityCode, date, DetailTime, item['RoadName'],item['Direction'],item['Speed'],item['Data'],item['Bounds'],True)

            self.LoadDatabase(mysql,sql)

    def LoadDatabase(self,mysql,sql):

        cursor = mysql.cursor()
        try:
            cursor.execute(sql)
            mysql.commit()
        except Exception as e:

            print("error:%s" % e)
            mysql.rollback()
            return False
        return True
