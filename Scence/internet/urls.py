from django.urls import path
from internet import views

urlpatterns = [
    path("brand/<slug:brand>/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>",
         views.get_mobile_brand_rate),
    path("brand/<slug:brand>/<slug:mobiletype>/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>",
         views.get_mobile_type_rate),
    path("resolution/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>", views.get_mobile_resolution_rate),
    path("system/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>", views.get_mobile_system_rate),

    path("operator/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>", views.get_mobile_operator_rate),
    path("network/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>", views.get_mobile_network_rate),
    path("wechat/<slug:accout>", views.get_wechat_public),
    path("wetchat/read/<slug:accout>", views.get_wetchat_public_read),
    path("wechat/public_keyword/<slug:accout>", views.get_wechat_public_keyword),
    path("keyword/search/<slug:keyword>", views.get_keyword_search_index),
    path("goods/keyword/<slug:keyword>", views.get_alibaba_keyword_buy_index),
    path("user/portrait/<int:year>-<int:month>", views.get_user_portrait),

    path("custom/user?portrait/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>/<slug:key>",
         views.custom_user_portrait),
    path("user/behavior/<int:year>-<int:month>", views.get_user_behavior),
    path("custom/user?behavior/<int:startyear>-<int:startmonth>-<int:endyear>-<int:endmonth>/<slug:key>",
         views.custom_user_behavior),
    path("app/app=<slug:appname>/info", views.get_app_importance_info),
    path("app/app=<slug:appname>/acitve", views.get_app_active)
]
