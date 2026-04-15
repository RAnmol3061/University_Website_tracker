# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

class UnitrackerPipeline:
    def process_item(self, item):   

        # Removes branch name and only keeps semester number
        match = re.search(r'semester \d', item.semester, re.IGNORECASE)
        if match:
            item.semester = match.group().capitalize()

        return item
