#coding=utf-8
'''
国土资源奖
'''
import re

import scrapy
from landandresourceaward.items import LandandresourceawardItem
from scrapy.crawler import CrawlerProcess


class LandANDResourseAward(scrapy.Spider):
    name = "lar_spider"
    part_award_end_page = 113
    national_award_end_page = 9
    
    pageSizeNum = "20"
    pageSize = "20"
    
    field_tuple = ("asequence", "pname", "munit", "mperson", "anumber", "awardtype", "rank")
    
    def start_requests(self):
        urls = [
            'http://jlps.mnr.gov.cn/global/reward!listAllReward.do',
            'http://jlps.mnr.gov.cn/global/reward!award.do'
        ]
#         for _p in range(1, self.part_award_end_page + 1):
#             yield scrapy.FormRequest(
#                     url = urls[0],
#                     formdata = {
#                         "pageNo" : str(_p),
#                         "pageSize" : self.pageSize,
#                         "pageSizeNum" : self.pageSizeNum,
#                         "currentPageNo" : str(_p - 1) if _p - 1 > 0 else str(_p),
#                         "goInput" : str(_p - 1) if _p - 1 > 0 else str(_p),
#                     },
#                     callback = self.parse,
#                     meta = {
#                         "m_url" : "http://jlps.mnr.gov.cn/global/reward!readResult.do",
#                         "type" : 1 #部分奖
#                     }
#                 )
        
        for _p in range(1, self.national_award_end_page + 1):
            yield scrapy.FormRequest(
                    url = urls[1],
                    formdata = {
                        "pageNo" : str(_p),
                        "pageSize" : self.pageSize,
                        "pageSizeNum" : self.pageSizeNum,
                        "currentPageNo" : str(_p - 1) if _p - 1 > 0 else str(_p),
                        "goInput" : str(_p - 1) if _p - 1 > 0 else str(_p),
                    },
                    callback = self.parse,
                    meta = {
                        "m_url" : "http://jlps.mnr.gov.cn/global/reward!readCountryResult.do",
                        "type" : 0 #国家奖
                        }
                )
    
    def parse(self, response):
        content_table = response.xpath("//div[@class='tablebox']/table")[1]
        
        trs = content_table.xpath(".//tr")
        for tr in trs[1:]:
            tds = tr.xpath("./td")
            op_td = tds[-1]
            onclick_text = op_td.xpath("./a/@onclick").extract_first()
            if onclick_text:
                result = re.search(r"(view|read1)\('(.*?)',?", onclick_text)
                if result:
                    if result.groups():
                        resultId = result.groups()[1]
                        yield scrapy.Request(url = response.meta["m_url"] + f"?resultId={resultId}", callback=self.parse_detail, meta=response.meta)
    
    def parse_detail(self, response):
        lar_item = LandandresourceawardItem()
        
        if response.meta["type"] == 0:
            lar_item["type"] = "国家奖"
        if response.meta["type"] == 1:
            lar_item["type"] = "部分成果奖"
        
        trs = response.xpath("//div[@class='tablebox']/table//tr")[:7]
        for index, tr in enumerate(trs, 0):
            tds = tr.xpath("./td")
            if len(tds) > 1:
                value = tds[1].xpath("string(.)").extract_first()
                if not value.strip():
                    value = tds[1].xpath("./@textContent").extract_first()
                if value:
                    lar_item[self.field_tuple[index]] = value.strip()
        
        return lar_item
                    

#调试使用
# if __name__ == "__main__":
#     import scrapy.cmdline
#     def main():
#         scrapy.cmdline.execute(['scrapy', 'crawl', 'lar_spider'])
#     main()

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    
    process.crawl(LandANDResourseAward)
    process.start()           
                
            
        
        
        
