from abc import ABC, abstractmethod
from urllib.parse import urlencode
import json, requests


class Traffic(ABC):

    @abstractmethod
    def CityTraffic(self, cityCode):
        pass

    # 道路数据获取
    @abstractmethod
    def RoadData(self, cityCode):
        pass

    @abstractmethod
    def YearTraffic(self, cityCode, year,quarter):
        pass
    #经纬度查询
    def getLngLat(self, City):
        # https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%20%E5%8C%97%E4%BA%AC
        pre_url = 'https://apis.map.qq.com/jsapi?'
        req = {
            "newmap": 1,
            "qt": 'poi',
            "wd": City
        }
        headers = {'Host': 'apis.map.qq.com',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        url = pre_url + urlencode(req)
        data = requests.get(url=url, headers=headers)
        g = json.loads(data.text)
        bounds = g['detail']['city']
        lon = bounds['pointx']
        lat = bounds['pointy']
        return {"lat": lat, "lon": lon}
