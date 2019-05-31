import pymysql
import time
import csv
from SpyderTool.Tool.PeopleFlow import ScencePeopleFlow
from SpyderTool.Tool.Weather import Weather
from SpyderTool.Tool.BaiduTraffic import BaiduTraffic
from SpyderTool.Tool.GaodeTraffic import GaodeTraffic

from concurrent.futures import ThreadPoolExecutor
from SpyderTool.setting import *


class ScenceFunction:
    # 待更改为信号量来实现多线程操作数据库
    instance = None
    db = pymysql.connect(host=host, user=user, password=password, database=scencedatabase,
                         port=port)

    # 录入数据库景区数据库信息
    @staticmethod
    def initdatabase():
        mysql = pymysql.connect(host=host, user=user, password=password, database=scencedatabase,
                                port=port)
        mysql.connect()
        cursor = mysql.cursor()
        with open(scencefilepath, 'r') as f:
            reader = csv.reader(f)
            reader.__next__()  # 跳过表头
            count = 0
            for item in reader:
                count += 1
                name = str(item[0]).strip(' ')
                peoplepid = int(item[1])
                bounds_lon = float(item[2])
                bounds_lat = float(item[3])
                citycode = int(item[4])
                weatherpid = str(item[5]).strip(" ")
                peopletablepid = count
                citytablecode = count
                weathertablepid = count

                sql = "insert into webdata.ScenceInfoData(name,bounds_lon,bounds_lat,PeoplePid,CityCode,WeatherPid," \
                      "PeopleTablePid,CityTableCode,WeatherTablePid)" \
                      " values ('%s','%f','%f','%d','%d','%s','%d','%d','%d')" % (
                          name, bounds_lon, bounds_lat, peoplepid, citycode, weatherpid, peopletablepid, citytablecode,
                          weathertablepid)
                try:
                    cursor.execute(sql)
                    mysql.commit()
                except Exception as e:
                    print("error:%s" % e)
                    mysql.rollback()
        cursor.close()
        mysql.close()
        return True

    @classmethod
    def people_flow(cls, peoplepidlist):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.programmerpool(cls.instance.getpeopleflow, peoplepidlist)
            time.sleep(1800)

    def getpeopleflow(self, peoplepid):

        mysql = pymysql.connect(host=host, user=user, password=password, database=scencedatabase,
                                port=port)
        sql = "select PeopleTablePid from webdata.ScenceInfoData where  PeoplePid=" + \
              str(peoplepid) + ";"

        cursor = self.get_cursor(mysql, sql)
        if cursor is None:
            return
        peopletablepid = cursor.fetchone()[0]
        cursor.close()
        date = time.strftime('%Y-%m-%d', time.localtime())
        flow = ScencePeopleFlow(peoplepid, mysql)
        info = flow.peopleflow_info

        info = self.__dealwith_peopleflow(mysql, info, date, peopletablepid)
        for detailTime, num in info:
            sql = "insert into peopleFlow(pid_id,date,num,detailTime) values ('%d','%s','%d','%s');" % (
                peopletablepid, date, num, detailTime)
            if not self.loaddatabase(mysql, sql):
                print("插入出错")
                continue
        print("success")
        mysql.close()

    # 检查数据库是否存在部分数据，存在则不再插入
    def __dealwith_peopleflow(self, mysql, info, date, peopletablepid):

        sql = "select detailTime from webdata.peopleFlow where  pid_id=" + str(
            peopletablepid) + " and  date=str_to_date('" + str(date) + "','%Y-%m-%d');"
        cursor = self.get_cursor(mysql, sql)
        if cursor is None:
            return
        data = cursor.fetchall()
        cursor.close()
        dic = {}
        for detailTime, num in info:
            dic[detailTime] = num
        for item in data:
            try:
                dic.pop(item[0])
            except KeyError:
                continue
        for detailTime, num in dic.items():
            yield detailTime, num

    @classmethod
    def weather(cls, weatherpidlist):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.programmerpool(cls.instance.getweather, weatherpidlist)
            time.sleep(4 * 3600)

    def getweather(self, weatherpid):
        mysql = pymysql.connect(host=host, user=user, password=password, database=scencedatabase,
                                port=port)
        sql = "select WeatherTablePid from webdata.ScenceInfoData where  WeatherPid=" \
              + "'" + weatherpid + "';"

        cursor = self.get_cursor(mysql, sql)
        if cursor is None:
            return
        weathertablepid = cursor.fetchone()[0]
        cursor.close()
        weather = Weather(mysql)
        info = weather.weatherforcest(weatherpid)

        # 每次爬取都是获取未来7天的数据，所以再次爬取时只需要以此刻为起点，看看数据库存不存在7天后的数据
        date = time.strftime('%Y-%m-%d', time.localtime(
            time.time() + 7 * 3600 * 24))

        info = self.__dealwith_weather(info, mysql, weathertablepid, date)
        for item in info:
            date = item['date']
            detailtime = item['detailTime']
            state = item['state']
            temperature = item['temperature']
            wind = item['wind']
            sql = "insert into  webdata.weather(pid_id,date,detailTime,state,temperature,wind) " \
                  "values('%d','%s','%s','%s','%s','%s');" % (
                      weathertablepid, date, detailtime, state, temperature, wind)
            if not self.loaddatabase(mysql, sql):
                print("插入失败！")
                continue

        mysql.close()
        print("success")

    '''天气数据去已️存在数据'''

    def __dealwith_weather(self, info, mysql, pid, date):

        sql = "select  date,detailTime from webdata.weather where pid_id=" + str(
            pid) + " and date =str_to_date('" + date + "','%Y-%m-%d');"
        cursor = self.get_cursor(mysql, sql)
        if cursor is None:
            cursor.close()
            return info
        data = cursor.fetchall()

        if len(data) == 0:
            cursor.close()
            return info
        lis = []

        for item in info:
            if item['date'] != date:
                continue
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        for olddata in data:
            self.filter(info, olddata[0], olddata[1])
        lis = []
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        return info

    @classmethod
    def traffic(cls, citycodelist):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.programmerpool(cls.instance.gettraffic, citycodelist)
            time.sleep(350)

    def gettraffic(self, citycode):
        mysql = pymysql.connect(host=host, user=user, password=password, database=scencedatabase,
                                port=port)

        sql = "select CityTableCode from webdata.ScenceInfoData where  CityCode=" + "'" + str(citycode) + "';"

        cursor = self.get_cursor(mysql, sql)
        if cursor is None:
            print("cursor is None")
            return
        citytablecode = cursor.fetchone()[0]
        cursor.close()

        if citycode > 1000:
            traffic = GaodeTraffic(mysql)

        elif 0 < citycode < 1000:
            traffic = BaiduTraffic(mysql)

        else:
            return
        t = time.time()

        today = time.strftime('%Y-%m-%d', time.localtime(t))
        yesterday = time.strftime('%Y-%m-%d', time.localtime(t - 3600 * 24))
        info = traffic.citytraffic(citycode)

        info = self.__dealwith_traffic(info, mysql, citytablecode, today, yesterday)
        if info is None:
            print("Null")
            return None

        for item in info:
            date = item['date']
            index = float(item['index'])
            detailtime = item['detailTime']
            sql = "insert into  webdata.traffic(pid_id,date,TrafficIndex,detailTime) " \
                  "values('%d','%s','%s','%s');" % (
                      citytablecode, date, index, detailtime)
            self.loaddatabase(mysql, sql)

        print("success")
        mysql.close()

    # 写入数据库
    @staticmethod
    def loaddatabase(mysql, sql):
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

    def __dealwith_traffic(self, info, mysql, pid, today, yesterday):

        lis = []
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        # 将昨天的数据全部剔除
        for i in range(len(info)):
            if info[i].get(yesterday) is None:
                info = info[i + 1:]
                break

        sql = "select  date,detailTime from webdata.traffic where pid_id=" + str(
            pid) + " and date =str_to_date('" + today + "','%Y-%m-%d');"
        cursor = self.get_cursor(mysql, sql)
        if cursor is None:
            return
        data = cursor.fetchall()
        cursor.close()
        # 剔除今天重复的数据
        for item in data:
            self.filter(info, item[0], item[1])
        lis.clear()
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        return info

    # 处理返回执行smysql返回cursor
    @staticmethod
    def get_cursor(mysql, sql):

        cursor = mysql.cursor()
        try:
            cursor.execute(sql)
            mysql.commit()
        except Exception as e:
            print("查询错误%s" % e)
            mysql.rollback()
            cursor.close()
            return None
        return cursor

    @staticmethod
    def programmerpool(func, pidlist):
        tasklist = []

        threadpool = ThreadPoolExecutor(max_workers=6)

        for pid in pidlist:
            task = threadpool.submit(func, pid)
            tasklist.append(task)
        while [item.done() for item in tasklist].count(False):
            pass

    '''过滤器'''

    @staticmethod
    def filter(info, date, detailtime):
        for i in range(len(info)):
            if info[i].get(str(date)) and info[i].get(detailtime):
                info.pop(i)
                return
