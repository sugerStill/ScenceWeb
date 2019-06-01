import requests
import json
import time
from urllib.parse import urlencode
from SpyderTool.Tool.Traffic import Traffic


class BaiduTraffic(Traffic):

    def __init__(self, db):
        self.db = db
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36'

        }
        # 获取实时城市交通情况

    # def deco(func):
    #     def Load(self, cityCode):
    #         data = func(self, cityCode)
    #         return data
    #
    #     return Load
    #
    # @deco
    def citytraffic(self, citycode, timetype='minute'):

        parameter = {
            'cityCode': citycode,
            'type': timetype  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        try:
            g = json.loads(data.text)
        except Exception as e:
            print("网络链接error:%s" % e)
            return None
        today = time.strftime("%Y-%m-%d", time.localtime())  # 今天的日期
        date = today
        if '00:00' in str(g):
            date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))  # 昨天的日期
        # 含有24小时的数据
        dic = {}
        for item in g['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '13:45'}
            if item["time"] == '00:00':
                date = today
            dic['date'] = date
            dic['index'] = float(item['index'])
            dic['detailTime'] = item['time']
            yield dic

    def yeartraffic(self, citycode: int, year: int = int(time.strftime("%Y", time.localtime())),
                    quarter: int = int(time.strftime("%m", time.localtime())) / 3):

        sql = "select   name from trafficdatabase.MainTrafficInfo where cityCode=" \
              + str(citycode) + ";"
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
            print("百度交通信息数据库查不到相关信息")
            return None
        parameter = {
            'cityCode': citycode,
            'type': 'day'  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        try:
            obj = json.loads(data.text)
        except Exception as e:
            print("百度年度交通爬取失败！:%s" % e)
            return None
        if not len(obj):
            return None
        year = time.strftime("%Y-", time.localtime())  #

        for item in obj['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '04-12'}
            date = year + item['time']
            index = float(item["index"])
            yield {"date": date, "index": index, "city": city}

    def roaddata(self, citycode):
        dic = self.__roads(citycode)
        if dic['status'] == 1:
            print("参数不合法")
            return None
        datalist = self.__realtime_road(dic, citycode)

        for item, data in zip(dic['data']['list'], datalist):
            roadname = item["roadname"]
            speed = float(item["speed"])
            direction = item['semantic']
            bounds = json.dumps({"coords": data['coords']})
            info = json.dumps(data['data'])

            yield {"RoadName": roadname, "Speed": speed, "Direction": direction, "Bounds": bounds, 'Data': info}

    def __roads(self, citycode):
        parameter = {
            'cityCode': citycode,
            'roadtype': 0
        }
        href = ' https://jiaotong.baidu.com/trafficindex/city/roadrank?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        dic = json.loads(data.text)
        return dic

    def __realtime_road(self, dic, citycode):

        for item, i in zip(dic['data']['list'], range(1, 11)):
            data = self.__realtime_roaddata(item['roadsegid'], i, citycode)
            yield data

    # 道路请求
    def __realtime_roaddata(self, pid, i, citycode):
        parameter = {
            'cityCode': citycode,
            'id': pid
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/roadcurve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        obj = json.loads(data.text)
        timelist = []
        data = []
        for item in obj['data']['curve']:  # 交通数据
            timelist.append(item['datatime'])
            data.append(item['congestIndex'])
        realdata = {"num": i, "time": timelist, "data": data}
        bounds = []
        for item in obj['data']['location']:  # 卫星数据
            bound = {}
            for locations, count in zip(item.split(","), range(0, item.split(",").__len__())):
                if count % 2 != 0:

                    bound['lat'] = locations
                else:
                    bound['lon'] = locations
            bounds.append(bound)
        return {"data": realdata, "coords": bounds}
