import scrapy


class SyllabustrackerSpider(scrapy.Spider):
    name = "syllabustracker"
    allowed_domains = ["csvtu.ac.in"]
    start_urls = ["https://csvtu.ac.in"]

    def parse(self, response):
        pass
