# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from mafengwo.items import MafengwoItem
import re
import requests
import math

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
                  'http://www.mafengwo.cn/poi/2947.html',
                  'http://www.mafengwo.cn/poi/5426352.html',
                  'http://www.mafengwo.cn/poi/6335495.html',
                  'http://www.mafengwo.cn/poi/6625199.html',
                  'http://www.mafengwo.cn/poi/3112102.html',
                  'http://www.mafengwo.cn/poi/6330877.html',
                  'http://www.mafengwo.cn/poi/3121722.html',
                  'http://www.mafengwo.cn/poi/8872554.html',
                  'http://www.mafengwo.cn/poi/8469860.html',
                  'http://www.mafengwo.cn/poi/7560938.html',
                  'http://www.mafengwo.cn/poi/7948843.html',
                  'http://www.mafengwo.cn/poi/6330882.html',
                  'http://www.mafengwo.cn/poi/6330879.html',
                  'http://www.mafengwo.cn/poi/6330885.html',
                  'http://www.mafengwo.cn/poi/7668364.html',
                  'http://www.mafengwo.cn/poi/26264873.html',
                  'http://www.mafengwo.cn/poi/33644268.html',
                  'http://www.mafengwo.cn/poi/33628100.html',
                  'http://www.mafengwo.cn/poi/33644484.html',
                  'http://www.mafengwo.cn/poi/52944408.html',
                  'http://www.mafengwo.cn/poi/33644188.html',
                  'http://www.mafengwo.cn/poi/33644336.html',
                  'http://www.mafengwo.cn/poi/33644160.html',
                  'http://www.mafengwo.cn/poi/33644504.html',
                  'http://www.mafengwo.cn/poi/33644496.html',
                  'http://www.mafengwo.cn/poi/33644180.html',
                  'http://www.mafengwo.cn/poi/33644416.html',
                  'http://www.mafengwo.cn/poi/33644420.html',
                  'http://www.mafengwo.cn/poi/33644512.html',
                  'http://www.mafengwo.cn/poi/33644432.html',
                  'http://www.mafengwo.cn/poi/33644428.html'
                  ]

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

        results = self.parse_scene(poi_id,remark_acccount)
        comments_list = []
        for i in range(len(results)):
            comment = results[i][0]
            comment_time = results[i][1]
            comments_dict = {'comment_time': comment_time, 'comment': comment}
            comments_list.append(comments_dict)
        item['comments'] = comments_list

        source = "website"
        item['source'] = source
        second_source = "mafengwo"
        item['second_source'] = second_source
        item['url'] = response.url
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
                     "2947": "德夯苗寨",
                     "5426352": "德夯大峡谷",
                     "6335495": "乾州古城",
                     "6625199": "天问台",
                     "3112102": "德夯风景名胜区",
                     "6330877": "流沙瀑布",
                     "3121722": "矮寨镇",
                     "8872554": "吉首大学砂子坳校区",
                     "8469860": "黄永玉艺术博物馆",
                     "7560938": "德夯地质公园",
                     "7948843": "玉泉溪",
                     "6330882": "九龙溪",
                     "6330879": "盘古峰",
                     "6330885": "东门坡公园",
                     "7668364": "寨阳",
                     "26264873": "吉斗苗寨",
                     "33644268": "乾州城隍庙",
                     "33628100": "苗民起义古战场",
                     "33644484": "吉斗寨",
                     "52944408": "山谷居民原创民族文化体验馆",
                     "33644188": "骆驼峰",
                     "33644336": "流沙瀑布",
                     "33644160": "玉泉溪",
                     "33644504": "罗荣光故居",
                     "33644496": "天心庵",
                     "33644180": "驷马峰",
                     "33644416": "德夯村",
                     "33644420": "胡家塘",
                     "33644512": "杨岳斌故居",
                     "33644432": "接龙桥",
                     "33644428": "乾州三门开"
                     }
        return name_dict[poi_id]

#http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery1810043045428484501436_1537415257075&params=%7B%22poi_id%22%3A%225426352%22%2C%22page%22%3A2%2C%22just_comment%22%3A1%7D&_=1537415437842
    def parse_scene(self,poi_id,remark_acccount):
        # 设置URL的第一部分
        url1 = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery1810043045428484501436_1537415257075&params={"poi_id":"'
        # 设置URL的第二部分
        url2 =  '","page":'
        url4 = ',"just_comment":1}'
        results = [] #
        pageNum = math.ceil(remark_acccount/15)
        for page in range(1,pageNum+1,1):
            print("当前爬取第：%s页",page)
            url = url1 + str(poi_id) + url2 + str(page) + url4
            r = requests.get(url=url)
            html = r.content
            ht1 = html.decode('unicode-escape')
            ht2 = ht1.replace('\/', '/')
            ht3 = ht2.replace(r'<br \/>', '')  # 替换换行
            print("内容")
            # print(ht1)
            # file = open(poi_id, 'w', encoding='utf-8')
            # file.write(ht1)
            # file.close()

            remark_contents = re.findall(r'<p class="rev-txt">(.*)', ht3)
            times = re.findall(r'<span class="time">(.*)<\/span>', ht3)
            # group = re.findall(r'<p class="rev-txt">(.*)</p>',ht3)      #每页15条评论，正则碰到强制换行，待解决！
            # group = re.findall(r'德夯苗寨',ht2)
            print(type(remark_contents))
            for i in range(len(remark_contents)):
                print((remark_contents[i], times[i]))
                results.append((remark_contents[i].replace("</p>", ""), times[i]))
        return results







