import scrapy
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


class CryptofeedItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    datetime = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
