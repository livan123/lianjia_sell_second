# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class LianjiaPipeline(object):

    def __init__(self):
      self.csvwriter = csv.writer(open('lianjia_houses.csv', 'w', newline=''), delimiter=',')
      self.csvwriter.writerow(['第几套房','链接','标题','房型','总价','位置','单价','房屋概况'])

    def process_item(self, item, spider):

        rows = zip(item['ii'],
                   item['url'],
                   item['title'],
                   item['typess'],
                   item['total_price'],
                   item['location'],
                   item['price'],
                   item['basic_facts'],
                   )

        for row in rows:
            self.csvwriter.writerow(row)

        return item
