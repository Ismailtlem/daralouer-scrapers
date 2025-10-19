from scrapy import signals
from scrapy.http import HtmlResponse
import logging

logger = logging.getLogger(__name__)


class AvitoScraperSpiderMiddleware:
    """Spider middleware for processing spider input/output"""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        logger.error(f"Spider exception on {response.url}: {exception}")

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        logger.info(f"Spider opened: {spider.name}")


class AvitoScraperDownloaderMiddleware:
    """Downloader middleware for processing requests/responses"""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        # Check for blocked/captcha responses
        if response.status in [403, 429]:
            logger.warning(
                f"Received status {response.status} for {request.url}. "
                "May be blocked or rate limited."
            )
        return response

    def process_exception(self, request, exception, spider):
        logger.error(f"Request exception on {request.url}: {exception}")

    def spider_opened(self, spider):
        logger.info(f"Spider opened: {spider.name}")
