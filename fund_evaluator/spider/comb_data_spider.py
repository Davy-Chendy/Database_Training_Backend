import requests
import json

# import urllib.request
# import json
import requests
from comb_data.models import CombData
from django.http import HttpResponse
import datetime

def getAchieve(subAccountNo):
    url = 'https://tradeapilvs6.1234567.com.cn/User/SubA/SubAGradingIndexDetailV2'
    head_info = {
        'igggggnoreburst': 'true',
        'Referer': 'https://mpservice.com/a461099f332046f0b32783c5d3d980a8/release/pages/index/index?SubAccountNo='+subAccountNo,
        'gtoken': 'ceaf-fb866d2ed4b7addd2b98075f4fd9a432',
        'clientInfo': 'ttjj-CDY-AN00-Android-10',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '306',
        'Host': 'tradeapilvs6.1234567.com.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.13'
    }
    post_param_data = {
        'appVersion': '6.5.5',
        'product': 'EFund',
        'ServerVersion': '6.5.5',
        'Passportid': None,
        'SubAccountNo': subAccountNo,
        'CustomerNo': None,
        'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'version': '6.5.5',
        'PhoneType': 'Android10',
        'MobileKey': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'UserId': None,
        'UToken': None,
        'plat': 'Android',
        'CToken': None,
        'customerNo': None
    }
    response = requests.post(url=url,headers=head_info,data=post_param_data)
    # print(response.content.decode('utf-8'))
    result = response.json()['Data']

    dict1 = {} # 近1月、近3月、近6月和近1年的最大回撤、夏普比率、波动率、收益回撤比
    for SubIntervalIndex in result['SubIntervalIndexList']:
        dict2 = {}
        for SubIndex in SubIntervalIndex['SubIndexList']:
            if SubIndex['IndexID'] == 2:
                dict2['MaxPullback'] = SubIndex['IndexValue']
            elif SubIndex['IndexID'] == 3:
                dict2['SharpeRatio'] = SubIndex['IndexValue']
            elif SubIndex['IndexID'] == 5:
                dict2['Volatility'] = SubIndex['IndexValue']
            elif SubIndex['IndexID'] == 11:
                dict2['ReturnPullbackRatio'] = SubIndex['IndexValue']

        if SubIntervalIndex['IntervalType'] == 4:
            dict1['NearlyOneMonth'] = dict2
        elif SubIntervalIndex['IntervalType'] == 3:
            dict1['NearlyThreeMonth'] = dict2
        elif SubIntervalIndex['IntervalType'] == 2:
            dict1['NearlySixMonth'] = dict2
        elif SubIntervalIndex['IntervalType'] == 1:
            dict1['NearlyOneYear'] = dict2

    FundHoldList = [] # 组合拥有的基金列表
    # dict1 = {} # 组合拥有的基金的类型、名字、占比
    for HoldClassify in result['HoldProportion']['FundHoldInfo']['HoldClassifyList']:
        # list = []
        for FundHold in HoldClassify['FundHoldList']:
            # dict2 = {}
            # dict2['FundCode'] = FundHold['FundCode']
            # dict2['FundName'] = FundHold['FundName']
            # dict2['Proportion'] = FundHold['Proportion']
            # list.append(dict2)
            FundHoldList.append(FundHold['FundName'])

    return result['AccountExistTime'], result['AssetVol'], dict1, FundHoldList

