# services.py

import requests
import redis
import json
from typing import List
from models import CountryInfo
from settings import API_BASE_URL, CACHE_DURATION, USE_CACHE, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_CACHE_KEY

class CountryAPI:
    def __init__(self) -> None:
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def fetch_data(self) -> List[CountryInfo]:
        if USE_CACHE:
            cached_data = self.redis_client.get(REDIS_CACHE_KEY)
            if cached_data:
                data = json.loads(cached_data)
                return [CountryInfo(**item) for item in data]

        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        data = response.json()

        countries = []
        for item in data:
            name = item.get("name", {}).get("common", "N/A")
            capital = item.get("capital", ["N/A"])[0]
            flag_url = item.get("flags", {}).get("png", "N/A")
            countries.append(CountryInfo(name, capital, flag_url))

        if USE_CACHE:
            self.redis_client.setex(REDIS_CACHE_KEY, CACHE_DURATION, json.dumps([country.__dict__ for country in countries]))

        return countries
