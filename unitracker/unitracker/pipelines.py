# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import sqlite3

class UnitrackerPipeline:
    def process_item(self, item):   

        # Removes branch name and only keeps semester number
        match = re.search(r'semester \d', item.semester, re.IGNORECASE)
        if match:
            item.semester = match.group().capitalize()

        return item

class SavetoDBPipeline:
    def open_spider(self):
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS syllabus (
                         Course_Name TEXT,
                         Semester TEXT,
                         Scheme_Link TEXT
                         Syllabus_Link TEXT
                         Scheme_ETAG TEXT
                         Syllabus_Content_Length INTEGER
                         Upload_Date TEXT
                         )
                         """)
        self.con.commit()
    

