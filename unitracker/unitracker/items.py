# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class SchemeItem:
    course_name: str
    scheme_link: str
    scheme_etag: str
    syllabus_link: str
    upload_date: str
    semester: str
    syllabus_content_length: str