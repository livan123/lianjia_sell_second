# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem
from scrapy.http import Request
import urllib.request
from lxml import etree
import time

class FangziSpider(scrapy.Spider):
    name = 'fangzi'
    allowed_domains = ['lianjia.com']
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
    start_urls = ['http://sh.lianjia.com/ershoufang/pudong',
                  'http://sh.lianjia.com/ershoufang/minhang',
                  'http://sh.lianjia.com/ershoufang/baoshan',
                  'http://sh.lianjia.com/ershoufang/xuhui',
                  'http://sh.lianjia.com/ershoufang/putuo',
                  'http://sh.lianjia.com/ershoufang/yangpu',
                  'http://sh.lianjia.com/ershoufang/changning',
                  'http://sh.lianjia.com/ershoufang/songjiang',
                  'http://sh.lianjia.com/ershoufang/jiading',
                  'http://sh.lianjia.com/ershoufang/huangpu',
                  'http://sh.lianjia.com/ershoufang/jingan',
                  'http://sh.lianjia.com/ershoufang/zhabei',
                  'http://sh.lianjia.com/ershoufang/hongkou',
                  'http://sh.lianjia.com/ershoufang/qingpu',
                  'http://sh.lianjia.com/ershoufang/fengxian',
                  'http://sh.lianjia.com/ershoufang/jinshan',
                  'http://sh.lianjia.com/ershoufang/chongming',
                  'http://sh.lianjia.com/ershoufang/shanghaizhoubian',
                  ]

    def parse(self, response):

        counts = response.xpath("//div[@class='column location']/div[2]/div[2]/div/@class").extract()
        for i in range(2, len(counts)+1):
            area = response.xpath("//div[@class='column location']/div[2]/div[2]/div["+str(i)+"]/a/@href").extract()
            # 各个小区域的url
            urls = "http://sh.lianjia.com"+area[0]
            houses = urllib.request.urlopen(urls).read().decode("utf-8", "ignore")
            housess = etree.HTML(houses, parser=None, base_url=None)
            nums = housess.xpath("//div[@class='search-result']/span/text()")

            # 计算一共有多少页：
            if(nums[0]!='0'):
                page_num = int(nums[0])/30
                for j in range(1, int(page_num)+2):
                    url = urls+"/d"+str(j)
                    print(url)
                    yield Request(url, headers=self.header, meta={"url":url}, callback=self.parse_Detail)

    def parse_Detail(self, response):

        items = LianjiaItem()

        # 一页有多少房子：
        counts = response.xpath("//ul[@class='js_fang_list']/li/div/@class").extract()

        # 标题
        items["title"] = response.xpath("//div[@class='prop-title']/a/text()").extract()

        # 房型
        typesss = []
        ii = []
        urls = []
        for i in range(1, len(counts)+1):
            ii.append(str(i))
            path = "//ul[@class='js_fang_list']/li["+str(i)+"]/div/div[@class='info-table']/div[1]/span//text()"
            houses_type = response.xpath(path).extract()
            housesss = []
            for j in range(0, len(houses_type)):
                houses_typess = houses_type[j].replace('\t', '').replace('\n','')
                housesss.append(houses_typess)
            houses_types = ''.join(housesss)
            typesss.append(houses_types)
            url = response.meta["url"]
            urls.append(url)
        items["typess"] = typesss
        items["ii"] = ii
        items["url"] = urls

        # 总价：
        total_pricess = []
        total_price = response.xpath("//div[@class='info-table']/div[1]/div/span[1]/text()").extract()
        for i in range(0, len(total_price)):
            print("第"+str(i)+"套房子")
            total_prices = total_price[i]+"万"
            total_pricess.append(total_prices)
        items["total_price"] = total_pricess

        #位置
        locationssss = []
        for i in range(1, len(counts)+1):
            path = "//ul[@class='js_fang_list']/li["+str(i)+"]/div/div[@class='info-table']/div[2]/span[1]//text()"
            location = response.xpath(path).extract()
            locationss = []
            for j in range(0, len(location)):
                locations = location[j].replace('\t', '').replace('\n','')
                locationss.append(locations)
            locationsss = ''.join(locationss)
            locationssss.append(locationsss)
        items["location"] = locationssss

        # 单价：
        pricesss = []
        prices = response.xpath("//div[@class='info-table']/div[2]/span[2]/text()").extract()
        for i in range(0,len(prices)):
            ii.append(i)
            pricess = prices[i].replace('\t', '').replace('\n','')
            pricesss.append(pricess)
        items["price"] = pricesss

        # 房屋概况
        factssss = []
        for i in range(1, len(counts)+1):
            path = "//ul[@class='js_fang_list']/li["+str(i)+"]/div/div[@class='property-tag-container']//text()"
            fact = response.xpath(path).extract()
            factss = []
            for j in range(0, len(fact)):
                facts = fact[j].replace('\t', '').replace('\n','')
                factss.append(facts)
            factsss = ''.join(factss)
            factssss.append(factsss)
        items["basic_facts"] = factssss

        yield items

