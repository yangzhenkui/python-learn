# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyscrapyprojectPipeline:
    # 这个方法 处理item类型对象的
    # 用于持久化存储
    # 每接收一次 调用一次
    def process_item(self, item, spider):
        # yield的数据会在这儿进行处理
        print(item)
        # return item
