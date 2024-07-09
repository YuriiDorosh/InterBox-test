import requests
import json
import redis
from typing import List
from models.product_model import Product
import logging


class ProductRepository:
    def __init__(
        self,
        cache_duration: int,
        use_cache: bool,
        redis_host: str,
        redis_port: int,
        redis_db: int,
        redis_cache_key: str,
    ) -> None:

        self.use_cache = use_cache
        self.cache_duration = cache_duration
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.redis_cache_key = redis_cache_key

    def fetch_page(self, url: str) -> str:
        if self.use_cache:
            cached_data = self.redis_client.get(self.redis_cache_key)
            if cached_data:
                data = json.loads(cached_data)
                return data

        response = requests.get(url)
        response.raise_for_status()
        page_content = response.content

        if self.use_cache:
            self.redis_client.setex(url, self.cache_duration, page_content)

        return page_content

    def save_products(self, products: List[Product], filename: str):
        with open(filename, "w") as file:
            json.dump([product.dict() for product in products], file, indent=4)
        logging.info(f"Parsed data saved to {filename}")