def getPageVIP(pageNum):
    url = 'https://groupapi.1234567.com.cn/FundMCApi/FundMSubAccount/MSA20GetCommonTypeSubAccountList'
    head_info = {
        'private_cache': 'cache',
        'Referer': 'https://mpservice.com/b27411c8aba745c4bbac04ae308a83b5/release/pages/index',
        'igggggnoreburst': 'true',
        'Cache-Control': 'no-cache',
        'gtoken': 'ceaf-fb866d2ed4b7addd2b98075f4fd9a432',
        'clientInfo': 'ttjj-CDY-AN00-Android-10',
        'Host': 'groupapi.1234567.com.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.13'
    }
    get_param_data = {
        'pageCount': 20,
        'condition': 'ACCSTY%3AS1%2CVIP%3A1',
        'product': 'EFund',
        'appVersion': '6.5.5',
        'plat': 'Iphone',
        'orderField': 'MPINGFEN%3Adesc',
        'deviceid': '1234567890',
        'pageNum': pageNum,
        'version': '6.5.5'
    }
    response = requests.get(url=url,headers=head_info,params=get_param_data)

    # print(response.content.decode('utf-8'))
    result = response.json()['Data']['result']
    list = []
    if result != None:
        for subAccount in result:
            AccountExistTime, AssetVol, SubIntervalIndexDict,FundHoldList = getAchieve(subAccount['subAccountNo'])
            if AccountExistTime >= 3*365:
                dict = {}
                dict['subAccountNo'] = subAccount['subAccountNo']
                dict['subAccountName'] = subAccount['subAccountName']
                dict['nicheng'] = subAccount['nicheng']
                dict['passportID'] = subAccount['passportID']
                dict['AccountExistTime'] = AccountExistTime
                dict['AssetVol'] = AssetVol
                dict['SubIntervalIndexDict'] = SubIntervalIndexDict
                dict['compose'] = FundHoldList
                list.append(dict)
                print(dict['subAccountName'])
    # print(list)

    return list

def getAllVIP():
    list = []
    for pageNum in range(1,21):
        pageList = getPageVIP(pageNum)
        list.extend(pageList)

    return list

def getFansCount(passportID):
    url = 'http://gbapi.eastmoney.com/userinfo/api/user/UserInfo'
    head_info = {
        'igggggnoreburst': 'true',
        'Referer': 'https://mpservice.com/d450a3216d9349cf8a3c5c5ccde5901c/release/pages/personalHome/profileHomePage?passportid='+passportID,
        'gtoken': 'ceaf-fb866d2ed4b7addd2b98075f4fd9a432',
        'clientInfo': 'ttjj-CDY-AN00-Android-10',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '175',
        'Host': 'gbapi.eastmoney.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.13',
    }
    post_param_data = {
        'ctoken': None,
        'product': 'Fund',
        'followuid': passportID,
        'utoken': None,
        'plat': 'Android',
        'userid': None,
        'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'version': '6.5.5',
        'passportid': None,
        'username': None
    }
    response = requests.post(url=url, headers=head_info, data=post_param_data)
    # print(response.content.decode('utf-8'))
    result = response.json()

    return result['user_fans_count']

def getHistory(subAccountNo):
    url = 'https://tradeapilvs6.1234567.com.cn/User/SubA/SubAProfit'
    head_info = {
        'igggggnoreburst': 'true',
        'Referer': 'https://mpservice.com/a461099f332046f0b32783c5d3d980a8/release/pages/historyNetValue/index?cid='+subAccountNo,
        'gtoken': 'ceaf-fb866d2ed4b7addd2b98075f4fd9a432',
        'clientInfo': 'ttjj-CDY-AN00-Android-10',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '355',
        'Host': 'tradeapilvs6.1234567.com.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.13'
    }
    post_param_data = {
        'appVersion': '6.5.5',
        'product': 'EFund',
        'ServerVersion': '6.5.5',
        'IntervalType': '9',
        'Passportid': None,
        'SubAccountNo': subAccountNo,
        'CustomerNo': None,
        'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'version': '6.5.5',
        'PhoneType': 'Android10',
        'SubCustomerNo': subAccountNo,
        'MobileKey': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'UserId': None,
        'DataType': '1',
        'UToken': None,
        'plat': 'Android',
        'CToken': None,
        'customerNo': None
    }
    response = requests.post(url=url, headers=head_info, data=post_param_data)
    # print(response.content.decode('utf-8'))
    result = response.json()['Data']
    list = []

    for GraphSpot in result['GraphSpotList']:
        dict = {}
        dict['NavDate'] = int(GraphSpot['AccountNav']['NavDate'][6:19])
        dict['Rate'] = GraphSpot['AccountNav']['Rate']
        list.append(dict)

    return list

