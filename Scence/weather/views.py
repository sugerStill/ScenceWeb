from django.shortcuts import render


# Create your views here.

def firstpage(request):
    """
    天气首页
    :param request:
    :return:
    """
    pass


# 将省份里的所有城市页面返回
def citys(request, pid):
    """
    省份下所有城市
    :param request:
    :param pid:
    :return:
    """
    pass


def history_detail(request, pid):
    """

    :param request:
    :param pid:
    :return:
    """
    pass


def weathermonthhistory(request, pid: int, date: str):
    pass
