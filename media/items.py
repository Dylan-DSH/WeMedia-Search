# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaItem(scrapy.Item):
    wemedia_name = scrapy.Field()
    wemedia_id = scrapy.Field()
    wemedia_url = scrapy.Field()
    website_id = scrapy.Field()
    auth_level = scrapy.Field()
    create_time = scrapy.Field()