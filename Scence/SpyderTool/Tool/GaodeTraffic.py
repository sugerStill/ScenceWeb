import requests
import json
import time
from urllib.parse import urlencode
from SpyderTool.MulThread import MulitThread
from SpyderTool.Tool.Traffic import Traffic


class GaodeTraffic(Traffic):

    def __init__(self, db):
        self.db = db
        self.s = requests.Session()
        self.headers = {
            'Host': 'report.amap.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36'

        }

    # def deco(func):
    #     def load(self, cityCode):
    #         data = func(self, cityCode)
    #         return data
    #
    #     return load
    #
    # @deco
    def citytraffic(self, citycode):
        url = "http://report.amap.com/ajax/cityHourly.do?cityCode=" + str(citycode)
        data = self.s.get(url=url, headers=self.headers)
        try:
            g = json.loads(data.text)
        except Exception as e:
            print("编号%d--网络链接error:%s" % (citycode, e))
            print(data)

            return None
        today = time.strftime("%Y-%m-%d", time.localtime())  # 今天的日期
        date = today
        if '00:00' in str(g):
            date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))  # 昨天的日期
        # 含有24小时的数据
        dic = {}
        for item in g:
            detailtime = time.strftime("%H:%M", time.localtime(int(item[0]) / 1000))
            if detailtime == '00:00':
                date = today
            dic['date'] = date
            dic['index'] = float(item[1])
            dic['detailTime'] = detailtime
            yield dic

    # 道路数据获取
    def roaddata(self, citycode):
        dic = self.__roads(citycode)  # 道路基本信息
        if not len(dic['route']):
            print("参数不合法或者网络链接失败")
            return None

        datalist = self.__realtimeroad(dic, citycode)  # 获取数据
        if datalist is None:
            return None
        for item, data in zip(dic['route'], datalist['data']):
            roadname = item["name"]  # 路名
            speed = float(item["speed"])  # 速度
            data = json.dumps(data)  # 数据包
            direction = item['dir']  # 道路方向
            bounds = json.dumps({"coords": item['coords']})  # 道路经纬度数据

            yield {"RoadName": roadname, "Speed": speed, "Direction": direction, "Bounds": bounds, 'Data': data}

    def __roads(self, citycode):

        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": citycode
        }
        url = "https://report.amap.com/ajax/roadRank.do?" + urlencode(req)
        data = self.s.get(url=url, headers=self.headers)

        try:
            route = json.loads(data.text)  # 道路信息包
        except Exception as e:
            print(e)
            return None
        list_id = []  # 记录道路pid
        list_roadname = []  # 记录道路名
        list_dir = []  # 记录道路方向
        list_speed = []  # 记录速度
        for item in route["tableData"]:
            list_roadname.append(item["name"])  # 道路名
            list_dir.append(item["dir"])  # 方向
            list_speed.append(item["speed"])  # 速度
            list_id.append(item["id"])  # 道路pid
        dic_collections = dict()  # 存放所有数据
        dic_collections["route"] = route['tableData']
        dic_collections["listId"] = list_id
        dic_collections["listRoadName"] = list_roadname
        dic_collections["listDir"] = list_dir
        dic_collections["listSpeed"] = list_speed

        return dic_collections

    # 某条路实时路况
    def __realtimeroad(self, dic, citycode):
        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": citycode,
            'lineCode': ''

        }
        url = "https://report.amap.com/ajax/roadDetail.do?" + urlencode(req)
        threadlist = []
        data = []
        for pid, i in zip(dic["listId"],
                          range(0, (dic["listId"]).__len__())):
            roadurl = url + str(pid)
            t = MulitThread(target=self.__realtime_roaddata, args=(roadurl, i,))  # i表示排名
            t.start()
            threadlist.append(t)
        for t in threadlist:
            t.join()
            if t.get_result is not None:
                data.append(t.get_result)
            else:
                continue

        # 排好序列
        if len(data) > 0:
            sorted(data, key=lambda x: ["num"])
        else:
            return None
        return {"data": data}

    def __realtime_roaddata(self, roadurl, i):
        data = self.s.get(url=roadurl, headers=self.headers)
        try:
            g = json.loads(data.text)  # 拥堵指数
        except Exception as e:
            print(e)
            return None
        data = []  # 拥堵指数
        time_list = []  # 时间
        for item in g:
            time_list.append(time.strftime("%H:%M", time.strptime(time.ctime(int(item[0] / 1000 + 3600 * 8)))))
            data.append(item[1])
        # {排名，时间，交通数据}
        realdata = {"num": i, "time": time_list, "data": data}
        return realdata

    def yeartraffic(self, citycode: int, year: int = int(time.strftime("%Y", time.localtime())),
                    quarter: int = int(time.strftime("%m", time.localtime())) / 3):
        if quarter - int(quarter) > 0:

            quarter = int(quarter) + 1
        else:
            quarter = int(quarter)
        url = "http://report.amap.com/ajax/cityDailyQuarterly.do?"

        # year键表示哪一年 的数据
        req = {
            "cityCode": citycode,
            "year": year,  # 年份
            "quarter": quarter  # 第几季
        }
        sql = "select   name from trafficdatabase.MainTrafficInfo where yearPid=" + str(citycode) + ";"
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()

        except Exception as e:
            print("百度模块数据库执行出错:%s" % e)
            self.db.rollback()
            cursor.close()
            return None

        try:
            city = cursor.fetchone()[0]
        except TypeError:
            print("高德交通信息数据库查不到相关信息")
            return None
        url = url + urlencode(req)
        data = requests.get(url=url, headers=self.headers)
        try:
            g = eval(data.text)
        except SyntaxError:
            print("高德地图年度数据请求失败！")
            return None
        for date, index in zip(g["categories"], g['serieData']):
            yield {"date": date, "index": index, "city": city}  # {'date': '2019-01-01', 'index': 1.25, 'city': city}
