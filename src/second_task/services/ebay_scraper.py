from bs4 import BeautifulSoup
import logging
from models.product_model import Product

class EbayScraper:
    def __init__(self, url: str, html_content: str):
        self.url = url
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.product = None

    def parse_data(self):
        try:
            name_tag = self.soup.find('h1', {'class': 'x-item-title__mainTitle'})
            name = name_tag.find('span').text.strip() if name_tag else 'N/A'
            logging.debug(f"Parsed name: {name}")
            
            price_tag = self.soup.find('div', {'class': 'x-price-primary'})
            price_span = price_tag.find('span', {'class': 'ux-textspans'}) if price_tag else None
            price_text = price_span.text if price_span else '0.0'
            price = float(''.join(filter(str.isdigit, price_text)) or 0.0) / 100
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

            returns_day = 0
            all_spans = self.soup.find_all('span')
            for span in all_spans:
                logging.debug(f"Checking span: {span.text.strip()}")
                if 'days returns' in span.text:
                    try:
                        returns_day = int(''.join(filter(str.isdigit, span.text)))
                        logging.debug(f"Found returns days: {returns_day}")
                        break
                    except ValueError:
                        logging.debug(f"Failed to parse returns days from span: {span.text.strip()}")
                        returns_day = 0

            logging.debug(f"Parsed returns_day: {returns_day}")

            self.product = Product(
                url=self.url,
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
