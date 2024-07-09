import sys
from settings import Settings
from controllers.scraper_controller import ScraperController
from repositories.product_repository import ProductRepository
from typing import List


def parse_multiple_products(file_path) -> List[str]:
    with open(file_path, "r") as file:
        urls = file.readlines()
    return urls


def main() -> None:
    settings = Settings()

    if len(sys.argv) > 1 and sys.argv[1] == "--no-cache":
        settings.USE_CACHE = False

    file_path = settings.FILE_NAME
    output_file = settings.OUTPUT_FILE

    product_repository = ProductRepository(
        cache_duration=settings.CACHE_DURATION,
        use_cache=settings.USE_CACHE,
        redis_host=settings.REDIS_HOST,
        redis_port=settings.REDIS_PORT,
        redis_db=settings.REDIS_DB,
        redis_cache_key=settings.REDIS_CACHE_KEY,
    )
    scraper_controller = ScraperController(product_repository)

    urls = parse_multiple_products(file_path)
    scraper_controller.scrape_and_save_products(urls, output_file)


if __name__ == "__main__":
    main()
