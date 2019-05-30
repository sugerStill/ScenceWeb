# import requests, json
# import sys,csv
# href = 'https://xingyun.map.qq.com/api/getXingyunPoints'
# post = {}
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
#
# }
#
# post['count'] = 5
# f = open("/Users/darkmoon/PycharmProjects/DataViewWeb/SpyderTool/learn.csv","a+")
# w = csv.writer(f)
# for i in range(1):
#     post['rank'] = i
#     result = requests.post(url=href, headers=headers, data=json.dumps(post))
#     g = json.loads(result.text)
#     for item in g['locs'].split(','):
#         pass
#
#
#
