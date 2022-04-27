import scrapy

from web_plan.items import WebPlanItem

class QuotesSpider(scrapy.Spider):
    
    name = 'uep-plan'
    
    start_urls = ['https://app.ue.poznan.pl/Schedule/Home/GetTimeTable?dep=106&cyc=1&year=3&group=10613001&type=2&_=1650825781983']
    
    weekends_dict = {}
    
    def parse(self, response):
        
        item = WebPlanItem()
        
        weekends_dict = {}
        table = response.xpath('/html/body/table[1]/tbody')
        rows = table.xpath('//tr')
        for count, row in enumerate(rows):
            str_list = []
            weekend =  row.css('::text').extract()
            for string_line in weekend:
                str_list.append(string_line.strip())
            str_list = [x for x in str_list if x]
            weekends_dict[str(count)] = str_list
        
        item['weekends_dict'] = weekends_dict
        
        yield item