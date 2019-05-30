import requests
import json
import re, time, importlib

from urllib.parse import urlencode


class Info(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
        }
        self.s = requests.Session()

    def intoBase(self, name, id, pid):
        parameter = {
            'qt': 'poi',
            'wd': name,
            'pn': 0,
            'rn': '10',
            'rich_source': 'qipao',
            'rich': 'web',
            'nj': 0,
            'c': 1,
            'key': 'FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS',
            'output': 'jsonp',
            'pf': 'jsapi',
            'ref': 'jsapi'
        }
        href = "https://apis.map.qq.com/jsapi?" + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)

        data = re.sub('(.*?)\(', '', data.text, count=1)[:-1]
        obj = json.loads(data)

        # 先附近景点数据：名字，地址，卫星数据
        l = []

        [l.append([pois['name'], pois['addr'], pois['pointx'], pois['pointy']]) for pois in obj['detail']['pois']]
        for item in l:
            s = ScencePOS()
            s.name = item[0]
            s.pid = pid
            s.addr = item[1]
            s.bounds_lon = item[2]
            s.bounds_lat = item[3]
            s.link_id = id
            s.save()

    # 搜索才地区是哪个城市
    def get(self, name):
        parameter = {
            'qt': 'poi',
            'wd': name,
            'pn': 0,
            'rn': '10',
            'rich_source': 'qipao',
            'rich': 'web',
            'nj': 0,
            'c': 1,
            'key': 'FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS',
            'output': 'jsonp',
            'pf': 'jsapi',
            'ref': 'jsapi'
        }
        href = "https://apis.map.qq.com/jsapi?" + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)

        data = re.sub('(.*?)\(', '', data.text, count=1)[:-1]
        obj = json.loads(data)
        city = obj['detail']['city']['path'][0]["cname"]
        print(name, city)
    def searchLocation(self,name,pid):
        parameter = {
            'qt': 'poi',
            'wd': name,
            'pn': 0,
            'rn': '10',
            'rich_source': 'qipao',
            'rich': 'web',
            'nj': 0,
            'c': 1,
            'key': 'FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS',
            'output': 'jsonp',
            'pf': 'jsapi',
            'ref': 'jsapi'
        }
        href = "https://apis.map.qq.com/jsapi?" + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)

        data = re.sub('(.*?)\(', '', data.text, count=1)[:-1]
        obj = json.loads(data)
        l = []
        item = obj['detail']['area']
        l.append(item['cname'])
        l.append(pid)
        l.append(item['pointx'])
        l.append(item['pointy'])
        return l
