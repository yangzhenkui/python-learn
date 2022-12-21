# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义item中的字段名称，其实item可以看作是一个字典
    name = scrapy.Field()
    address = scrapy.Field()
    link = scrapy.Field()
    nickname = scrapy.Field()
    # pass
