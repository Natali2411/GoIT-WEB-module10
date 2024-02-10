import scrapy
from scrapy.crawler import CrawlerProcess

from quoteapp.rabbit.producer import publish_author_info


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "data/quotes.json"}

    def parse(self, response, **kwargs):

        for quote in response.xpath("/html//div[@class='quote']"):
            author_url = quote.xpath("//a[contains(@href, 'author')]/@href").get()
            author_name = quote.xpath("span/small/text()").extract_first()

            # Send info about author to RabbitMQ
            publish_author_info(author_name=author_name, author_part_link=author_url)
            yield {
                "tags": quote.xpath(
                    "div[@class='tags']/a/text()").extract(),
                "author": author_name,
                "quote": quote.xpath(
                    "span[@class='text']/text()").extract_first(),
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
        else:
            publish_author_info()


# run spider QuotesSpider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
