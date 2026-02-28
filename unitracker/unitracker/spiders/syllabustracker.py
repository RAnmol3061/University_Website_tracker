import scrapy


class SyllabustrackerSpider(scrapy.Spider):
    name = "syllabustracker"
    allowed_domains = ["csvtu.ac.in"]
    start_urls = ["https://csvtu.ac.in/ew/programs-and-schemes/"]

    def parse(self, response):
        left_block = response.css('div.col-md-6')
        btech = left_block.xpath('.//a[normalize-space(.)="Bachelor of Technology (B.Tech.) with effective from session 2025-26 (for students enrolled from the year 2025-26)"]/ancestor::div[2]')
        final = btech.xpath(".//table//tr")

        for i in final:
            data = i.xpath(".//td").getall()
            yield {
                "Course Name": data[0],
                "Scheme-Link": data[1],
                "Syllabus-Link": data[2],
            }

        


            
