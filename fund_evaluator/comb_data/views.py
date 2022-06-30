from django.http import JsonResponse
from comb_data.models import CombData


def trans_data(s):
    for i in range(0, 4):
        s[i] = float(s[i])
    return s


def trans_data2(s):
    for i in range(0,4):
        s[i] = s[i][0:len(s[i])-1]
        s[i] = float(s[i])
    return s


def comb_data_list(request):
    res = CombData.objects.values('name')
    res = list(res)
    data = {"result": res}

    return JsonResponse(data, safe=False)


def comb_data_detail(request,name):
    res = CombData.objects.filter(name=name).values()
    res = list(res)
    index = 0
    for data in res:
        res[index]['drawdown'] = trans_data2(data['drawdown']['drawdown'])
        # res[index]['sharpeRatio'] = data['sharpeRatio']['sharpeRatio']
        res[index]['sharpeRatio'] = trans_data(data['sharpeRatio']['sharpeRatio'])
        res[index]['volatility'] = trans_data2(data['volatility']['volatility'])
        res[index]['earnDrawdownRatio'] = trans_data(data['earnDrawdownRatio']['earnDrawdownRatio'])
        res[index]['rise'] = data['rise']['rise']
        num = 0
        for date in res[index]['rise']:
            # print(date)
            # print(res[index]['rise'][num]['data'])
            res[index]['rise'][num]['data'] = date['data'][6:19]
            num = num+1
        res[index]['compose'] = data['compose']['compose']
        res[index]['level'] = float(data['level'])
        index = index + 1
    # print(res)
    data = {"result": res}

    return JsonResponse(data, safe=False)
