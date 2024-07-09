import requests
import redis
import json
from typing import List
from models.country_info import CountryInfo


class CountryRepository:
    def __init__(
        self,
        api_base_url: str,
        cache_duration: int,
        use_cache: bool,
        redis_host: str,
        redis_port: int,
        redis_db: int,
        redis_cache_key: str,
    ) -> None:
        self.api_base_url = api_base_url
        self.cache_duration = cache_duration
        self.use_cache = use_cache
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.redis_cache_key = redis_cache_key

    def fetch_data(self) -> List[CountryInfo]:
        if self.use_cache:
            cached_data = self.redis_client.get(self.redis_cache_key)
            if cached_data:
                data = json.loads(cached_data)
                return [CountryInfo(**item) for item in data]

        response = requests.get(self.api_base_url)
        response.raise_for_status()
        data = response.json()

        countries = []
        for item in data:
            name = item.get("name", {}).get("common", "N/A")
            capital = item.get("capital", ["N/A"])[0]
            flag_url = item.get("flags", {}).get("png", "N/A")
            countries.append(CountryInfo(name=name, capital=capital, flag_url=flag_url))

        if self.use_cache:
            self.redis_client.setex(
                self.redis_cache_key,
                self.cache_duration,
                json.dumps([country.dict() for country in countries]),
            )

        return countries
