# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class LiteraturecitationratecrawlerPipeline:
    def open_spider(self, spider):  # 在爬虫开启的时候仅执行一次
        self.writer = csv.writer(open('result.csv', 'a+', encoding='utf-8', newline=''))

    def process_item(self, item, spider):
        self.writer.writerow([item['literatureName']])
        # 将list1中的元素横向写入CSV文件
        self.writer.writerow([None] + item['ageList'] + [None] + item['ageList'])
        # 将list4中的元素横向写入CSV文件，并与list2同行相距一列
        self.writer.writerow([None] + item['selfCitesList']+ [None] + item['totalCitesList'])
        print("write")
        return item
