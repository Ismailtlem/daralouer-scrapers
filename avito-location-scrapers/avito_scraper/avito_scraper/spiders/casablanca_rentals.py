import scrapy
from datetime import datetime
from avito_scraper.items import AvitoRentalItem


class CasablancaRentalsSpider(scrapy.Spider):
    name = "casablanca_rentals"
    allowed_domains = ["avito.ma"]

    def start_requests(self):
        """
        Start scraping rental listings in Casablanca.
        URL structure for Avito.ma rental properties in Casablanca
        """
        base_url = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_louer"

        # Add Casablanca filter - you may need to adjust the city parameter
        params = "?cities=3"  # Casablanca city ID (verify this)

        start_url = base_url + params

        yield scrapy.Request(
            url=start_url,
            callback=self.parse_listing_page,
            meta={'page': 1}
        )

    def parse_listing_page(self, response):
        """Parse the listing page to extract individual property links"""

        # Extract all property listing links
        # Note: CSS selectors may need adjustment based on actual Avito.ma structure
        listing_links = response.css('a.oan0b7::attr(href)').getall()

        if not listing_links:
            # Try alternative selectors
            listing_links = response.css('a[href*="/appartements"]::attr(href)').getall()

        # Follow each listing link
        for link in listing_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_property_detail,
                meta={'listing_url': full_url}
            )

        # Handle pagination
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_listing_page,
                meta={'page': response.meta.get('page', 1) + 1}
            )

    def parse_property_detail(self, response):
        """Parse individual property detail page"""

        item = AvitoRentalItem()

        # Extract listing ID from URL
        item['listing_id'] = response.url.split('/')[-1].split('-')[-1] if response.url else None
        item['url'] = response.meta.get('listing_url', response.url)

        # Basic information
        item['title'] = response.css('h1::text').get()

        # Price extraction
        price_text = response.css('span.sc-1x0vz2r-0::text').get()
        if not price_text:
            price_text = response.css('[class*="price"]::text').get()

        item['price'] = self.clean_price(price_text) if price_text else None
        item['price_currency'] = 'DH'  # Moroccan Dirham

        # Location
        item['city'] = 'Casablanca'
        item['district'] = response.css('[class*="location"] span::text').get()

        # Property details - these selectors need to be adjusted based on actual site structure
        property_details = response.css('[class*="details"] li')

        for detail in property_details:
            label = detail.css('span:first-child::text').get()
            value = detail.css('span:last-child::text').get()

            if label and value:
                label_lower = label.lower()

                if 'type' in label_lower or 'catégorie' in label_lower:
                    item['property_type'] = value
                elif 'surface' in label_lower or 'superficie' in label_lower:
                    item['surface_area'] = self.extract_number(value)
                elif 'pièce' in label_lower or 'chambre' in label_lower:
                    item['num_rooms'] = self.extract_number(value)
                elif 'salle' in label_lower and 'bain' in label_lower:
                    item['num_bathrooms'] = self.extract_number(value)
                elif 'étage' in label_lower or 'floor' in label_lower:
                    item['floor'] = value
                elif 'meublé' in label_lower or 'furnished' in label_lower:
                    item['furnished'] = 'oui' in value.lower() or 'yes' in value.lower()

        # Description
        item['description'] = ' '.join(response.css('[class*="description"] p::text').getall())

        # Features/Amenities
        features = response.css('[class*="features"] li::text').getall()
        item['features'] = [f.strip() for f in features if f.strip()]

        # Images
        image_urls = response.css('[class*="gallery"] img::attr(src)').getall()
        if not image_urls:
            image_urls = response.css('img[class*="image"]::attr(src)').getall()
        item['images'] = image_urls

        # Seller information
        item['seller_name'] = response.css('[class*="seller"] [class*="name"]::text').get()
        seller_type = response.css('[class*="seller"] [class*="type"]::text').get()
        item['seller_type'] = 'Professional' if seller_type and 'pro' in seller_type.lower() else 'Individual'

        # Dates
        posted_date_text = response.css('[class*="date"]::text').get()
        item['posted_date'] = posted_date_text
        item['scraped_date'] = datetime.now().isoformat()

        yield item

    @staticmethod
    def clean_price(price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None

        # Remove currency symbols and spaces
        import re
        price_clean = re.sub(r'[^\d,.]', '', price_text)
        price_clean = price_clean.replace(',', '').replace('.', '')

        try:
            return int(price_clean)
        except ValueError:
            return None

    @staticmethod
    def extract_number(text):
        """Extract first number from text"""
        if not text:
            return None

        import re
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else None
