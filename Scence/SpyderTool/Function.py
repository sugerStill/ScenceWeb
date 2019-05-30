from SpyderTool.PeopleFlow import ScencePeopleFlow
from SpyderTool.Weather import Weather
from SpyderTool.Traffic import BaiduTraffic, GaodeTraffic
import pymysql, time, csv
from concurrent.futures import ThreadPoolExecutor
from SpyderTool.setting import *
class DataBaseInit:
    # 待更改为信号量来实现多线程操作数据库
    instance = None
    db = pymysql.connect(host=host, user=user, password=password, database=database,
                         port=port)

    # 录入数据库景区数据库信息
    def __test_LoadIntoDatabase(self):

        cursor = self.db.cursor()
        with open(Filepath, 'r') as f:
            reader = csv.reader(f)
            reader.__next__()  # 跳过表头
            count = 0
            for item in reader:
                count += 1
                name = str(item[0]).strip(' ')
                PeoplePid = int(item[1])
                bounds_lon = float(item[2])
                bounds_lat = float(item[3])
                CityCode = int(item[4])
                WeatherPid = str(item[5]).strip(" ")
                PeopleTablePid = count
                CityTableCode = count
                WeatherTablePid = count

                sql = "insert into ScenceInfoData(name,bounds_lon,bounds_lat,PeoplePid,CityCode,WeatherPid,PeopleTablePid,CityTableCode,WeatherTablePid) values ('%s','%f','%f','%d','%d','%s','%d','%d','%d')" % (
                    name, bounds_lon, bounds_lat, PeoplePid, CityCode, WeatherPid, PeopleTablePid, CityTableCode,
                    WeatherTablePid)
                try:
                    cursor.execute(sql)
                    self.db.commit()
                    print("success")
                except Exception as e:
                    print("error:%s" % e)
                    self.db.rollback()
        self.db.close()


    @classmethod
    def PeopleFlow(cls, PeoplePidList):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.__ProgrammerPool(cls.instance.GetPeopleFlow, PeoplePidList)
            time.sleep(1800)
    def GetPeopleFlow(self, PeoplePid):

        mysql = pymysql.connect(host=host, user=user, password=password, database=database,
                         port=port)
        sql = "select PeopleTablePid from ScenceInfoData where  PeoplePid=" + str(PeoplePid) + ";"

        cursor = self.GetCursor(mysql, sql)
        if cursor is None:
            return
        PeopleTablePid = cursor.fetchone()[0]
        cursor.close()
        date = time.strftime('%Y-%m-%d', time.localtime())
        flow = ScencePeopleFlow(PeoplePid, mysql)
        info = flow.PeopleFlowInfo

        info = self.__DealWithPeopleFlow(mysql, info, date, PeopleTablePid)
        for detailTime, num in info:
            try:
                flow.LoadDatabase(PeopleTablePid, date, num, detailTime)
            except Exception as e:
                print("error---%s" % e)
        print("success")
        mysql.close()

    # 检查数据库是否存在部分数据，存在则不再插入
    def __DealWithPeopleFlow(self, mysql, info, date, PeopleTablePid):

        sql = "select detailTime from peopleFlow where  pid_id=" + str(
            PeopleTablePid) + " and  date=str_to_date('" + str(date) + "','%Y-%m-%d');"
        cursor = self.GetCursor(mysql, sql)
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
    def Weather(cls, WeatherPidList):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.__ProgrammerPool(cls.instance.GetWeather, WeatherPidList)
            time.sleep(4*3600)
    def GetWeather(self, WeatherPid):
        mysql = pymysql.connect(host=host, user=user, password=password, database=database,
                         port=port)
        sql = "select WeatherTablePid from ScenceInfoData where  WeatherPid=" + "'" + WeatherPid + "';"

        cursor = self.GetCursor(mysql, sql)
        if cursor is None:
            return
        WeatherTablePid = cursor.fetchone()[0]
        cursor.close()
        weather = Weather(mysql)
        info = weather.WeatherForcest(WeatherPid)
        # 每次爬取都是获取未来7天的数据，所以再次爬取时只需要以此刻为起点，看看数据库存不存在7天后的数据
        date = time.strftime('%Y-%m-%d', time.localtime(
            time.time() + 7 * 3600 * 24))

        info = self.__DealWithWeather(info, mysql, WeatherTablePid, date)

        for item in info:
            date = item['date']
            detailTime = item['detailTime']
            state = item['state']
            temperature = item['temperature']
            wind = item['wind']
            weather.LoadDatabase(WeatherTablePid, date, detailTime, state, temperature, wind)
        mysql.close()
        print("success")

    '''天气数据去已️存在数据'''

    def __DealWithWeather(self, info, mysql, Pid, date):

        sql = "select  date,detailTime from weather where pid_id=" + str(
            Pid) + " and date =str_to_date('" + date + "','%Y-%m-%d');"
        cursor = self.GetCursor(mysql, sql)
        if cursor is None:
            cursor.close()
            return info
        data = cursor.fetchall()

        if len(data)==0:
            cursor.close()
            return info
        lis = []

        for item in info:
            if item['date'] != date:
                continue
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        for Olddata in data:
            self.__filter(info, Olddata[0], Olddata[1])
        lis = []
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        return info

    @classmethod
    def Traffic(cls, CityCodeList):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.__ProgrammerPool(cls.instance.GetTraffic, CityCodeList)
            time.sleep(350)
    def GetTraffic(self, CityCode):
        mysql = pymysql.connect(host=host, user=user, password=password, database=database,
                         port=port)

        sql = "select CityTableCode from ScenceInfoData where  CityCode=" + "'" + str(CityCode) + "';"

        cursor = self.GetCursor(mysql, sql)
        if cursor is None:
            print("cursor is None")
            return
        CityTableCode = cursor.fetchone()[0]
        cursor.close()
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

        info = self.__DealWithTraffic(info, mysql, CityTableCode, today, yesterday)
        if info is None:
            print("Null")
            return None

        for item in info:
            date = item['date']
            index = float(item['index'])
            detailTime = item['detailTime']
            traffic.LoadDatabase(CityTableCode, date, index, detailTime)

        print("success")
        mysql.close()

    def __DealWithTraffic(self, info, mysql, Pid, today, yesterday):

        lis = []
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        # 将昨天的数据全部剔除
        for i in range(len(info)):
            if info[i].get(yesterday) is None:
                info = info[i + 1:]
                break

        sql = "select  date,detailTime from traffic where pid_id=" + str(
            Pid) + " and date =str_to_date('" + today + "','%Y-%m-%d');"
        cursor = self.GetCursor(mysql, sql)
        if cursor is None:
            return
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

    # 处理返回执行smysql返回cursor
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

    def __ProgrammerPool(self, func, PidList):
        l = []

        threadPool = ThreadPoolExecutor(max_workers=6)

        for Pid in PidList:
            task = threadPool.submit(func, Pid)
            l.append(task)
        while [item.done() for item in l].count(False):
            pass

    '''过滤器'''

    def __filter(self, info, date, detailTime):
        for i in range(len(info)):
            if info[i].get(str(date)) and info[i].get(detailTime):
                info.pop(i)
                return
