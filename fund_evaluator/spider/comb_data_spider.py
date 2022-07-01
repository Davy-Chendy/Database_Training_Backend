import requests
import json
import urllib
# import urllib.request
import json
import requests
from comb_data.models import CombData
from django.http import HttpResponse
import datetime
import time



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
        'appVersion': '6.5.6',
        'product': 'EFund',
        'ServerVersion': '6.5.6',
        'Passportid': None,
        'SubAccountNo': subAccountNo,
        'CustomerNo': None,
        'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'version': '6.5.6',
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
        'condition': 'ACCSTY%3AS1',
        'product': 'EFund',
        'appVersion': '6.5.6',
        'plat': 'Iphone',
        'orderField': 'MPINGFEN%3Adesc',
        'deviceid': '1234567890',
        'pageNum': pageNum,
        'version': '6.5.6'
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

def getAllVIP(num):
    list = []
    pageNum = num

    # # 看所有的页
    # while True:
    #     pageList = getPageVIP(pageNum)
    #     if len(pageList) != 0:
    #         list.extend(pageList)
    #         pageNum = pageNum + 1
    #     else:
    #         break

    # 只看一页
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
        'version': '6.5.6',
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
        'appVersion': '6.5.6',
        'product': 'EFund',
        'ServerVersion': '6.5.6',
        'IntervalType': '9',
        'Passportid': None,
        'SubAccountNo': subAccountNo,
        'CustomerNo': None,
        'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'version': '6.5.6',
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
    result = response.json()['Data']
    list = []
    list2 = []

    for GraphSpot in result['GraphSpotList']:
        dict = {}
        dict['data'] = GraphSpot['AccountNav']['NavDate']
        dict['value'] = GraphSpot['AccountNav']['Rate']
        list.append(dict)

        dict2 = {}
        timeArray = time.localtime(int(GraphSpot['AccountNav']['NavDate'][6:16]))
        datestr = time.strftime('%Y-%m-%d', timeArray)
        dict2['date'] = datestr
        dict2['Nav'] = GraphSpot['AccountNav']['Nav']
        list2.append(dict2)

    return list, list2

def getPageWarehouseAdjustment(subAccountNo, name, TimePoint, Content_Length):
    url = 'https://jijinbaapi.eastmoney.com/FundMCApi/FundMBNew/FZH15DynamicPostList2'
    head_info = {
        'igggggnoreburst': 'true',
        'Referer': 'https://mpservice.com/a461099f332046f0b32783c5d3d980a8/release/pages/wareHouse/index?id='+subAccountNo+'&name='+urllib.parse.quote(name)+'&subType=0&isSelf=false',
        'gtoken': 'ceaf-fb866d2ed4b7addd2b98075f4fd9a432',
        'clientInfo': 'ttjj-CDY-AN00-Android-10',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Content_Length,
        'Host': 'jijinbaapi.eastmoney.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.13'
    }
    post_param_data = {
        'appVersion': '6.5.6',
        'product': 'EFund',
        'ServerVersion': '6.5.6',
        'TimePoint': TimePoint,
        'Passportid': None,
        'pageSize': 21,
        'CustomerNo': None,
        'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'version': '6.5.6',
        'ZHCode' : subAccountNo,
        'PhoneType': 'Android10',
        'MobileKey': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
        'UserId': None,
        'ApiType': 4,
        'UToken': None,
        'plat': 'Android',
        'CToken': None,
        'customerNo': None
    }
    response = requests.post(url=url, headers=head_info, data=post_param_data)
    # print(response.content.decode('utf-8'))
    result = response.json()['Data']
    list = [] # 卖出
    list2 = [] # 买入
    i = 0
    TimePointStr = '0'
    if result != None:
        for warehouseAdjustmentRecode in result:
            if warehouseAdjustmentRecode['warehouseRecord']['BusinName'] == '卖出':
                dict = {}
                dict['dateTime'] = warehouseAdjustmentRecode['dateTime']
                dict['FundCode'] = warehouseAdjustmentRecode['warehouseRecord']['FundCode']
                dict['FundName'] = warehouseAdjustmentRecode['warehouseRecord']['FundName']
                list.append(dict)
            elif warehouseAdjustmentRecode['warehouseRecord']['BusinName'] == '买入':
                dict = {}
                dict['dateTime'] = warehouseAdjustmentRecode['dateTime']
                dict['FundCode'] = warehouseAdjustmentRecode['warehouseRecord']['FundCode']
                dict['FundName'] = warehouseAdjustmentRecode['warehouseRecord']['FundName']
                list2.append(dict)
            i = i+1
            if i == 20:
                TimePointStr = warehouseAdjustmentRecode['timePointStr']

    return list, list2, TimePointStr, i

