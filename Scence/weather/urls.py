from django.urls import path
from weather import views

urlpatterns = [
    path('', views.firstpage, name="firstpage"),  # 天气首页

    path('citys/lishi/', views.citys, name="citys"),  # 省份下所有城市

    path('citys/lishi/<int:pid>/', views.history_detail, name="historyfirstpage"),  # 天气历史数据列表
    path('citys/lishi/<int:pid>/<int:date>', views.weathermonthhistory, name="monthhistory"),  # 某月份的数据

]
