# Avito Casablanca Rental Scraper

A Scrapy project to scrape real estate rental data from avito.ma, specifically for Casablanca properties.

## Installation

Install dependencies using uv:

```bash
uv sync
```

## Running the Spider

Navigate to the spider directory:

```bash
cd avito_scraper
```

Run the spider and save output to JSON:

```bash
scrapy crawl casablanca_rentals -o output.json
```

Run the spider and save output to CSV:

```bash
scrapy crawl casablanca_rentals -o output.csv
```

Run with custom settings:

```bash
scrapy crawl casablanca_rentals -o output.json -s LOG_LEVEL=DEBUG
```

## Project Structure

```
avito_scraper/
├── avito_scraper/
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── casablanca_rentals.py  # Main spider
│   ├── __init__.py
│   ├── items.py                    # Data models
│   ├── middlewares.py              # Custom middlewares
│   ├── pipelines.py                # Data processing pipelines
│   └── settings.py                 # Scrapy settings
└── scrapy.cfg                      # Scrapy config
```

## Data Fields

The spider extracts the following information:

- **listing_id**: Unique identifier for the listing
- **url**: Property listing URL
- **title**: Property title
- **price**: Monthly rental price (in Moroccan Dirham)
- **city**: City (Casablanca)
- **district**: Neighborhood/district
- **property_type**: Type of property (apartment, house, villa, etc.)
- **surface_area**: Property size in m²
- **num_rooms**: Number of rooms
- **num_bathrooms**: Number of bathrooms
- **floor**: Floor number
- **furnished**: Whether the property is furnished
- **features**: List of amenities/features
- **description**: Property description
- **images**: List of image URLs
- **seller_name**: Seller name
- **seller_type**: Professional or Individual
- **posted_date**: When the listing was posted
- **scraped_date**: When the data was scraped

## Important Notes

1. **CSS Selectors**: The CSS selectors in the spider are generic and may need adjustment based on the actual Avito.ma HTML structure. You should inspect the website and update the selectors accordingly.

2. **Rate Limiting**: The spider includes delays and auto-throttling to respect the website's resources. Adjust `DOWNLOAD_DELAY` in settings.py if needed.

3. **Casablanca City ID**: The city filter parameter may need verification. Check Avito.ma's URL structure to confirm the correct city ID for Casablanca.

4. **Robots.txt**: Currently set to `ROBOTSTXT_OBEY = False`. Change this according to your needs and respect the website's terms of service.

## Customization

To scrape other cities, modify the `start_requests` method in `casablanca_rentals.py`:

```python
params = "?cities=<city_id>"  # Change city ID
```

To add more data fields, update:
1. `items.py` - Add new field definitions
2. `casablanca_rentals.py` - Add extraction logic in `parse_property_detail`
