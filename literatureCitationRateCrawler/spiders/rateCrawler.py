import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from literatureCitationRateCrawler.items import LiteraturecitationratecrawlerItem
import csv
class RatecrawlerSpider(scrapy.Spider):
    name = "rateCrawler"
    csv_filename = '../sourceFile/discontinued3.csv'
    # 打开CSV文件并读取数据
    with open(csv_filename, 'r', newline='', encoding='latin-1') as csvfile:
        csvreader = csv.reader(csvfile)

        # 读取CSV文件的第一行，即标题行
        headers = next(csvreader)

        # 根据标题行中的内容确定Title所在的列索引
        title_column_index = headers.index('Title')

        # 初始化一个列表以存储Title列的内容
        title_column_data = []

        # 遍历CSV文件的其余行，获取Title列的内容
        for row in csvreader:
            title_column_data.append(row[title_column_index])

    # title_column_data 现在包含了Title列的所有内容
    print(title_column_data)
    urls = []
    for literatureName in title_column_data:
        url = 'https://www.scimagojr.com/journalsearch.php?q=' + literatureName.replace(' ', '+')
        print(url)
        urls.append(url)

    def start_requests(self):
        for url in self.urls:
            # literatureName = url.split('=')[-1].replace('+', ' ')
            # yield scrapy.Request(url=url,meta={'name': literatureName})
            yield scrapy.Request(url=url)
    def parse(self, response):
        # 模式1:获取搜索列表所有期刊
        # aList = response.xpath("//div[@class='search_results']/a");
        # aList = response.xpath("//div[@class='search_results']/a[1]");
        # for a in aList:
        #     href = "https://www.scimagojr.com/" + a.xpath('./@href').extract_first()
        #     print(href)
        #     literatureName = response.meta.get("name")
        #     print("literatureName:" + response.meta.get("name"))
        #     # 爬取具体的文献自引率
        #     yield scrapy.Request(url=href, callback=self.parse_next, meta={'name': literatureName})

        # 模式2:获取搜索列表第一个期刊
        a = response.xpath("//div[@class='search_results']/a[1]");
        literatureName = response.xpath("//div[@class='search_results']/a[1]/span/text()").extract_first()
        href = "https://www.scimagojr.com/" + a.xpath('./@href').extract_first()
        print(href)
        # 爬取具体的文献自引率
        yield scrapy.Request(url=href, callback=self.parse_next, meta={'name': literatureName})
    def parse_next(self, response):
        text_elements = response.xpath("//div[@class='dashboard']/div[4]/div[@class='cellcontent']//table/tbody/tr/td/text()").extract()
        text_elements_len = len(text_elements)
        # 分割线，前一半是自引率，后一半是总引率
        divider = text_elements_len / 2
        count = 0
        selfCiteList = []
        totalCiteList = []
        ageList = []
        item = LiteraturecitationratecrawlerItem()
        # 打印匹配到的所有文本
        for text in text_elements:
            if count <= divider:
                if count % 3 == 2:
                    selfCiteList.append(text)
                elif count % 3 == 1:
                    ageList.append(text)
            else:
                if count % 3 == 2:
                    totalCiteList.append(text)
            count += 1
            print(text.strip())
        item['literatureName'] = response.meta.get('name')
        item['totalCitesList'] = totalCiteList
        item['selfCitesList'] = selfCiteList
        item['ageList'] = ageList
        yield item

        # print("自引")
        # self.ceshi(selfCiteList)
        # print("自引年份")
        # self.ceshi(selfCiteAgeList)
        # print("总引")
        # self.ceshi(totalCiteList)
        # print("总引年份")
        # self.ceshi(totalCiteAgeList)

    # def ceshi(self, a):
    #     for i in a:
    #         print(i+" ")
if __name__ == '__main__':
    # 创建 CrawlerProcess 实例，并传入项目设置
    process = CrawlerProcess(settings=get_project_settings())

    # 添加爬虫到 CrawlerProcess
    process.crawl(RatecrawlerSpider)

    # 启动爬虫
    process.start()