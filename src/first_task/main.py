import sys
from repositories.country_repository import CountryRepository
from services.country_service import CountryService
from controllers.country_controller import CountryController
from settings import Settings


def main():
    settings = Settings()

    if len(sys.argv) > 1 and sys.argv[1] == "--no-cache":
        settings.USE_CACHE = False

    repository = CountryRepository(
        api_base_url=settings.API_BASE_URL,
        cache_duration=settings.CACHE_DURATION,
        use_cache=settings.USE_CACHE,
        redis_host=settings.REDIS_HOST,
        redis_port=settings.REDIS_PORT,
        redis_db=settings.REDIS_DB,
        redis_cache_key=settings.REDIS_CACHE_KEY,
    )
    service = CountryService(repository)
    controller = CountryController(service)
    controller.display_data()


if __name__ == "__main__":
    main()
