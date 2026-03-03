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
            data = i.xpath(".//td")

            absolute_link = response.urljoin(data[2].css('a::attr(href)').get())
            
            yield response.follow(absolute_link,
                                  callback=self.parse_syllabus_page,
                                  meta = {"Course Name": data[0].css('td::text').get(),
                                          "Scheme-Link": data[1].css('a::attr(href)').get()})

            

        
    def parse_syllabus_page(self,response):
        left_block = response.css('div.col-md-6')
        syllabus = left_block.css('div.syllabus-content')
        rows = syllabus.xpath('.//tr[td]')
        group = {}

        for i in rows:
            which_sem = i.xpath('.//a[@class="package-title"]/text()').get()
            upload_date = i.xpath('.//span[@class="__dt_update_date "]/text()').get()
            syllabus_link = i.css('a.wpdm-download-link.download-on-click.btn.btn-primary::attr(data-downloadurl)').get()

            group[which_sem] = [response.meta["Course Name"], response.meta["Scheme-Link"], syllabus_link, upload_date]
        
        yield group
            
        

            
        
