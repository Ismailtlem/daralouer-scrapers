import scrapy


class AvitoRentalItem(scrapy.Item):
    """Item to store rental property data from Avito.ma"""

    # Property identifiers
    listing_id = scrapy.Field()
    url = scrapy.Field()

    # Basic information
    title = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field()

    # Location
    city = scrapy.Field()
    district = scrapy.Field()

    # Property details
    property_type = scrapy.Field()  # Apartment, House, Villa, etc.
    surface_area = scrapy.Field()  # in m²
    num_rooms = scrapy.Field()
    num_bathrooms = scrapy.Field()
    floor = scrapy.Field()

    # Features
    furnished = scrapy.Field()
    features = scrapy.Field()  # List of features (e.g., parking, elevator, etc.)

    # Description
    description = scrapy.Field()

    # Images
    images = scrapy.Field()  # List of image URLs

    # Seller information
    seller_name = scrapy.Field()
    seller_type = scrapy.Field()  # Professional or Individual

    # Metadata
    posted_date = scrapy.Field()
    scraped_date = scrapy.Field()