def getAllWarehouseAdjustment(subAccountNo, name):
    list = [] # 卖出
    list2 = [] # 买入
    FundDict = {} # 基金字典
    TimePoint = '0'
    pageList, pageList2, TimePointStr, i = getPageWarehouseAdjustment(subAccountNo, name, TimePoint, str(334))
    TimePoint = TimePointStr
    list.extend(pageList)
    list2.extend(pageList2)
    while i == 21:
        pageList, pageList2, TimePointStr, i = getPageWarehouseAdjustment(subAccountNo, name, TimePoint, str(352))
        TimePoint = TimePointStr
        list.extend(pageList)
        list2.extend(pageList2)

    for PurchaseRecord in list2[::-1]:
        if PurchaseRecord['FundCode'] not in FundDict:
            date = datetime.datetime.strptime(PurchaseRecord['dateTime'], '%Y年%m月%d日')
            FundDict[PurchaseRecord['FundCode']] = {}
            FundDict[PurchaseRecord['FundCode']]['PurchaseTime'] = date
    for SalesRecord in list[::-1]:
        if SalesRecord['FundCode'] in FundDict:
            date = datetime.datetime.strptime(SalesRecord['dateTime'], '%Y年%m月%d日')
            FundDict[SalesRecord['FundCode']]['SalesTime'] = date

    sum = datetime.datetime.now() - datetime.datetime.now() # 持有天数总和
    count = 0 # 参与持有天数计算计算的基金数量
    for key, values in FundDict.items():
        count = count + 1
        if 'SalesTime' in values:
            sum = sum + (values['SalesTime'] - values['PurchaseTime'])
        else:
            sum = sum + (datetime.datetime.now() - values['PurchaseTime'])
    if count == 0:
        average = 0
    else:
        average = (sum / count).days # 平均持有天数

    return list, average

def getFundHistory(fundCode, fundName, date):
    pageIndex = 1
    finish = 0
    list = []
    while True:
        if pageIndex <= 10:
            contentLength = '334'
        else:
            contentLength = '335'

        url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNHisNetList'
        head_info = {
            'igggggnoreburst': 'true',
            'Referer': 'https://mpservice.com/516939c37bdb4ba2b1138c50cf69a2e1/release/pages/fundHistoryWorth/index?fundCode='+fundCode+'&fundName='+urllib.parse.quote(fundName),
            'gtoken': 'ceaf-fb866d2ed4b7addd2b98075f4fd9a432',
            'clientInfo': 'ttjj-CDY-AN00-Android-10',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': contentLength,
            'Host': 'fundmobapi.eastmoney.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.13',
        }
        post_param_data = {
            'product': 'EFund',
            'appVersion': '6.5.6',
            'serverVersion': '6.5.6',
            'pageSize': 20,
            'FCODE': fundCode,
            'version': '6.5.6',
            'deviceid': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
            'userId': 'uid',
            'cToken': 'ctoken',
            'MobileKey': 'ff5d271dfa24a769bf5c3c6180447d86%7C%7Ciemi_tluafed_me',
            'pageIndex': pageIndex,
            'appType': 'ttjj',
            'OSVersion': 10,
            'plat': 'Android',
            'IsShareNet': 'true',
            'passportid': None,
            'uToken': 'utoken'
        }
        response = requests.post(url=url, headers=head_info, data=post_param_data)
        result = response.json()['Datas']

        pageIndex = pageIndex + 1

        if len(result) != 0:
            for GraphSpot in result:
                if len(list) == 0:
                    list.append(GraphSpot['DWJZ'])
                FSRQ = datetime.datetime.strptime(GraphSpot['FSRQ'], '%Y-%m-%d')
                if FSRQ > date:
                    continue
                elif FSRQ == date:
                    list.append(GraphSpot['DWJZ'])
                    finish = finish + 1
                    break
                elif FSRQ < date:
                    finish = finish + 1
                    break
            if finish > 0:
                break
        else:
            break

    return list


def spider(request):
    # 第17页开始没爬
    num = int(1)
    while(num<=16):
        list = getAllVIP(num)
        for subAccount in list:
            subAccount['user_fans_count'] = getFansCount(subAccount['passportID'])
            subAccount['GraphSpotList'],rise = getHistory(subAccount['subAccountNo'])
            subAccount['warehouseRecord'] = getAllWarehouseAdjustment(subAccount['subAccountNo'],subAccount['subAccountName'])
            warehouseRecordList, subAccount['average_holding_days'] = getAllWarehouseAdjustment(subAccount['subAccountNo'], subAccount['subAccountName'])
            warehouseAdjustmentSuccess = 0
            warehouseAdjustmentTotal = 0
            for warehouseRecord in warehouseRecordList:
                date = datetime.datetime.strptime(warehouseRecord['dateTime'], '%Y年%m月%d日')
                datestr = date.strftime('%Y-%m-%d')
                warehouseRecordData = getFundHistory(warehouseRecord['FundCode'], warehouseRecord['FundName'], date)
                if len(warehouseRecordData) == 2:
                    for dict in rise:
                        if datestr == dict['date']:
                            warehouseAdjustmentTotal = warehouseAdjustmentTotal + 1
                            if (float(rise[-1]['Nav']) - float(dict['Nav'])) / float(dict['Nav']) - (
                                    float(warehouseRecordData[0]) - float(warehouseRecordData[1])) / float(
                                    warehouseRecordData[1]) > 0:
                                warehouseAdjustmentSuccess = warehouseAdjustmentSuccess + 1
                            break
            if warehouseAdjustmentTotal == 0:
                subAccount['level'] = 0
            else:
                subAccount['level'] = warehouseAdjustmentSuccess / warehouseAdjustmentTotal
            print('爬完某个组合的所有数据')
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
            saveData.level  = data['level']
            saveData.average_holding_days = data['average_holding_days']

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

        print('爬完第'+str(num)+'页')
        num = num+1

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