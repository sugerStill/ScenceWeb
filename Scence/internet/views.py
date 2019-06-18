from django.shortcuts import render


# Create your views here.
def get_mobile_brand_rate(request, startyear, startmonth, endyear, endmonth, brand):
    """
    返回手机品牌某段时间的历史占有率
    :param request:
    :param startyear: 开始年份
    :param startmonth: 开始月份
    :param endyear: 结束年份
    :param endmonth: 结束月份
    :param brand: 品牌名
    :return:list[{'date':,"value":x%}]
        """

    pass


def get_mobile_type_rate(request, startyear, startmonth, endyear, endmonth, brand, mobiletype):
    """
    返回品牌某手机机型某段时间历史占有率
    :param startyear: 开始年份
    :param startmonth: 开始月份
    :param endyear: 结束年份
    :param endmonth: 结束月份
    :param brand:品牌名
    :param mobiletype:手机机型
    :return:list[{'date':,"value":x%}]
    """
    pass


def get_mobile_resolution_rate(request, startyear, startmonth, endyear, endmonth):
    """
    返回手机分辨率占有率历史数据
    :param request:
    :param startyear: 开始年份
    :param startmonth: 开始月份
    :param endyear: 结束年份
    :param endmonth: 结束月份
    :return:list[{'date':,"value":x%}]
    """
    pass


def get_mobile_system_rate(request, startyear, startmonth, endyear, endmonth):
    """
    返回手机系统占有率历史数据
    :param request:
    :param startyear: 开始年份
    :param startmonth: 开始月份
    :param endyear: 结束年份
    :param endmonth: 结束月份
    :return:list[{'date':,"value":x%}]
    """
    pass


def get_mobile_operator_rate(request, startyear, startmonth, endyear, endmonth):
    """
    返回手机运营商占有率历史数据
    :param request:
    :param startyear: 开始年份
    :param startmonth: 开始月份
    :param endyear: 结束年份
    :param endmonth: 结束月份
    :return:list[{'date':,"value":x%}]"""

    pass


def get_mobile_network_rate(request, startyear, startmonth, endyear, endmonth):
    """
    返回手机网络占有率历史数据
    :param request:
    :param startyear: 开始年份
    :param startmonth: 开始月份
    :param endyear: 结束年份
    :param endmonth: 结束月份
    :return:list[{'date':,"value":x%}]"""
    pass


def get_wechat_public(request, account):
    """
    根据用户输入的公众号名称和微信号返回相似账号
    :param request:
    :param account:
    :return:
    """
    pass


def get_wetchat_public_read(request, account):
    """
    获取公众号信息，如公众号名字，账号，平均阅读量，最高阅读量，平均点赞，最高点赞，历史数据":[{"日期": , "总阅读数":
    , "总点赞数": , "发表文章数"}]
    :param request:
    :param account:账号名
    :return:{"situation":{"average_read": 头条平均阅读量, "hight_read": 最高阅读量, "average_like": 头条平均点赞数,
                               "hight_like":最高点赞数 },"data":历史数据（一个月的数据量）->
                               [{"day":日期 , "read_num_total":总阅读数 ,
                                "top_like_num_total":总点赞数 , "articles_total":发表文章数
                }]}
    """
    pass


def get_wechat_public_keyword(request, account):
    """
    获取公众号关键词列表
    :param account ：公众号
    :return list[{"keyword":公众号关键词,"value": 热度}]
    """
    pass


def get_keyword_search_index(request, keyword):
    """
    获取浏览器的关键词搜索频率，最长一个月数据
    :param request:
    :param keyword: 关键词
    :return: [{"baidu_update": 百度最新统计时间, "baidu_pc":PC端搜索量 , "baidu_mobile":移动端搜索量 , "baidu_all":整体搜索量 },
                   {"haosou_update":360最新统计时间 , "haosou_pc":PC端搜索量 , "haosou_mobile":移动端 搜索量,
                    "haosou_all":整体搜索量 }，
                   {"sougou_update":搜狗最新统计时间 , "sougou_pc":PC端搜索量 , "sougou_mobile":移动端搜索量 ,
                    "sougou_all": 整体}]
    """
    pass


def get_alibaba_keyword_buy_index(request, keyword):
    """

    获取淘宝，1688商品的搜索频率，返回一年数据
    :param request:
    :param keyword: 关键词
    :return: {"pur1688":1688采购数量  , "taobao":淘宝采购数量 ,
                "supply1688": 1688供应数量 , "lastdate":最近时间 ,
                "olddate": 最远时间}
    """
    pass


def get_user_portrait(request, year, month):
    """
    获取用户图像---性别分布 ，年龄分布，消费偏好，区域热度，应用偏好,年限需要注意

    :param request:
    :param year:
    :param month:
    :return:待定
    """
    pass


def custom_user_portrait(request, startyear, startmonth, endyear, endmonth, key):
    """
       定制服务---获取用户图像---性别分布 ，年龄分布，消费偏好，区域热度，应用偏好,年限需要注意

       :param request:
       :param startyear:开始年限
       :param startmonth:开始月份
       :param endyear:结束年限
       :param endmonth:结束月份
       :param key:用户key
       :return:待定
       """
    pass


def get_user_behavior(request, year, month):
    """
    获取用户行为---人均安装应用趋势，人均启动应用趋势

        :param year:年份
        :param month:结束月份---》截止至month前6个月的数据
        :rtype: list
        :return list[{"date": 日期, "install": 人均安装应用, "active":人均启动应用 }]

    """
    pass


def custom_user_behavior(request, startyear, startmonth, endyear, endmonth, key):
    """
        定制服务---获取用户行为---人均安装应用趋势，人均启动应用趋势

       :param request:
       :param startyear:开始年限
       :param startmonth:开始月份
       :param endyear:结束年限
       :param endmonth:结束月份
       :param key:用户key

    :return: list[{"date": 日期, "install": 人均安装应用, "active":人均启动应用 }]
    """
    pass


def get_app_importance_info(request, appname):
    """
    获取app的核心数据
    :param request:
    :param appname:
    :return: 待定
    """
    pass


def get_app_active(request, appname):
    """
    获取app的用户画像数据
    :return:待定
    """
    pass
