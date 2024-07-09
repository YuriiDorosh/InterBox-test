from repositories.product_repository import ProductRepository
from services.ebay_scraper import EbayScraper
import logging

class ScraperController:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def scrape_and_save_products(self, urls, output_file):
        products = []
        for url in urls:
            url = url.strip()
            if not url:
                continue
            logging.info(f"Processing URL: {url}")
            html_content = self.product_repository.fetch_page(url)
            scraper = EbayScraper(url, html_content)
            scraper.parse_data()
            product = scraper.get_product()
            if product:
                products.append(product)
            logging.info(f"Finished processing URL: {url}")

        self.product_repository.save_products(products, output_file)
