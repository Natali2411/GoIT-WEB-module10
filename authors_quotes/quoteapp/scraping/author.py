import queue
import threading
import time
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

from authors_quotes.settings import RABBITMQ_QUEUE
from quoteapp.rabbit.consumer import read_rabbit_msg
from quoteapp.rabbit.rabbit_connect import make_exchange_queue_bind

locker = threading.RLock()


class AuthorSpider(scrapy.Spider):
    channel, connection = make_exchange_queue_bind()
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "data/authors.json"}
    authors = queue.Queue()
    thread = threading.Thread(target=read_rabbit_msg,
                              args=(channel, RABBITMQ_QUEUE, authors, locker))

    def start_requests(self) -> Iterable[Request]:
        self.thread.start()

        while True:
            print(f"Queue size is {self.authors.qsize()}")
            author = self.authors.get()
            author_name, author_link = author.get("name"), author.get("link")
            if author_name and author_link:
                print(f'Scraped author: {author_name}, {author_link}')
                yield scrapy.Request(url=self.start_urls[0] + author_link)
            else:
                break
        self.thread.join()

    def parse(self, response, **kwargs):
        for author in response.xpath("/html//div[@class='author-details']"):
            print("Send request to get info about author")
            author_info = {
                "fullname": author.xpath("h3/text()").extract_first(),
                "born_date": author.xpath(
                    "//span[@class='author-born-date']/text()")
                .extract_first(),
                "born_location": author.xpath(
                    "//span[@class='author-born-location']/text()")
                .extract_first(),
                "description": author.xpath(
                    "//div[@class='author-description']/text()")
                .extract_first().strip(),
            }
            print(f"Author name: {author_info['fullname']}")
            yield author_info

    def closed(self, reason):
        self.thread.join()


# run spider AuthorSpider
if __name__ == "__main__":
    runner = CrawlerRunner()
    d = runner.crawl(AuthorSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

