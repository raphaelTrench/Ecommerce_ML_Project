# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class NetshoesPipeline(object):
    def process_item(self, item, spider):
        item['images'] = [p['path'] for p in item['images']]
        return item

class ShoeImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename','')

    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            meta = {'filename': url.split('/')[-1]}
            yield Request(url=url, meta=meta)