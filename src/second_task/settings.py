import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Settings:
    FILE_NAME = "products.txt"
    OUTPUT_FILE = "ebay_products_data.json"
    CACHE_DURATION = 3600  # 1 година
    USE_CACHE = True  # По дефолту залишаємо кешування увімкненим
    REDIS_HOST = "redis"  # Поміняти на localhost, якщо ви запускаєте Redis не в докері
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_CACHE_KEY = "product_data"
