# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy.statscollectors


class PostItem(scrapy.Item):
    image_url = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    date_published = scrapy.Field()
    type = scrapy.Field()
