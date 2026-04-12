import scrapy
from unitracker.items import SchemeItem


class SyllabustrackerSpider(scrapy.Spider):
    name = "syllabustracker"
    allowed_domains = ["csvtu.ac.in"]
    start_urls = ["https://csvtu.ac.in/ew/programs-and-schemes/"]

    def parse(self, response):
        left_block = response.css('div.col-md-6')
        btech = left_block.xpath('.//a[normalize-space(.)="Bachelor of Technology (B.Tech.) with effective from session 2025-26 (for students enrolled from the year 2025-26)"]/ancestor::div[2]')
        final = btech.xpath(".//table//tr")

        allowed_course = ['computer']

        for i in final:
            data = i.xpath(".//td")
            course_name = data[0].css('td::text').get()
            scheme_link = response.urljoin(data[1].css('a::attr(href)').get())
            absolute_link = response.urljoin(data[2].css('a::attr(href)').get())

            course_name_set = set(course_name.lower().split())

            if not any(i in course_name_set for i in allowed_course):
                continue
            
            yield scrapy.Request(scheme_link,
                                 method='HEAD',
                                 callback=self.getetag,
                                 meta = {"branchwise_link": absolute_link, 
                                          "Course Name": course_name,
                                          "Scheme-Link": scheme_link})

    def getetag(self,response):
        etag_binary = response.headers.get('ETag', b'')
        etag = etag_binary.decode('utf-8')

        parse_meta = response.meta.copy()
        parse_meta['etag'] = etag

        yield response.follow(response.meta['branchwise_link'],
                              callback=self.parse_syllabus_page,
                              meta = parse_meta)
            

        
    def parse_syllabus_page(self,response):
        left_block = response.css('div.col-md-6')
        syllabus = left_block.css('div.syllabus-content')
        rows = syllabus.xpath('.//tr[td]')
        group = {}

        for i in rows:
            which_sem = i.xpath('.//a[@class="package-title"]/text()').get()
            upload_date = i.xpath('.//span[@class="__dt_update_date "]/text()').get()
            syllabus_link = i.css('a.wpdm-download-link.download-on-click.btn.btn-primary::attr(data-downloadurl)').get()
        
            yield SchemeItem(course_name = response.meta["Course Name"],
                scheme_link = response.meta["Scheme-Link"],
                scheme_etag = response.meta["etag"],
                syllabus_link = syllabus_link,
                upload_date = upload_date,
                semester = which_sem)
        

            
        
