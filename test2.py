# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re

'''
从网页http://www.mafengwo.cn/jd/34639/gonglve.html处获取吉首景点列表和poiID
参考：https://blog.csdn.net/qq_28053189/article/details/79538978

'''


#
def get_param():
    '''
    获取所有景点的参数
    :return: 从网页http://www.mafengwo.cn/jd/34639/gonglve.html处获取吉首景点列表和poiID
    '''

    total = []
    router_url = 'http://www.mafengwo.cn/ajax/router.php'
    for num in range(1, 4):
        params = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': 34639,
            'iTagId': 0,
            'iPage': num
        }
        pos = requests.post(url=router_url, data=params).json()
        print(type(pos))
        for key in pos:
            print(key, pos[key])
        soup_pos = BeautifulSoup(pos['data']['list'], 'lxml')

        result = [{'scenery': p['title'], 'href': re.findall(re.compile(r'/poi/(\d+).html'), p['href'])[0]} for p in
                  soup_pos.find_all('a')]
        total.extend(result)

    return total

totals = get_param()
for i in range(len(totals)):
    print(totals[i])