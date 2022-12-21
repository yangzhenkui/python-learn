import scrapy
from myScrapyProject.items import MyscrapyprojectItem
from faker import Faker, Factory

# 出现该错误时：ModuleNotFoundError: No module named 'attrs'
# 使用该命令即可解决上述错误：pip install attrs --upgrade

# scrapy startproject xxxx：创建一个xxx的scrapy项目
# scrapy genspider example example.com： 创建一个爬取页面
# scrapy crawl example：运行爬虫程序


class ThespiderSpider(scrapy.Spider):
    name = 'theSpider'  # 爬虫的名字
    # 设置allowed_domains的含义是过滤爬取的域名
    # allowed_domains = ['www.baidu.com']
    page_number = 1
    base_url = 'https://bj.fang.ke.com/loupan/pg%s/'
    start_urls = [base_url%page_number]
    User_Agent = Factory.create()




    # todo 第一次联系笔记
    # def parse(self, response):
    #     # 首先获取到显示楼盘名的ul列表
    #     main_li_list = response.xpath("/html/body/div[6]/ul[2]/li")
    #
    #     for li in main_li_list:
    #         # 单独的对每个li下的数据进行提取
    #         # @表示提取属性中的值
    #         name = li.xpath("./a/@title").extract()[0]
    #         address = li.xpath("./div/a[1]/text()").extract()[-1].strip()
    #         # 声明item对象
    #         item = MyscrapyprojectItem()
    #         item["name"] = name
    #         item["address"] = address
    #         # 这儿yield的数据会进到pipelines的process_item()方法中进行处理
    #         yield item
    #         # print(name, address)
    #     # print(response.text)

    # todo 第一阶段 多次调用多页
    # def parse(self, response):
    #     main_li_list = response.xpath("/html/body/div[6]/ul[2]/li")
    #     for li in main_li_list:
    #         name = li.xpath("./a/@title").extract_first()
    #         address = li.xpath("./div/a[1]/text()").extract()[-1].strip()
    #         item = MyscrapyprojectItem()
    #         item["name"] = name
    #         item['address'] = address
    #         # yield item
    #         print(name, address)
    #         if self.page_number <= 3:
    #             self.page_number += 1
    #             new_url = self.base_url%self.page_number
    #             yield scrapy.Request(url=new_url, callback=self.parse)


    # todo 第二阶段 完成页面 一个页面全部数据的穿透 ,注意这里的数据被分割了
    # 即是在同时爬取首页和详情页的信息
    # def parse(self, response):
    #     main_li_list = response.xpath("/html/body/div[6]/ul[2]/li")
    #     for li in main_li_list:
    #         name = li.xpath("./a/@title").extract_first()
    #         address = li.xpath("./div/a[1]/text()").extract()[-1].strip()
    #         link = "https://bj.fang.ke.com/"+li.xpath('./a/@href').extract_first()
    #         item = MyscrapyprojectItem()
    #         item["name"] = name
    #         item['address'] = address
    #         item['link'] = link
    #         # meta将数据传入到回调的函数中
    #         yield scrapy.Request(url=link, callback=self.detail_page_parse, meta={"item": item})
    #
    # def detail_page_parse(self, response):
    #     item = response.meta['item']
    #     nickname = response.xpath("//*[@class='other-name']/text()").extract()[-1].strip()
    #     item['nickname'] = nickname
    #     yield item
    #     # print(item)


    # todo 第三阶段 联合多页面 以及详情页面的 闭环爬取
    total = []
    def parse(self, response):
        main_li_list = response.xpath("/html/body/div[6]/ul[2]/li")
        for li in main_li_list:
            name = li.xpath("./a/@title").extract_first()
            address = li.xpath("./div/a[1]/text()").extract()[-1].strip()
            link = "https://bj.fang.ke.com/" + li.xpath('./a/@href').extract_first()
            item = MyscrapyprojectItem()
            item["name"] = name
            item['address'] = address
            item['link'] = link
            self.total.append(link)
            yield scrapy.Request(url=link, callback=self.detail_page_parse, meta={"item": item})

    def detail_page_parse(self, response):
        item = response.meta['item']
        nickname = response.xpath("//*[@class='other-name']/text()").extract()[-1].strip()
        item['nickname'] = nickname
        yield item
        if self.page_number <= 3:
            self.page_number += 1
            new_link = self.base_url % self.page_number
            print("正在处理的页面为："+new_link)
            scrapy.Request(url=new_link, callback=self.parse)



