import urllib.request
import json
import requests
from comb_data.models import CombData
from django.http import HttpResponse
import datetime

def db_delete(request):
    # 删除所有数据
    CombData.objects.all().delete()
    return HttpResponse("<p>数据删除成功！</p>")
