import scrapy

class EndpointArticle(scrapy.Item):
    domain = scrapy.Field()
    endpoint = scrapy.Field()
    lang = scrapy.Field() # 2 letter language code
    
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field(serializer=str)
    url = scrapy.Field()
