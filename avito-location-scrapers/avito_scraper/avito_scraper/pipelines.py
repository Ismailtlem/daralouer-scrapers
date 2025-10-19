import logging
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)


class AvitoScraperPipeline:
    """Pipeline for processing scraped items"""

    def open_spider(self, spider):
        """Called when spider is opened"""
        logger.info(f"Opening spider: {spider.name}")
        self.items_scraped = 0

    def close_spider(self, spider):
        """Called when spider is closed"""
        logger.info(f"Closing spider: {spider.name}. Total items scraped: {self.items_scraped}")

    def process_item(self, item, spider):
        """Process and validate each scraped item"""
        adapter = ItemAdapter(item)

        # Clean and validate data
        # Remove extra whitespace from string fields
        for field in adapter.field_names():
            value = adapter.get(field)
            if isinstance(value, str):
                adapter[field] = value.strip()

        # Validate required fields
        required_fields = ['listing_id', 'title', 'price', 'city']
        for field in required_fields:
            if not adapter.get(field):
                logger.warning(
                    f"Item missing required field '{field}': {adapter.get('url', 'unknown URL')}"
                )

        self.items_scraped += 1

        return item
