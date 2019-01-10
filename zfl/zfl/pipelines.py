# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import re

class ZflPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['imgurl']:
            yield Request(img_url, meta={'item':item['title']})
    
    def file_path(self, request, response=None, info=None):
        img_alt = request.url.split('/')[-1]
        title = request.meta['item']
        title = re.sub(r'[？\\*|“<>:/]', '', title)
        filename = u'full/{}/{}'.format(title, img_alt)
        return filename
    
    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item    
