import scrapy


class AvitoRentalDataSpider(scrapy.Spider):
    name = "avito_rental_data"
    allowed_domains = ["avito.ma"]
    start_urls = ["https://avito.ma"]

    def parse(self, response):
        pass
