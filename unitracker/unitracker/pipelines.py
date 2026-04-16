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
                         Scheme_Link TEXT,
                         Syllabus_Link TEXT,
                         Scheme_ETAG TEXT,
                         Syllabus_Content_Length INTEGER,
                         Upload_Date TEXT
                         )
                         """)
        self.con.commit()
    
    def process_item(self,item):
        self.cur.execute("""INSERT INTO syllabus (Course_Name, Semester, Scheme_Link, Syllabus_Link, Scheme_ETAG, Syllabus_Content_Length,Upload_Date) VALUES (?, ?, ?, ?, ?, ?, ?)""", (item.course_name, item.semester, item.scheme_link, item.syllabus_link, item.scheme_etag, item.syllabus_content_length, item.upload_date))

        return item
    
    def close_spider(self):
        self.con.commit()
        self.con.close()