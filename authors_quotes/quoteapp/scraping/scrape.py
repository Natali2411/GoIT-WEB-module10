from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from .author import AuthorSpider
from .quote import QuotesSpider



@defer.inlineCallbacks
def crawl():
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    try:
        yield runner.crawl(QuotesSpider)
        yield runner.crawl(AuthorSpider)
    except Exception as e:
        # Log the exception
        print(f"Error during crawling: {e}")
    finally:
        # Stop the reactor regardless of success or failure
        reactor.stop()
