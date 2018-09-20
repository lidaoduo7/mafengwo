# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from mafengwo.items import MafengwoItem
import re
import requests

'''
参考：https://blog.csdn.net/beyond9305/article/details/80713665
     https://blog.csdn.net/qq_28053189/article/details/79538978
'''

class LvyouSpiderSpider(scrapy.Spider):
    name = 'lvyou_spider'
    allowed_domains = ['mafengwo.cn']
    # start_urls = ['http://mafengwo.cn/']
    # start_urls = ['http://www.mafengwo.cn/jd/34639/gonglve.html']
    start_urls = ['http://www.mafengwo.cn/poi/6335328.html',
                  'http://www.mafengwo.cn/poi/2947.html'
                  ]  #矮寨大桥

    def parse(self, response):
        print("网页信息")
        print(response.url)
        # print(response.text)

        selector = Selector(response)
        item = MafengwoItem()

        group = re.findall(r'<a title="蜂蜂点评">蜂蜂点评<span>（(\d+)条）</span></a>', response.text)  #评论数
        remark_acccount = int(group[0])
        print(remark_acccount)

        group = re.findall(r"http://www.mafengwo.cn/poi/(.*).html", response.url)     #提取出景点的id标示
        poi_id = group[0]

        self.parse_scene(poi_id)

        source = "website"
        item['source'] = source
        second_source = "mafengwo"
        item['second_source'] = second_source
        item['remark_acccount'] = remark_acccount
        scene_name = self.get_scene_name(poi_id)
        item['scene_name'] = scene_name
        yield item

    def get_scene_name(self, poi_id):
        '''
        从网址中解析出景点的名称
        :param poi_id:网址http://www.mafengwo.cn/poi/6335328.html中的6335328
        :return:
        '''
        name_dict = {"6335328": "矮寨大桥",
                     "dehang": "德夯",
                     "dehangdizhigongyuan": "德夯地址公园",
                     "liushapubu": "流沙瀑布",
                     "2947": "德夯苗寨",
                     "xianglushangumiaozhai": "香炉山古苗寨",
                     "baxianhu": "八仙湖"}
        return name_dict[poi_id]

#http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery1810043045428484501436_1537415257075&params=%7B%22poi_id%22%3A%225426352%22%2C%22page%22%3A2%2C%22just_comment%22%3A1%7D&_=1537415437842
    def parse_scene(self,poi_id):
        # 设置URL的第一部分
        url1 = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery1810043045428484501436_1537415257075&params={"poi_id":"'
        # 设置URL的第二部分
        url2 =  '","page":'
        url4 = ',"just_comment":1}'
        page = 1
        url = url1 + str(poi_id) + url2 + str(page) +url4
        r = requests.get(url=url)
        html = r.content
        ht1 = html.decode('unicode-escape')
        # print("内容")
        # print(ht1)
        # file = open(poi_id, 'w', encoding='utf-8')
        # file.write(ht1)
        # file.close()

        pos = requests.get(url=url).json()
        print(type(pos))
        for key in pos:
            print(key, pos[key])



