class Settings:
    FILE_NAME = "products.txt"
    CACHE_DURATION = 3600  # 1 година
    USE_CACHE = True  # По дефолту залишаємо кешування увімкненим
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_CACHE_KEY = "product_data"