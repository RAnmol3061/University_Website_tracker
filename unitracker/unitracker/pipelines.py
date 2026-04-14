# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from unitracker.items import SchemeItem


class UnitrackerPipeline:
    def process_item(self, item, spider):

        # Removes branch name and only keeps semester number
        if '1' in item.semester:
            item.semester = "Semester 1"
        elif '2' in item.semester:
            item.semester = "Semester 2"

        return item