def spider(request):
    list = getAllVIP()
    for subAccount in list:
        subAccount['user_fans_count'] = getFansCount(subAccount['passportID'])
        subAccount['GraphSpotList'] = getHistory(subAccount['subAccountNo'])
    # print(list)

    result = {}
    result['info'] = list
    #print(list)

    for data in list:
        GraphSpotList ={}
        GraphSpotList['rise']=data['GraphSpotList']

        saveData = CombData()
        saveData.subAccountNo = data['subAccountNo']
        saveData.name = data['subAccountName']
        saveData.nickname = data['nicheng']
        saveData.passportID = data['passportID']
        saveData.AccountExistTime = data['AccountExistTime']
        saveData.AssetVol = data['AssetVol']

        # 处理drawdown
        drawdown = []
        drawdown.append(data['SubIntervalIndexDict']['NearlyOneMonth']['MaxPullback'])
        drawdown.append(data['SubIntervalIndexDict']['NearlyThreeMonth']['MaxPullback'])
        drawdown.append(data['SubIntervalIndexDict']['NearlySixMonth']['MaxPullback'])
        drawdown.append(data['SubIntervalIndexDict']['NearlyOneYear']['MaxPullback'])
        MaxPullback = {}
        MaxPullback['drawdown'] = drawdown
        saveData.drawdown = MaxPullback

        # 处理sharpeRatio
        sharpeRatio = []
        sharpeRatio.append(data['SubIntervalIndexDict']['NearlyOneMonth']['SharpeRatio'])
        sharpeRatio.append(data['SubIntervalIndexDict']['NearlyThreeMonth']['SharpeRatio'])
        sharpeRatio.append(data['SubIntervalIndexDict']['NearlySixMonth']['SharpeRatio'])
        sharpeRatio.append(data['SubIntervalIndexDict']['NearlyOneYear']['SharpeRatio'])
        SharpeRatio = {}
        SharpeRatio['sharpeRatio'] = sharpeRatio
        saveData.sharpeRatio = SharpeRatio

        # 处理volatility
        volatility = []
        volatility.append(data['SubIntervalIndexDict']['NearlyOneMonth']['Volatility'])
        volatility.append(data['SubIntervalIndexDict']['NearlyThreeMonth']['Volatility'])
        volatility.append(data['SubIntervalIndexDict']['NearlySixMonth']['Volatility'])
        volatility.append(data['SubIntervalIndexDict']['NearlyOneYear']['Volatility'])
        Volatility = {}
        Volatility['volatility'] = volatility
        saveData.volatility = Volatility

        # 处理earnDrawdownRatio
        earnDrawdownRatio = []
        earnDrawdownRatio.append(data['SubIntervalIndexDict']['NearlyOneMonth']['ReturnPullbackRatio'])
        earnDrawdownRatio.append(data['SubIntervalIndexDict']['NearlyThreeMonth']['ReturnPullbackRatio'])
        earnDrawdownRatio.append(data['SubIntervalIndexDict']['NearlySixMonth']['ReturnPullbackRatio'])
        earnDrawdownRatio.append(data['SubIntervalIndexDict']['NearlyOneYear']['ReturnPullbackRatio'])
        ReturnPullbackRatio = {}
        ReturnPullbackRatio['earnDrawdownRatio'] = earnDrawdownRatio
        saveData.earnDrawdownRatio = ReturnPullbackRatio

        Compose = {}
        Compose['compose'] = data['compose']
        saveData.compose = Compose

        saveData.user_fans_count = data['user_fans_count']
        saveData.rise = GraphSpotList
        saveData.save()

    return HttpResponse("<p>爬虫爬取成功！</p>")


        #打印rise
        #print(GraphSpotList)
        # drawdown = []
        # drawdown.append(data['SubIntervalIndexDict']['NearlyOneMonth']['MaxPullback'])
        # drawdown.append(data['SubIntervalIndexDict']['NearlyThreeMonth']['MaxPullback'])
        # drawdown.append(data['SubIntervalIndexDict']['NearlySixMonth']['MaxPullback'])
        # drawdown.append(data['SubIntervalIndexDict']['NearlyOneYear']['MaxPullback'])
        # print(drawdown)

    # with open('info.json','w') as f:
    #     json.dump(result, f)