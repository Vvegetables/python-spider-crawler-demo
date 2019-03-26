# -*- coding: utf-8 -*-
from openpyxl.workbook.workbook import Workbook
from scrapy.exporters import JsonItemExporter


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class LandandresourceawardPipeline(object):
    def process_item(self, item, spider):
        return item

class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["奖项类型", "获奖序号", "项目名称", "主要完成单位", "主要完成人", "获奖证书编号", "奖种", "等级"])
    
    def process_item(self, item, spider):
        line = [
            item.get("type"), item.get("asequence"), item.get("pname"),
            item.get("munit"), item.get("mperson"), item.get("anumber"),
            item.get("awardtype"), item.get("rank")
        ]
        
        self.ws.append(line)
        self.wb.save("landandresourceaward.xlsx")
        
        return item
    
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open("larexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
        
        
        
        
