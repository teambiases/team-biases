import scrapy

from biases.scrape.items import EndpointArticle

class UnitedWithIsraelSpider(scrapy.Spider):
    """
    Spider to scrape United with Israel (https://unitedwithisrael.org/).
    """

    name = 'united_with_israel'
    start_urls = ['https://unitedwithisrael.org/']

    def parse(self, response):
        for category_link in response.css('.category_nav a::attr(href)').extract():
            yield scrapy.Request(category_link, callback=self.parse_category)

    def parse_category(self, response):
        for article_link in response.css('.page-header a::attr(href)').extract():
          yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        article = EndpointArticle()
        article['title'] = response.css('.single-title > span::text').extract_first()
        for possible_author in response.css('.span8 .post_content > p > em::text').extract():
            if possible_author.startswith('By: '):
                    article['author'] = possible_author[4:]

        texts = response.css('#content #main .post_content > p::text').extract()
        article['content'] = ' '.join(texts)
        article['date'] = response.css('.span1 > p > time::text').extract_first()
        article['url'] = response.url

        article['domain'] = 'ipconflict'
        article['endpoint'] = 'united_with_israel'
        article['lang'] = 'en'

        yield article
