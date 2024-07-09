# from models.product_model import Product
# import requests
# from bs4 import BeautifulSoup
# import json
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class EbayScraper:
#     def __init__(self, url):
#         self.url = url
#         self.soup = None
#         self.product = None

#     def fetch_page(self):
#         response = requests.get(self.url)
#         if response.status_code == 200:
#             self.soup = BeautifulSoup(response.content, 'html.parser')
#         else:
#             print(f"Failed to fetch page. Status code: {response.status_code}")

#     def parse_data(self):
#         if not self.soup:
#             logging.warning(f"No content to parse for URL: {self.url}")
#             return
        
#         try:
#             name_tag = self.soup.find('h1', {'class': 'x-item-title__mainTitle'})
#             name = name_tag.find('span').text.strip() if name_tag else 'N/A'
#             logging.debug(f"Parsed name: {name}")
            
#             price_tag = self.soup.find('div', {'class': 'x-price-primary'})
#             price_span = price_tag.find('span', {'class': 'ux-textspans'}) if price_tag else None
#             price = float(price_span.text.replace('US', '').replace('$', '').strip()) if price_span else 0.0
#             logging.debug(f"Parsed price: {price}")
            
#             main_img_tag = self.soup.find('div', {'class': 'ux-image-carousel-item image-treatment active image'})
#             main_img_url = main_img_tag.find('img')['src'] if main_img_tag else 'N/A'
#             logging.debug(f"Parsed main_img_url: {main_img_url}")

#             second_img_button = self.soup.select('button.ux-image-grid-item.image-treatment.rounded-edges')
#             second_img_url = second_img_button[1].find('img')['src'] if len(second_img_button) > 1 else 'N/A'
#             logging.debug(f"Parsed second_img_url: {second_img_url}")
            
#             seller_tag = self.soup.find('h2', {'class': 'd-stores-info-categories__container__info__section__title'})
#             if seller_tag:
#                 seller_span = seller_tag.find('span', {'class': 'ux-textspans ux-textspans--BOLD'}) if seller_tag else None
#                 seller = seller_span.text.strip() if seller_span else 'N/A'
#                 logging.debug(f"Parsed seller: {seller}")
                
#                 seller_link_tag = seller_tag.find('a', {'class': 'ux-action'})
#                 seller_link = seller_link_tag['href'] if seller_link_tag else 'N/A'
#                 logging.debug(f"Parsed seller_link: {seller_link}")
#             else:
#                 seller = 'N/A'
#                 seller_link = 'N/A'
#                 logging.debug(f"No seller information found for URL: {self.url}")
            
#             seller_info_tag = self.soup.find('div', class_='d-stores-info-categories__container__details')
#             seller_joined_span = seller_info_tag.find('span', {'class': 'ux-textspans'}) if seller_info_tag else None
#             seller_joined_at = seller_joined_span.text.strip().replace('Joined ', '') if seller_joined_span else 'N/A'
#             logging.debug(f"Parsed seller_joined_at: {seller_joined_at}")
            
#             seller_items_sold_tag = self.soup.find_all('div', class_='d-stores-info-categories__container__info__section__item')
#             seller_items_sold_span = None

#             for tag in seller_items_sold_tag:
#                 span_tag = tag.find('span', {'class': 'ux-textspans ux-textspans--BOLD'})
#                 if span_tag and 'items sold' in tag.text:
#                     seller_items_sold_span = span_tag
#                     break

#             seller_items_sold = float(seller_items_sold_span.text.replace('K', '000').replace('M', '000000').replace('.', '').strip()) if seller_items_sold_span else 0.0
#             logging.debug(f"Parsed seller_items_sold: {seller_items_sold}")
            
#             shipping_tag = self.soup.find('div', {'data-testid': 'ux-layout-section__item'})
#             shipping_price_span = shipping_tag.find('span', {'class': 'ux-textspans ux-textspans--BOLD ux-textspans--NEGATIVE'}) if shipping_tag else None
#             shipping_price = shipping_price_span.text.strip() if shipping_price_span else 'N/A'
#             logging.debug(f"Parsed shipping_price: {shipping_price}")

#             returns_div = self.soup.find('div', {'class': 'ux-labels-values__values-content'})
#             returns_day = 0
#             if returns_div:
#                 span_elements = returns_div.find_all('span')
#                 for span in span_elements:
#                     if 'days returns' in span.text:
#                         try:
#                             returns_day = int(''.join(filter(str.isdigit, span.text)))
#                         except ValueError:
#                             returns_day = 0
#             logging.debug(f"Parsed returns_day: {returns_day}")

#             self.product = Product(
#                 name=name,
#                 price=price,
#                 main_img_url=main_img_url,
#                 second_img_url=second_img_url,
#                 seller=seller,
#                 seller_link=seller_link,
#                 seller_joined_at=seller_joined_at,
#                 seller_items_sold=seller_items_sold,
#                 shipping_price=shipping_price,
#                 returns_day=returns_day
#             )
#         except Exception as e:
#             logging.error(f"Error parsing data for URL: {self.url} - {e}")


#     def get_product(self):
#         return self.product

#     def save_to_file(self, filename):
#         with open(filename, 'w') as file:
#             json.dump(self.product.model_dump(), file, indent=4)

#     def print_product(self):
#         print(json.dumps(self.product.model_dump(), indent=4))
        

# def parse_multiple_products(file_path):
#     with open(file_path, 'r') as file:
#         urls = file.readlines()
    
