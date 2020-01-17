# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoesItem(scrapy.Item):
    raw_name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    customer_reviews_number = scrapy.Field()
    customer_score = scrapy.Field()
    customer_recommendation_rate = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    nationality = scrapy.Field()
    material = scrapy.Field()
    usage_type = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    colors = scrapy.Field()

