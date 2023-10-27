# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiteraturecitationratecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 期刊名
    literatureName = scrapy.Field()
    # 总引率
    totalCitesList = scrapy.Field()
    # 自引率
    selfCitesList = scrapy.Field()
    # 年份
    ageList = scrapy.Field()
    pass
