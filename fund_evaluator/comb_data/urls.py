from django.urls import path
from . import views
from spider import comb_data_spider
from spider import db_func

app_name = 'comb_data'

urlpatterns = [
    path('', views.comb_data_list, name='list'),
    path('comb_data_spider/',comb_data_spider.spider,name='spider'),
    path('delete/',db_func.db_delete,name='delete'),
]
