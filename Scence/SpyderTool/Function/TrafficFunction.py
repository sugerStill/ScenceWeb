from SpyderTool.Tool.BaiduTraffic import BaiduTraffic
from SpyderTool.Tool.GaodeTraffic import GaodeTraffic
from SpyderTool.setting import *
import time, csv, pymysql
from SpyderTool.setting import CityFilePath, Trafficdatabase
from concurrent.futures import ThreadPoolExecutor


class TraffciFunction(object):

    def __initDatabase(self):

        mysql = pymysql.connect(host=host, user=user, password=password, database=Trafficdatabase,
                                port=port)
        mysql.connect()
        cursor = mysql.cursor()
        with open(CityFilePath, 'r') as f:

            read = csv.reader(f)
            read.__next__()
            for item in read:
                Name = item[0]
                Lat = float(item[1])
                Lon = float(item[2])
                CityCode = int(item[3])
                YearPid = int(item[4])
                sql = "insert into MainTrafficInfo(name,cityCode,bounds_lat,bounds_lon,yearPid) values ('%s','%d','%f','%f','%d')" % (
                    Name, CityCode, Lat, Lon, YearPid)

                try:
                    cursor.execute(sql)
                    mysql.commit()
                except Exception as e:
                    print("error:%s" % e)
                    cursor.close()
                    mysql.rollback()
                    break
        cursor.close()
        mysql.close()
        return True
    @classmethod

    def DailyCityTraffic(cls,CityCodeList):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.__ProgrammerPool(cls.instance.GetTraffic, CityCodeList)

    def GetTraffic(self, CityCode):
        mysql = pymysql.connect(host=host, user=user, password=password, database=Trafficdatabase,
                         port=port)


        traffic = None

        if CityCode > 1000:
            traffic = GaodeTraffic(mysql)

        elif CityCode > 0 and CityCode < 1000:

            traffic = BaiduTraffic(mysql)
        else:
            return
        t = time.time()
        today = time.strftime('%Y-%m-%d', time.localtime(t))
        yesterday = time.strftime('%Y-%m-%d', time.localtime(t - 3600 * 24))
        info = traffic.CityTraffic(CityCode)

        info = self.__DealWithTraffic(info, CityCode,mysql, today, yesterday)
        if info is None:
            print("Null")
            return None

        for item in info:
            date = item['date']
            index = float(item['index'])
            detailTime = item['detailTime']
            sql = "insert into  CityTraffic(pid_id,date,TrafficIndex,detailTime) values('%d','%s','%s','%s');" % (
                CityCode, date, index, detailTime)
            if not self.LoadDatabase(mysql,sql):
                print("%s插入失败"%item)

        print("success")

        mysql.close()
    def __DealWithTraffic(self, info, mysql,Pid ,today, yesterday):

        lis = []
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        # 将昨天的数据全部剔除
        for i in range(len(info)):
            if info[i].get(yesterday) is None:
                info = info[i + 1:]
                break

        sql = "select  date,detailTime from CityTraffic where pid_id=" + str(
            Pid) + " and date =str_to_date('" + today + "','%Y-%m-%d');"
        cursor = self.GetCursor(mysql, sql)
        if cursor is None:
            return None
        data = cursor.fetchall()
        cursor.close()
        # 剔除今天重复的数据
        for item in data:
            self.__filter(info, item[0], item[1])
        lis.clear()
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        return info

    def RoadManager(self, cityCode):
        mysql = pymysql.connect(host=host, user=user, password=password, database=Trafficdatabase,
                                port=port)
        t = time.localtime()
        date = time.strftime("%Y-%m-%d", t)
        DetailTime = time.strftime("%H:%M", t)
        g = None
        if cityCode > 1000:
            g = GaodeTraffic(mysql)
        elif cityCode < 1000:
            g = BaiduTraffic(mysql)
        result = g.RoadData(cityCode)
        for item in result:
            sql = "insert into  roadtraffic(pid_id,date,detailTime,name,direction,speed,data,bounds,flag) values('%d','%s','%s','%s','%s','%f','%s','%s',%s);" % (
                cityCode, date, DetailTime, item['RoadName'], item['Direction'], item['Speed'], item['Data'],
                item['Bounds'], True)

            if not self.LoadDatabase(mysql, sql):
                print("%s写入数据库失败" % item)
                continue

    def YearTraffic(self, cityCode):
        mysql = pymysql.connect(host=host, user=user, password=password, database=Trafficdatabase,
                                port=port)
        g = None
        if cityCode > 1000:
            g = GaodeTraffic(mysql)
        elif cityCode < 1000:
            g = BaiduTraffic(mysql)
        result = g.YearTraffic(cityCode)
        for item in result:
            date = item['date']
            index = item['index']
            city = item['city']
            sql = "insert into  yearcitytraffic(pid_id,date,name,index) values('%d','%s','%s','%f');" % (
                cityCode, date, city, index)
            if not self.LoadDatabase(mysql, sql):
                print("%s写入数据库失败" % item)
                continue


    def LoadDatabase(self, mysql, sql):

        cursor = mysql.cursor()
        try:
            cursor.execute(sql)
            mysql.commit()
            cursor.close()
        except Exception as e:

            print("error:%s" % e)
            mysql.rollback()
            cursor.close()
            return False
        return True
    def __ProgrammerPool(self, func, PidList):
        l = []

        threadPool = ThreadPoolExecutor(max_workers=6)

        for Pid in PidList:
            task = threadPool.submit(func, Pid)
            l.append(task)
        while [item.done() for item in l].count(False):
            pass
    def GetCursor(self, mysql, sql):

        cursor = mysql.cursor()
        try:
            cursor.execute(sql)
            mysql.commit()
        except Exception as e:
            print("查询错误%s" % e)
            mysql.rollback()
            return None
        return cursor
    def __filter(self, info, date, detailTime):
        for i in range(len(info)):
            if info[i].get(str(date)) and info[i].get(detailTime):
                info.pop(i)
                return

TraffciFunction().YearTraffic(120)