#     products = []
#     for url in urls:
#         url = url.strip()
#         if not url:
#             continue
#         logging.info(f"Processing URL: {url}")
#         scraper = EbayScraper(url)
#         scraper.fetch_page()
#         scraper.parse_data()
#         product = scraper.get_product()
#         if product:
#             products.append(product.model_dump())
#         logging.info(f"Finished processing URL: {url}")

#     return products


# if __name__ == "__main__":
#     file_path = 'products.txt'
#     products = parse_multiple_products(file_path)
#     output_file = 'ebay_products_data.json'
#     with open(output_file, 'w') as file:
#         json.dump(products, file, indent=4)
#     logging.info(f"Parsed data saved to {output_file}")

from models.product_model import Product
import requests
from bs4 import BeautifulSoup
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.product = None

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            logging.info(f"Fetched page for URL: {self.url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch page for URL: {self.url} - {e}")

    def parse_data(self):
        if not self.soup:
            logging.warning(f"No content to parse for URL: {self.url}")
            return
        
        try:
            name_tag = self.soup.find('h1', {'class': 'x-item-title__mainTitle'})
            name = name_tag.find('span').text.strip() if name_tag else 'N/A'
            logging.debug(f"Parsed name: {name}")
            
            price_tag = self.soup.find('div', {'class': 'x-price-primary'})
            price_span = price_tag.find('span', {'class': 'ux-textspans'}) if price_tag else None
            price_text = price_span.text if price_span else '0.0'
            price = float(''.join(filter(str.isdigit, price_text)) or 0.0)
            price = price / 100
            logging.debug(f"Parsed price: {price}")
            
            main_img_tag = self.soup.find('div', {'class': 'ux-image-carousel-item image-treatment active image'})
            main_img_url = main_img_tag.find('img')['src'] if main_img_tag else 'N/A'
            logging.debug(f"Parsed main_img_url: {main_img_url}")

            second_img_button = self.soup.select('button.ux-image-grid-item.image-treatment.rounded-edges')
            second_img_url = second_img_button[1].find('img')['src'] if len(second_img_button) > 1 else 'N/A'
            logging.debug(f"Parsed second_img_url: {second_img_url}")
            
            seller_tag = self.soup.find('h2', {'class': 'd-stores-info-categories__container__info__section__title'})
            if seller_tag:
                seller_span = seller_tag.find('span', {'class': 'ux-textspans ux-textspans--BOLD'}) if seller_tag else None
                seller = seller_span.text.strip() if seller_span else 'N/A'
                logging.debug(f"Parsed seller: {seller}")
                
                seller_link_tag = seller_tag.find('a', {'class': 'ux-action'})
                seller_link = seller_link_tag['href'] if seller_link_tag else 'N/A'
                logging.debug(f"Parsed seller_link: {seller_link}")
            else:
                seller = 'N/A'
                seller_link = 'N/A'
                logging.debug(f"No seller information found for URL: {self.url}")
            
            seller_info_tag = self.soup.find('div', class_='d-stores-info-categories__container__details')
            seller_joined_span = seller_info_tag.find('span', {'class': 'ux-textspans'}) if seller_info_tag else None
            seller_joined_at = seller_joined_span.text.strip().replace('Joined ', '') if seller_joined_span else 'N/A'
            logging.debug(f"Parsed seller_joined_at: {seller_joined_at}")
            
            seller_items_sold_tag = self.soup.find_all('div', class_='d-stores-info-categories__container__info__section__item')
            seller_items_sold_span = None

            for tag in seller_items_sold_tag:
                span_tag = tag.find('span', {'class': 'ux-textspans ux-textspans--BOLD'})
                if span_tag and 'items sold' in tag.text:
                    seller_items_sold_span = span_tag
                    break

            seller_items_sold = float(seller_items_sold_span.text.replace('K', '000').replace('M', '000000').replace('.', '').strip()) if seller_items_sold_span else 0.0
            logging.debug(f"Parsed seller_items_sold: {seller_items_sold}")
            
            shipping_tag = self.soup.find('div', {'data-testid': 'ux-layout-section__item'})
            shipping_price_span = shipping_tag.find('span', {'class': 'ux-textspans ux-textspans--BOLD ux-textspans--NEGATIVE'}) if shipping_tag else None
            shipping_price = shipping_price_span.text.strip() if shipping_price_span else 'N/A'
            logging.debug(f"Parsed shipping_price: {shipping_price}")

            all_spans = self.soup.find_all('span')
            returns_day = 0
            for span in all_spans:

                if 'days returns' in span.text:
                    try:
                        returns_day = int(''.join(filter(str.isdigit, span.text)))
                    except ValueError:
                        returns_day = 0
            logging.debug(f"Parsed returns_day: {returns_day}")

            self.product = Product(
                url = self.url,
                name=name,
                price=price,
                main_img_url=main_img_url,
                second_img_url=second_img_url,
                seller=seller,
                seller_link=seller_link,
                seller_joined_at=seller_joined_at,
                seller_items_sold=seller_items_sold,
                shipping_price=shipping_price,
                returns_day=returns_day
            )
        except Exception as e:
            logging.error(f"Error parsing data for URL: {self.url} - {e}")

    def get_product(self):
        return self.product


def parse_multiple_products(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    products = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        logging.info(f"Processing URL: {url}")
        scraper = EbayScraper(url)
        scraper.fetch_page()
        scraper.parse_data()
        product = scraper.get_product()
        if product:
            products.append(product.model_dump())
        logging.info(f"Finished processing URL: {url}")

    return products


if __name__ == "__main__":
    file_path = 'products.txt'
    products = parse_multiple_products(file_path)
    output_file = 'ebay_products_data.json'
    with open(output_file, 'w') as file:
        json.dump(products, file, indent=4)
    logging.info(f"Parsed data saved to {output_file}")
